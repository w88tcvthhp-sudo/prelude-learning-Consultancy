/* Toolkit access form: accessible client-side validation and server error display.
   The server (/api/toolkit-access) re-validates everything and checks the access code. */
(function () {
  'use strict';
  var form = document.getElementById('toolkitForm');
  if (!form) return;
  var summary = document.getElementById('tkErrors');
  var fields = {
    first_name: { el: document.getElementById('tk-first'), err: document.getElementById('tk-first-err'), msg: 'Enter your first name' },
    email: { el: document.getElementById('tk-email'), err: document.getElementById('tk-email-err'), msg: 'Enter an email address in the format name@example.com' },
    code: { el: document.getElementById('tk-code'), err: document.getElementById('tk-code-err'), msg: 'Enter the access code printed in the book' }
  };
  var CODE_WRONG = 'That access code wasn’t recognised. Check the code on the first page of The Toolkit, at the back of the book, and try again.';
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function setError(key, show, msg) {
    var f = fields[key];
    f.el.setAttribute('aria-invalid', show ? 'true' : 'false');
    f.err.hidden = !show;
    f.err.textContent = show ? (msg || f.msg) : '';
  }
  function showSummary(items) {
    if (!items.length) { summary.hidden = true; summary.innerHTML = ''; return; }
    summary.innerHTML = '<strong>There is a problem</strong><ul>' + items.map(function (it) {
      return '<li><a href="#' + fields[it.key].el.id + '">' + it.msg + '</a></li>';
    }).join('') + '</ul>';
    summary.hidden = false;
    summary.setAttribute('tabindex', '-1');
    summary.focus();
  }
  function validate() {
    var bad = [];
    if (!fields.first_name.el.value.trim()) bad.push('first_name');
    if (!EMAIL.test(fields.email.el.value.trim())) bad.push('email');
    if (!fields.code.el.value.replace(/[^A-Za-z0-9]/g, '')) bad.push('code');
    Object.keys(fields).forEach(function (k) { setError(k, bad.indexOf(k) !== -1); });
    return bad.map(function (k) { return { key: k, msg: fields[k].msg }; });
  }
  form.addEventListener('submit', function (e) {
    var bad = validate();
    if (bad.length) { e.preventDefault(); showSummary(bad); return; }
    if (window.preludeTrack) window.preludeTrack('toolkit_form_submit', { updates: form.updates.checked ? 'yes' : 'no' });
  });

  /* errors returned by the server: /book-toolkit/?error=first_name,email,code or ?error=server */
  var params = new URLSearchParams(location.search);
  var p = params.get('error');
  if (p) {
    if (p === 'server') {
      summary.innerHTML = '<strong>Sorry, something went wrong.</strong> Please try again, or email jason.smith@prelude-learning.com and we will send you the toolkit directly.';
      summary.hidden = false;
    } else {
      var items = p.split(',').filter(function (k) { return fields[k]; }).map(function (k) {
        var msg = k === 'code' ? CODE_WRONG : fields[k].msg;
        setError(k, true, msg);
        return { key: k, msg: msg };
      });
      showSummary(items);
    }
  }
  if (params.get('access') === 'required') {
    summary.innerHTML = '<strong>Please enter the access code from the book.</strong> Your access has expired or this browser hasn’t been used for the toolkit before. Enter your details and the code, and the downloads page will open straight away.';
    summary.hidden = false;
  }
})();
