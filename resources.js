/* Free resources: email-gated PDF download (Formspree, no backend required).
   Without JavaScript the "Get free PDF" buttons are hidden and the email-delivery
   form on the page is used instead. */
(function () {
  'use strict';
  var dialog = document.getElementById('resourceDialog');
  var form = document.getElementById('resourceForm');
  if (!dialog || !form || typeof dialog.showModal !== 'function') return;
  var email = document.getElementById('res-email');
  var emailErr = document.getElementById('res-email-err');
  var errors = document.getElementById('resErrors');
  var body = document.getElementById('resBody');
  var done = document.getElementById('resDone');
  var nameEl = document.getElementById('resName');
  var field = document.getElementById('resField');
  var dl = document.getElementById('resDownload');
  var submit = document.getElementById('resSubmit');
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var trigger = null, current = null;
  var KEY = 'prelude-resource-access';

  function track(name, data) { if (window.preludeTrack) window.preludeTrack(name, data || {}); }
  function remembered() { try { return sessionStorage.getItem(KEY) === '1'; } catch (e) { return false; } }
  function remember() { try { sessionStorage.setItem(KEY, '1'); } catch (e) { /* storage unavailable */ } }

  function showDone() {
    body.hidden = true; done.hidden = false;
    dl.href = current.file;
    dl.setAttribute('data-file', current.id);
    done.focus();
  }
  function reset() {
    body.hidden = false; done.hidden = true; errors.hidden = true; errors.innerHTML = '';
    email.setAttribute('aria-invalid', 'false'); emailErr.hidden = true; emailErr.textContent = '';
    submit.disabled = false;
  }
  function open(btn) {
    trigger = btn;
    current = { id: btn.getAttribute('data-resource'), file: btn.getAttribute('data-file'), title: btn.getAttribute('data-title') };
    field.value = current.id;
    nameEl.innerHTML = current.title;
    reset();
    dialog.showModal();
    if (remembered()) { showDone(); } else { email.focus(); }
    track('resource_request_open', { resource: current.id });
  }

  document.querySelectorAll('.r-get').forEach(function (btn) {
    btn.addEventListener('click', function (e) { e.preventDefault(); open(btn); });
  });
  document.getElementById('resClose').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener('close', function () { if (trigger) trigger.focus(); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!EMAIL.test(email.value.trim())) {
      email.setAttribute('aria-invalid', 'true');
      emailErr.textContent = 'Enter an email address in the format name@example.com';
      emailErr.hidden = false; email.focus();
      return;
    }
    email.setAttribute('aria-invalid', 'false'); emailErr.hidden = true;
    submit.disabled = true;
    var data = new FormData(form);
    if (!document.getElementById('res-updates').checked) data.set('updates', 'no');
    fetch(form.action, { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r; })
      .then(function () {
        remember();
        track('resource_request_submit', { resource: current.id, updates: data.get('updates') });
        showDone();
      })
      .catch(function () {
        submit.disabled = false;
        errors.innerHTML = '<strong>Sorry, that didn&rsquo;t go through.</strong> Please try again, or email ' +
          '<a href="mailto:jason.smith@prelude-learning.com">jason.smith@prelude-learning.com</a> and we will send the resource directly.';
        errors.hidden = false;
        errors.setAttribute('tabindex', '-1'); errors.focus();
      });
  });
})();
