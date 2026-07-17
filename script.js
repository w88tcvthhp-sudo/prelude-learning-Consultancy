/* =====================================================================
   PRELUDE LEARNING & CONSULTANCY
   script.js — interaction layer
   ===================================================================== */
(function () {
  'use strict';

  /* ---- Sticky nav: add .scrolled once the page is scrolled ---- */
  var nav = document.getElementById('nav');
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---- Mobile menu: toggle panel, animate burger, lock body scroll ---- */
  var burger = document.getElementById('burger');
  var links = document.getElementById('navLinks');

  function toggleMenu(forceState) {
    if (!links || !nav) return;
    var willOpen = (typeof forceState === 'boolean')
      ? forceState
      : !links.classList.contains('open');
    links.classList.toggle('open', willOpen);
    nav.classList.toggle('menu-open', willOpen);
    document.body.style.overflow = willOpen ? 'hidden' : '';
  }

  if (burger) {
    burger.addEventListener('click', function () { toggleMenu(); });
  }
  if (links) {
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { toggleMenu(false); });
    });
  }

  /* ---- Sectors nav dropdown: click-toggle (mobile/touch); desktop uses CSS :hover ---- */
  document.querySelectorAll('.nav-item.has-dropdown').forEach(function (item) {
    var btn = item.querySelector('.nav-drop-btn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var isOpen = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  });

  /* ---- Scroll-reveal: fade/slide elements in as they enter view ---- */
  var revealEls = document.querySelectorAll('.reveal:not(.in)');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    // Fallback: show everything if IntersectionObserver is unavailable
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- Current year in the footer ---- */
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---- Sticky CTA: appears after the hero, dismissible, hidden on contact/privacy ---- */
  var stickyCta = document.getElementById('stickyCta');
  var suppressedPages = ['contact.html', 'privacy.html'];
  var onSuppressedPage = suppressedPages.some(function (p) { return location.pathname.indexOf(p) !== -1; });
  if (stickyCta && !onSuppressedPage && sessionStorage.getItem('stickyCtaDismissed') !== '1') {
    var ctaShown = false;
    var onCtaScroll = function () {
      var trigger = window.innerHeight * 0.9;
      if (window.scrollY > trigger && !ctaShown) {
        stickyCta.classList.add('show');
        ctaShown = true;
      } else if (window.scrollY <= trigger && ctaShown) {
        stickyCta.classList.remove('show');
        ctaShown = false;
      }
    };
    window.addEventListener('scroll', onCtaScroll, { passive: true });
    onCtaScroll();
    var stickyCtaClose = document.getElementById('stickyCtaClose');
    if (stickyCtaClose) {
      stickyCtaClose.addEventListener('click', function () {
        stickyCta.classList.remove('show');
        sessionStorage.setItem('stickyCtaDismissed', '1');
        window.removeEventListener('scroll', onCtaScroll);
      });
    }
  }
})();

/* =====================================================================
   Multi-page interactions: accordion, case filters, metric counters
   ===================================================================== */
(function () {
  'use strict';

  /* ---- Accordion (Services) ---- */
  var accItems = document.querySelectorAll('.acc-item');
  accItems.forEach(function (item) {
    var head = item.querySelector('.acc-head');
    var body = item.querySelector('.acc-body');
    if (!head || !body) return;
    head.setAttribute('aria-expanded', item.classList.contains('open') ? 'true' : 'false');
    if (item.classList.contains('open')) body.style.maxHeight = body.scrollHeight + 'px';
    head.addEventListener('click', function () {
      var isOpen = item.classList.toggle('open');
      head.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      body.style.maxHeight = isOpen ? body.scrollHeight + 'px' : null;
    });
  });
  // keep open panels sized correctly after resize
  window.addEventListener('resize', function () {
    document.querySelectorAll('.acc-item.open .acc-body').forEach(function (b) {
      b.style.maxHeight = b.scrollHeight + 'px';
    });
  });

  /* ---- Case study filters ---- */
  var filterBtns = document.querySelectorAll('.filter-btn');
  if (filterBtns.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.getAttribute('data-filter');
        filterBtns.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        document.querySelectorAll('.case').forEach(function (c) {
          var sectors = (c.getAttribute('data-sector') || '').split(' ');
          var show = (f === 'all') || sectors.indexOf(f) !== -1;
          c.classList.toggle('hide', !show);
        });
      });
    });
  }

  /* ---- Animated metric counters ---- */
  var figures = document.querySelectorAll('[data-count]');
  if (figures.length && 'IntersectionObserver' in window) {
    var animate = function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      var prefix = el.getAttribute('data-prefix') || '';
      var suffix = el.getAttribute('data-suffix') || '';
      var dur = 1400, start = null;
      var step = function (ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        var val = Math.round(target * eased);
        el.innerHTML = prefix + val.toLocaleString() + '<span class="unit">' + suffix + '</span>';
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    var cobs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animate(e.target); cobs.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    figures.forEach(function (f) { cobs.observe(f); });
  }
})();
