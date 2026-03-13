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
      // Replace form with simple success message for the customer
      formWrap.innerHTML = `
        <div class="form-success">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="22" stroke="currentColor" stroke-width="2"/>
            <path d="M15 24l6 6 12-12" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <h3>Vielen Dank für Ihre Anfrage!</h3>
          <p>Ich habe Ihre Nachricht erhalten und melde mich innerhalb von 24 Stunden bei Ihnen.</p>
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

