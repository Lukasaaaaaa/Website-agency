#!/usr/bin/env python3
"""
Google Maps Scraper via Playwright (headless Chromium)
Kein API-Key nötig. Echte Daten.
"""

import json, time, re
from playwright.sync_api import sync_playwright

def search_google_maps(query: str, location: str, max_results: int = 20) -> dict:
    """
    Sucht auf Google Maps nach lokalen Unternehmen.
    Gibt Liste mit name, address, phone, rating, review_count, website zurück.
    """
    results = []
    search_query = f"{query} in {location}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            locale="de-DE",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = ctx.new_page()

        url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
        print(f"  Scraping: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # Cookie-Banner wegklicken falls vorhanden
        try:
            page.click("button:has-text('Alle ablehnen')", timeout=3000)
        except:
            try:
                page.click("button:has-text('Accept all')", timeout=2000)
            except:
                pass
        time.sleep(1)

        # Ergebnis-Liste scrollen um mehr zu laden
        panel = page.query_selector('div[role="feed"]')
        if panel:
            for _ in range(5):
                panel.evaluate("el => el.scrollBy(0, 800)")
                time.sleep(1)

        # Alle Einträge sammeln
        items = page.query_selector_all('div[role="feed"] > div > div > a')
        print(f"  Gefunden: {len(items)} Einträge")

        for item in items[:max_results]:
            try:
                item.click()
                time.sleep(2)

                name = ""
                address = ""
                phone = ""
                website = None
                rating = 0.0
                review_count = 0
                category = ""

                # Name
                h1 = page.query_selector('h1.DUwDvf, h1[class*="fontHeadlineLarge"]')
                if h1:
                    name = h1.inner_text().strip()

                if not name:
                    continue

                # Kategorie
                cat_el = page.query_selector('button.DkEaL, span.DkEaL, [jsaction*="category"]')
                if cat_el:
                    category = cat_el.inner_text().strip()

                # Rating
                rating_el = page.query_selector('div.F7nice span[aria-hidden="true"]')
                if rating_el:
                    try:
                        rating = float(rating_el.inner_text().strip().replace(",", "."))
                    except:
                        pass

                # Review count
                review_el = page.query_selector('div.F7nice span[aria-label*="Rezension"], div.F7nice span[aria-label*="review"]')
                if review_el:
                    m = re.search(r'[\d.]+', review_el.get_attribute("aria-label") or "")
                    if m:
                        review_count = int(m.group().replace(".", ""))

                # Adresse
                addr_el = page.query_selector('button[data-item-id="address"] .Io6YTe, [data-tooltip="Adresse kopieren"] .Io6YTe')
                if addr_el:
                    address = addr_el.inner_text().strip()

                # Telefon
                phone_el = page.query_selector('button[data-item-id^="phone"] .Io6YTe, [data-tooltip="Telefonnummer kopieren"] .Io6YTe')
                if phone_el:
                    phone = phone_el.inner_text().strip()

                # Website
                web_el = page.query_selector('a[data-item-id="authority"] .Io6YTe, a[href*="http"][data-tooltip*="ebsite"] .Io6YTe')
                if web_el:
                    website = web_el.inner_text().strip()
                    # Vollständige URL holen
                    web_link = page.query_selector('a[data-item-id="authority"], a[data-tooltip*="Website"]')
                    if web_link:
                        href = web_link.get_attribute("href")
                        if href and href.startswith("http"):
                            website = href

                if name:
                    results.append({
                        "name": name,
                        "address": address,
                        "phone": phone,
                        "rating": rating,
                        "review_count": review_count,
                        "website": website,
                        "category": category,
                        "place_id": f"maps_{len(results):03d}"
                    })
                    print(f"  + {name} | ⭐{rating} ({review_count}) | 🌐 {'ja' if website else 'nein'}")

            except Exception as e:
                print(f"  Fehler bei Eintrag: {e}")
                continue

        browser.close()

    return {
        "results": results,
        "total_found": len(results),
        "source": "playwright_maps"
    }


def check_url(url: str) -> dict:
    """Prüft ob eine Website existiert und wie modern sie ist."""
    if not url or url.upper() in ("FEHLT", "NONE", "N/A", ""):
        return {"exists": False, "status": "missing"}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            resp = page.goto(url, timeout=15000, wait_until="domcontentloaded")
            status_code = resp.status if resp else 0

            if not resp or status_code >= 400:
                browser.close()
                return {"exists": False, "status": "broken", "status_code": status_code}

            html = page.content().lower()

            # CMS Detection
            cms = None
            if "wp-content" in html or "wordpress" in html:
                cms = "WordPress"
            elif "squarespace" in html:
                cms = "Squarespace"
            elif "wix.com" in html:
                cms = "Wix"
            elif "jimdo" in html:
                cms = "Jimdo"
            elif "webflow" in html:
                cms = "Webflow"

            responsive = "width=device-width" in html
            ssl = url.startswith("https://")

            # Copyright Jahr
            yr_match = re.search(r'(?:copyright|©|\(c\))\s*(\d{4})', html)
            copyright_year = int(yr_match.group(1)) if yr_match else None

            modern = ssl and responsive and cms and copyright_year and copyright_year >= 2022

            browser.close()
            return {
                "exists": True,
                "status_code": status_code,
                "is_responsive": responsive,
                "has_ssl": ssl,
                "cms": cms,
                "copyright_year": copyright_year,
                "status": "modern" if modern else "outdated"
            }
        except Exception as e:
            browser.close()
            return {"exists": False, "status": "error", "error": str(e)}


if __name__ == "__main__":
    # Testlauf
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Elektriker"
    location = sys.argv[2] if len(sys.argv) > 2 else "Berlin"
    result = search_google_maps(query, location, max_results=10)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def fetch_logo(url: str):
    """
    Versucht das Logo einer Website zu holen.
    Gibt data-URI (base64) zurück oder None.
    Priorität: og:image > apple-touch-icon > favicon > img[class*=logo]
    """
    import base64, requests as req
    if not url:
        return None
    try:
        r = req.get(url, timeout=10)
        html = r.text
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        from urllib.parse import urljoin

        candidates = []

        # 1. OG image
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            candidates.append(og["content"])

        # 2. Apple touch icon (hochauflösend)
        for rel in ["apple-touch-icon", "apple-touch-icon-precomposed"]:
            link = soup.find("link", rel=rel)
            if link and link.get("href"):
                candidates.append(urljoin(url, link["href"]))

        # 3. img mit "logo" in class/id/alt/src
        for img in soup.find_all("img"):
            attrs = " ".join([
                img.get("class", [""])[0] if img.get("class") else "",
                img.get("id", ""),
                img.get("alt", ""),
                img.get("src", ""),
            ]).lower()
            if "logo" in attrs and img.get("src"):
                candidates.append(urljoin(url, img["src"]))

        # 4. Favicon als Fallback
        icon = soup.find("link", rel=lambda r: r and "icon" in r)
        if icon and icon.get("href"):
            candidates.append(urljoin(url, icon["href"]))

        # Ersten gültigen Kandidaten laden
        for candidate_url in candidates[:4]:
            try:
                img_r = req.get(candidate_url, timeout=8)
                if img_r.status_code == 200 and len(img_r.content) > 500:
                    ctype = img_r.headers.get("content-type", "image/png").split(";")[0]
                    b64 = base64.b64encode(img_r.content).decode()
                    return f"data:{ctype};base64,{b64}"
            except:
                continue
    except Exception as e:
        print(f"  Logo-Fehler: {e}")
    return None
