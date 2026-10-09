// GET /api/toolkit-download?f=<id>
// Streams one toolkit file from the private Vercel Blob store, only to readers with a valid
// access cookie. Files are stored under toolkit/<original file name> (see README-TOOLKIT.md).
import { get } from '@vercel/blob';
import { config, hasAccess, redirect, safeFilename, CONTENT_TYPES, FORM_PATH } from './_lib/toolkit.js';
import { MANIFEST } from './_lib/toolkit-manifest.js';

function failPage(status, message) {
  const html = `<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Toolkit | Prelude Learning &amp; Consultancy</title><link rel="stylesheet" href="/styles.css"></head>
<body><main id="main" class="sec"><div class="wrap narrow"><h1 class="section-title">Sorry about this</h1><p>${message}</p>
<p><a class="text-link" href="/book-toolkit/downloads/">Back to the downloads</a></p></div></main></body></html>`;
  return new Response(html, { status, headers: { 'Content-Type': 'text/html; charset=utf-8', 'X-Robots-Tag': 'noindex', 'Cache-Control': 'no-store' } });
}

export async function GET(request) {
  if (!hasAccess(request, config())) return redirect(`${FORM_PATH}?access=required#toolkitForm`);

  const id = new URL(request.url).searchParams.get('f') || '';
  const item = /^[a-z0-9-]{3,60}$/.test(id) ? MANIFEST.find(m => m.id === id) : null;
  if (!item) return failPage(404, 'That file could not be found.');

  let result;
  try {
    result = await get(`toolkit/${item.file}`, { access: 'private' });
  } catch (err) {
    console.error('toolkit: blob read failed for', item.file, err?.message);
    result = null;
  }
  if (!result || result.statusCode !== 200 || !result.stream) {
    console.error('toolkit: missing file', item.file);
    return failPage(404, 'This file is not available at the moment. Please email jason.smith@prelude-learning.com and we will send it to you directly.');
  }

  const name = safeFilename(item.download_name);
  return new Response(result.stream, {
    headers: {
      'Content-Type': CONTENT_TYPES[item.ext] || result.blob.contentType || 'application/octet-stream',
      'Content-Disposition': `attachment; filename="${name}"; filename*=UTF-8''${encodeURIComponent(name)}`,
      'X-Content-Type-Options': 'nosniff',
      'X-Robots-Tag': 'noindex',
      'Cache-Control': 'private, no-store',
    },
  });
}
