// POST /api/toolkit-access
// Checks the reader's details and the access code printed in the book, records the request,
// sets the 12-month access cookie and sends the reader to the downloads page.
import {
  config, codeMatches, makeToken, accessCookie, redirect, clean, validate,
  recordRequest, FORM_PATH, DOWNLOADS_PATH,
} from './_lib/toolkit.js';

const back = query => redirect(`${FORM_PATH}?${query}#toolkitForm`);

export async function POST(request) {
  let form;
  try { form = await request.formData(); } catch { return back('error=server'); }

  // Honeypot: people never fill this hidden field.
  if (clean(form.get('website'), 200)) return redirect(FORM_PATH);

  const fields = {
    first_name: clean(form.get('first_name'), 80),
    email: clean(form.get('email'), 200),
    organisation: clean(form.get('organisation'), 160),
    role: clean(form.get('role'), 160),
    code: clean(form.get('access_code'), 60),
    updates: form.get('updates') === 'yes' ? 'yes' : 'no',
  };

  const errors = validate(fields);
  if (errors.length) return back('error=' + errors.join(','));

  const cfg = config();
  if (!cfg.ready) {
    console.error('toolkit: TOOLKIT_ACCESS_CODES or TOOLKIT_SECRET is not configured');
    return back('error=server');
  }

  if (!codeMatches(fields.code, cfg.codes)) {
    await new Promise(r => setTimeout(r, 800)); // slows repeated guessing
    return back('error=code');
  }

  await recordRequest(fields, cfg);
  return redirect(DOWNLOADS_PATH, { 'Set-Cookie': accessCookie(makeToken(cfg.secret)) });
}

export function GET() {
  return redirect(FORM_PATH);
}
