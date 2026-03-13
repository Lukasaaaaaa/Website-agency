// ——— Navigation ———
const nav = document.getElementById('nav');
const navBurger = document.getElementById('navBurger');
const navLinks = document.getElementById('navLinks');

// Sticky nav
let lastScroll = 0;
window.addEventListener('scroll', () => {
  const currentScroll = window.scrollY;
  if (currentScroll > 60) {
    nav.classList.add('nav--scrolled');
  } else {
    nav.classList.remove('nav--scrolled');
  }
  lastScroll = currentScroll;
});

// Mobile menu toggle
navBurger.addEventListener('click', () => {
  navBurger.classList.toggle('nav__burger--active');
  navLinks.classList.toggle('nav__links--open');
  document.body.classList.toggle('no-scroll');
});

// Close mobile menu on link click
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navBurger.classList.remove('nav__burger--active');
    navLinks.classList.remove('nav__links--open');
    document.body.classList.remove('no-scroll');
  });
});

// ——— Smooth scroll ———
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;
    const target = document.querySelector(targetId);
    if (target) {
      e.preventDefault();
      const offset = nav.offsetHeight + 20;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ——— Scroll Animations (Intersection Observer) ———
const animElements = document.querySelectorAll('.anim-fade-up');

const observerOptions = {
  root: null,
  rootMargin: '0px 0px -60px 0px',
  threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const delay = parseInt(entry.target.dataset.delay) || 0;
      setTimeout(() => {
        entry.target.classList.add('anim-visible');
      }, delay);
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

animElements.forEach(el => observer.observe(el));

// ——— Sticky Mobile CTA ———
const stickyCta = document.getElementById('stickyCta');
if (stickyCta) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      stickyCta.classList.add('sticky-cta--visible');
    } else {
      stickyCta.classList.remove('sticky-cta--visible');
    }
  });
}

// ——— Contact Form ———
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = contactForm.querySelector('button[type="submit"]');
  const originalText = btn.innerHTML;
  const formWrap = contactForm.closest('.contact__form-wrap');

  // Show loading state
  btn.innerHTML = `
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" class="spin"><circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="2" stroke-dasharray="40" stroke-linecap="round"/></svg>
    Wird gesendet...
  `;
  btn.disabled = true;

  try {
    const response = await fetch('https://formspree.io/f/mjgarnga', {
      method: 'POST',
      body: new FormData(contactForm),
      headers: { 'Accept': 'application/json' }
    });

    if (response.ok) {
      // Replace form with success message + direct contact options
      formWrap.innerHTML = `
        <div class="form-success">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="22" stroke="currentColor" stroke-width="2"/>
            <path d="M15 24l6 6 12-12" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <h3>Anfrage erhalten!</h3>
          <p>Ich melde mich innerhalb von 24 Stunden bei Ihnen. Sie können mich auch direkt erreichen:</p>
          <div class="form-success__actions">
            <a href="https://wa.me/491752040444?text=Hallo%2C%20ich%20habe%20gerade%20eine%20Anfrage%20%C3%BCber%20die%20Website%20geschickt." class="btn btn--primary btn--full" target="_blank" rel="noopener">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" fill="currentColor"/><path d="M12 2C6.477 2 2 6.477 2 12c0 1.89.525 3.66 1.438 5.168L2 22l4.832-1.438A9.955 9.955 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2z" stroke="currentColor" stroke-width="2"/></svg>
              Direkt per WhatsApp schreiben
            </a>
            <a href="mailto:lukas@websitepolierer.de" class="btn btn--outline btn--full">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="2" y="4" width="20" height="16" rx="2" stroke="currentColor" stroke-width="2"/><path d="M22 6l-10 7L2 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              E-Mail schreiben
            </a>
          </div>
        </div>
      `;
    } else {
      throw new Error('Form submission failed');
    }
  } catch (error) {
    btn.innerHTML = originalText;
    btn.disabled = false;
    // Show inline error
    const errorMsg = document.createElement('p');
    errorMsg.className = 'form__error';
    errorMsg.textContent = 'Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut oder schreiben Sie mir direkt per WhatsApp.';
    const existingError = contactForm.querySelector('.form__error');
    if (existingError) existingError.remove();
    btn.parentNode.insertBefore(errorMsg, btn.nextSibling);
  }
});

