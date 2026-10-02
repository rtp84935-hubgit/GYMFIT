/* ==========================================================================
   GYMFIT — MAIN SCRIPT
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------------------------------------------------------------------
     1. PRELOADER — hide once page has fully loaded
  --------------------------------------------------------------------- */
  const preloader = document.getElementById('preloader');
  window.addEventListener('load', () => {
    setTimeout(() => preloader.classList.add('loaded'), 500);
  });
  // fallback in case 'load' already fired
  setTimeout(() => preloader && preloader.classList.add('loaded'), 3000);

  /* ---------------------------------------------------------------------
     2. STICKY NAV — transparency change on scroll + active link highlight
  --------------------------------------------------------------------- */
  const nav = document.getElementById('mainNav');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id], header[id]');

  function handleNavScroll() {
    if (window.scrollY > 60) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }

    // Highlight active section link
    let current = '';
    sections.forEach(sec => {
      const top = sec.offsetTop - 120;
      if (window.scrollY >= top) current = sec.getAttribute('id');
    });
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) link.classList.add('active');
    });
  }
  window.addEventListener('scroll', handleNavScroll);
  handleNavScroll();

  // Collapse mobile menu after clicking a link
  document.querySelectorAll('#navMenu .nav-link').forEach(link => {
    link.addEventListener('click', () => {
      const menu = document.getElementById('navMenu');
      if (menu.classList.contains('show')) {
        bootstrap.Collapse.getOrCreateInstance(menu).hide();
      }
    });
  });

  /* ---------------------------------------------------------------------
     3. HERO PARALLAX EFFECT
  --------------------------------------------------------------------- */
  const heroBg = document.getElementById('heroParallax');
  window.addEventListener('scroll', () => {
    const offset = window.scrollY;
    if (offset < window.innerHeight) {
      heroBg.style.transform = `translateY(${offset * 0.35}px) scale(1.05)`;
    }
  });

  /* ---------------------------------------------------------------------
     4. TYPING ANIMATION FOR HERO HEADING
  --------------------------------------------------------------------- */
  const typedEl = document.getElementById('typedHeading');
  const fullText = "Transform Your Body, Transform Your Life";
  let charIndex = 0;

  function typeWriter() {
    if (charIndex <= fullText.length) {
      typedEl.textContent = fullText.slice(0, charIndex);
      charIndex++;
      setTimeout(typeWriter, 45);
    }
  }
  typeWriter();

  /* ---------------------------------------------------------------------
     5. SCROLL REVEAL ANIMATIONS (fade-in sections/cards)
  --------------------------------------------------------------------- */
  const revealEls = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach(el => revealObserver.observe(el));

  /* ---------------------------------------------------------------------
     6. NUMBER COUNTER ANIMATIONS
  --------------------------------------------------------------------- */
  const counters = document.querySelectorAll('.counter');
  function animateCounter(el) {
    const target = parseFloat(el.getAttribute('data-target'));
    const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    const duration = 1600;
    const startTime = performance.now();

    function tick(now) {
      const progress = Math.min((now - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      const value = target * eased;
      el.textContent = decimals > 0 ? value.toFixed(decimals) : Math.floor(value).toLocaleString();
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = decimals > 0 ? target.toFixed(decimals) : target.toLocaleString();
    }
    requestAnimationFrame(tick);
  }

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });
  counters.forEach(el => counterObserver.observe(el));

  /* ---------------------------------------------------------------------
     7. ANIMATED CIRCULAR PROGRESS RINGS (on viewport enter)
  --------------------------------------------------------------------- */
  const CIRCUMFERENCE = 2 * Math.PI * 60; // r = 60

  document.querySelectorAll('.ring-fill').forEach(ring => {
    ring.style.strokeDasharray = `${CIRCUMFERENCE}`;
    ring.style.strokeDashoffset = `${CIRCUMFERENCE}`;
  });

  const ringObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const ring = entry.target.querySelector('.ring-fill');
        const percent = parseFloat(ring.getAttribute('data-percent'));
        const offset = CIRCUMFERENCE - (percent / 100) * CIRCUMFERENCE;
        requestAnimationFrame(() => { ring.style.strokeDashoffset = offset; });
        ringObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.ring-wrap').forEach(el => ringObserver.observe(el));

  /* ---------------------------------------------------------------------
     8. ROTATING MOTIVATIONAL QUOTES
  --------------------------------------------------------------------- */
  const quotes = [
    "Discipline is choosing between what you want now and what you want most.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "Progress, not perfection — every rep counts.",
    "Your only competition is who you were yesterday.",
    "Consistency is what transforms average into excellence.",
    "Sweat is just fat crying. Keep going."
  ];
  let quoteIndex = 0;
  const quoteEl = document.getElementById('quoteText');

  setInterval(() => {
    quoteEl.classList.add('fade-out');
    setTimeout(() => {
      quoteIndex = (quoteIndex + 1) % quotes.length;
      quoteEl.textContent = quotes[quoteIndex];
      quoteEl.classList.remove('fade-out');
    }, 600);
  }, 4500);

  /* ---------------------------------------------------------------------
     9. BUTTON RIPPLE EFFECT
  --------------------------------------------------------------------- */
  document.querySelectorAll('.ripple').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const rect = this.getBoundingClientRect();
      const circle = document.createElement('span');
      const size = Math.max(rect.width, rect.height);
      circle.classList.add('ripple-circle');
      circle.style.width = circle.style.height = `${size}px`;
      circle.style.left = `${e.clientX - rect.left - size / 2}px`;
      circle.style.top = `${e.clientY - rect.top - size / 2}px`;
      this.appendChild(circle);
      setTimeout(() => circle.remove(), 650);
    });
  });

  /* ---------------------------------------------------------------------
     10. FOOTER YEAR
  --------------------------------------------------------------------- */
  document.getElementById('year').textContent = new Date().getFullYear();

});