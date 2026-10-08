/* Toolkit access form: accessible client-side validation and server error display.
   The server (book-toolkit/submit.php) re-validates everything. */
(function () {
  'use strict';
  var form = document.getElementById('toolkitForm');
  if (!form) return;
  var summary = document.getElementById('tkErrors');
  var fields = {
    first_name: { el: document.getElementById('tk-first'), err: document.getElementById('tk-first-err'), msg: 'Enter your first name' },
    email: { el: document.getElementById('tk-email'), err: document.getElementById('tk-email-err'), msg: 'Enter an email address in the format name@example.com' }
  };
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function setError(key, show) {
    var f = fields[key];
    f.el.setAttribute('aria-invalid', show ? 'true' : 'false');
    f.err.hidden = !show;
    f.err.textContent = show ? f.msg : '';
  }
  function showSummary(keys) {
    if (!keys.length) { summary.hidden = true; summary.innerHTML = ''; return; }
    summary.innerHTML = '<strong>There is a problem</strong><ul>' + keys.map(function (k) {
      return '<li><a href="#' + fields[k].el.id + '">' + fields[k].msg + '</a></li>';
    }).join('') + '</ul>';
    summary.hidden = false;
    summary.focus && summary.setAttribute('tabindex', '-1');
    summary.focus();
  }
  function validate() {
    var bad = [];
    if (!fields.first_name.el.value.trim()) bad.push('first_name');
    if (!EMAIL.test(fields.email.el.value.trim())) bad.push('email');
    Object.keys(fields).forEach(function (k) { setError(k, bad.indexOf(k) !== -1); });
    return bad;
  }
  form.addEventListener('submit', function (e) {
    var bad = validate();
    if (bad.length) { e.preventDefault(); showSummary(bad); return; }
    if (window.preludeTrack) window.preludeTrack('toolkit_form_submit', { updates: form.updates.checked ? 'yes' : 'no' });
  });
  /* errors returned by the server: /book-toolkit/?error=first_name,email or ?error=server */
  var p = new URLSearchParams(location.search).get('error');
  if (p) {
    if (p === 'server' || p === 'rate') {
      summary.innerHTML = p === 'rate'
        ? '<strong>Too many requests.</strong> Please wait a few minutes and try again.'
        : '<strong>Sorry, something went wrong.</strong> Please try again, or email jason.smith@prelude-learning.com and we will send you the toolkit directly.';
      summary.hidden = false;
    } else {
      var keys = p.split(',').filter(function (k) { return fields[k]; });
      keys.forEach(function (k) { setError(k, true); });
      showSummary(keys);
    }
  }
  if (new URLSearchParams(location.search).get('access') === 'required') {
    summary.innerHTML = '<strong>Your access link has expired or wasn&rsquo;t recognised.</strong> Enter your details again and the downloads page will open straight away.';
    summary.hidden = false;
  }
})();
