<?php
/** Serves toolkit files from the private folder. No filesystem paths are exposed. */
declare(strict_types=1);
require __DIR__ . '/lib/toolkit.php';

if (!tk_has_access()) {
    tk_redirect('/book-toolkit/?access=required');
}
$id = (string) ($_GET['f'] ?? '');
if (!preg_match('/^[a-z0-9-]{3,60}$/', $id)) {
    tk_fail_page(404, 'That file could not be found.');
}
$item = null;
foreach (tk_manifest() as $m) {
    if (($m['id'] ?? '') === $id) { $item = $m; break; }
}
if (!$item) {
    tk_fail_page(404, 'That file could not be found.');
}
// Stored under the original file name from the toolkit pack; basename() blocks path traversal.
$file = basename((string) ($item['file'] ?? ($item['id'] . '.' . $item['ext'])));
$path = tk_private_dir() . '/toolkit/' . $file;
if (!is_file($path) || !is_readable($path)) {
    error_log('Prelude toolkit: missing file ' . $file);
    tk_fail_page(404, 'This file is being prepared and is not available yet. Please email jason.smith@prelude-learning.com and we will send it to you directly.');
}
$name = preg_replace('/[^A-Za-z0-9._-]/', '-', (string) $item['download_name']);
header('Content-Type: ' . tk_mime((string) $item['ext']));
header('Content-Disposition: attachment; filename="' . $name . '"; filename*=UTF-8\'\'' . rawurlencode($name));
header('Content-Length: ' . (string) filesize($path));
header('X-Content-Type-Options: nosniff');
header('X-Robots-Tag: noindex');
header('Cache-Control: private, max-age=0');
readfile($path);
