// Book companion toolkit: shared logic for the access and download functions.
// Files in api/_lib are not deployed as functions (underscore prefix).
//
// Configuration (Vercel > Project > Settings > Environment Variables). Never commit these.
//   TOOLKIT_ACCESS_CODES   one or more access codes printed in the book, comma-separated
//                          (case, spaces and hyphens are ignored when comparing)
//   TOOLKIT_SECRET         at least 32 random characters; signs the access cookie.
//                          Changing it signs everyone out (they re-enter the code).
//   TOOLKIT_RECORD_ENDPOINT optional; where access requests are recorded.
//                          Defaults to the site's existing Formspree form.
import crypto from 'node:crypto';

export const COOKIE = 'prelude_toolkit';
export const TTL_SECONDS = 365 * 24 * 60 * 60; // 12 months
export const FORM_PATH = '/book-toolkit/';
export const DOWNLOADS_PATH = '/book-toolkit/downloads/';
export const CONSENT_TEXT = "I'd also like occasional practical updates, tools and insights from Prelude Learning & Consultancy.";
export const CONSENT_VERSION = '2026-10-08';
const DEFAULT_RECORD_ENDPOINT = 'https://formspree.io/f/xeeyazed';
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export function config(env = process.env) {
  const codes = String(env.TOOLKIT_ACCESS_CODES || '')
    .split(',').map(normaliseCode).filter(c => c.length >= 6);
  const secret = String(env.TOOLKIT_SECRET || '');
  return {
    codes,
    secret,
    recordEndpoint: env.TOOLKIT_RECORD_ENDPOINT || DEFAULT_RECORD_ENDPOINT,
    ready: codes.length > 0 && secret.length >= 32,
  };
}

export function normaliseCode(value) {
  return String(value || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
}

const sha256 = v => crypto.createHash('sha256').update(v).digest();

/** Constant-time comparison against every configured code. */
export function codeMatches(input, codes) {
  const given = sha256(normaliseCode(input));
  let ok = false;
  for (const code of codes) {
    if (crypto.timingSafeEqual(given, sha256(code))) ok = true;
  }
  return ok && normaliseCode(input).length > 0;
}

const hmac = (data, secret) => crypto.createHmac('sha256', secret).update(data).digest('hex');

export function makeToken(secret, now = Date.now()) {
  const id = crypto.randomBytes(16).toString('hex');
  const exp = Math.floor(now / 1000) + TTL_SECONDS;
  return `${id}.${exp}.${hmac(`${id}.${exp}`, secret)}`;
}

export function tokenValid(token, secret, now = Date.now()) {
  if (typeof token !== 'string' || !/^[a-f0-9]{32}\.\d{9,11}\.[a-f0-9]{64}$/.test(token)) return false;
  const [id, exp, sig] = token.split('.');
  if (Number(exp) < Math.floor(now / 1000)) return false;
  const expected = Buffer.from(hmac(`${id}.${exp}`, secret), 'hex');
  const given = Buffer.from(sig, 'hex');
  return expected.length === given.length && crypto.timingSafeEqual(expected, given);
}

export function readCookie(request, name = COOKIE) {
  const header = request.headers.get('cookie') || '';
  for (const part of header.split(';')) {
    const i = part.indexOf('=');
    if (i > -1 && part.slice(0, i).trim() === name) return decodeURIComponent(part.slice(i + 1).trim());
  }
  return null;
}

export function accessCookie(token) {
  return `${COOKIE}=${token}; Path=/; Max-Age=${TTL_SECONDS}; HttpOnly; Secure; SameSite=Lax`;
}

export function hasAccess(request, cfg = config()) {
  return cfg.secret.length >= 32 && tokenValid(readCookie(request), cfg.secret);
}

export function redirect(location, extraHeaders = {}) {
  return new Response(null, { status: 303, headers: { Location: location, 'Cache-Control': 'no-store', ...extraHeaders } });
}

/** Trims, strips control characters and limits length. */
export function clean(value, max) {
  return String(value ?? '').replace(/[\u0000-\u001F\u007F]+/g, ' ').trim().slice(0, max);
}

export function validate(fields) {
  const errors = [];
  if (!fields.first_name) errors.push('first_name');
  if (!EMAIL.test(fields.email)) errors.push('email');
  if (!normaliseCode(fields.code)) errors.push('code');
  return errors;
}

/** Records the request (and any opt-in, with its wording) without blocking access if it fails. */
export async function recordRequest(fields, cfg = config(), fetchImpl = fetch) {
  const optIn = fields.updates === 'yes';
  const body = {
    _subject: 'Prelude website: book toolkit access',
    source: 'book-toolkit',
    first_name: fields.first_name,
    email: fields.email,
    organisation: fields.organisation,
    role: fields.role,
    updates_opt_in: optIn ? 'yes' : 'no',
    consent_wording: optIn ? CONSENT_TEXT : '',
    consent_version: optIn ? CONSENT_VERSION : '',
    received_utc: new Date().toISOString(),
  };
  try {
    const res = await fetchImpl(cfg.recordEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(4000),
    });
    if (!res.ok) console.error('toolkit: record endpoint returned', res.status);
    return res.ok;
  } catch (err) {
    console.error('toolkit: could not record request', err?.message);
    return false;
  }
}

export function safeFilename(name) {
  return String(name).replace(/[^A-Za-z0-9._-]/g, '-');
}

export const CONTENT_TYPES = {
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  pdf: 'application/pdf',
  xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  zip: 'application/zip',
};
