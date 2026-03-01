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
contactForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const btn = contactForm.querySelector('button[type="submit"]');
  const originalText = btn.innerHTML;
  btn.innerHTML = `
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 10l3 3 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    Nachricht gesendet!
  `;
  btn.disabled = true;
  btn.style.opacity = '0.7';
  setTimeout(() => {
    btn.innerHTML = originalText;
    btn.disabled = false;
    btn.style.opacity = '1';
    contactForm.reset();
  }, 3000);
});

