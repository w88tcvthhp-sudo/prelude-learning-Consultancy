<?php
/**
 * Training Isn't Always the Answer — reader toolkit access.
 *
 * Flow: form (book-toolkit/index.html) -> submit.php stores the request privately,
 * sets an access cookie and redirects straight to /book-toolkit/downloads/, then
 * sends one access email with a link back to the downloads page.
 * Files are served by download.php from a private folder outside public_html.
 *
 * Requires PHP 7.4+. No database. No third-party form service.
 * Configuration: see README-TOOLKIT.md. Never commit real secrets.
 */

declare(strict_types=1);

const TK_COOKIE = 'prelude_toolkit';
const TK_COOKIE_PATH = '/book-toolkit/';
const TK_TTL = 31536000;          // 12 months
const TK_SITE = 'https://www.prelude-learning.com';
const TK_CONSENT_TEXT = "I'd also like occasional practical updates, tools and insights from Prelude Learning & Consultancy.";
const TK_CONSENT_VERSION = '2026-10-08';

/** Private directory, outside the web root. Defaults to ~/prelude-private beside public_html. */
function tk_private_dir(): string {
    $dir = getenv('PRELUDE_PRIVATE_DIR');
    if (!$dir) {
        $root = rtrim($_SERVER['DOCUMENT_ROOT'] ?? dirname(__DIR__, 2), '/');
        $dir = dirname($root) . '/prelude-private';
    }
    return rtrim($dir, '/');
}

/** Settings: environment variables first, then prelude-private/config.php. */
function tk_config(string $key, string $default = ''): string {
    static $file = null;
    $map = [
        'secret' => 'PRELUDE_TOOLKIT_SECRET',
        'mail_from' => 'PRELUDE_MAIL_FROM',
        'mail_from_name' => 'PRELUDE_MAIL_FROM_NAME',
        'reply_to' => 'PRELUDE_MAIL_REPLY_TO',
        'resend_api_key' => 'RESEND_API_KEY',
    ];
    $env = isset($map[$key]) ? getenv($map[$key]) : false;
    if ($env !== false && $env !== '') {
        return (string) $env;
    }
    if ($file === null) {
        $path = tk_private_dir() . '/config.php';
        $file = is_readable($path) ? (array) (include $path) : [];
    }
    return isset($file[$key]) ? (string) $file[$key] : $default;
}

function tk_secret(): string {
    $s = tk_config('secret');
    if (strlen($s) < 32) {
        error_log('Prelude toolkit: secret missing or shorter than 32 characters.');
        tk_fail_page(500, 'The toolkit is not configured yet. Please email jason.smith@prelude-learning.com and we will send it to you directly.');
    }
    return $s;
}

/* ------------------------------------------------------------- tokens */

function tk_make_token(): string {
    $id = bin2hex(random_bytes(16));
    $exp = (string) (time() + TK_TTL);
    $sig = hash_hmac('sha256', $id . '.' . $exp, tk_secret());
    return $id . '.' . $exp . '.' . $sig;
}

function tk_token_valid(?string $token): bool {
    if (!is_string($token) || !preg_match('/^[a-f0-9]{32}\.\d{9,11}\.[a-f0-9]{64}$/', $token)) {
        return false;
    }
    [$id, $exp, $sig] = explode('.', $token);
    if ((int) $exp < time()) {
        return false;
    }
    return hash_equals(hash_hmac('sha256', $id . '.' . $exp, tk_secret()), $sig);
}

function tk_set_cookie(string $token): void {
    $exp = (int) explode('.', $token)[1];
    setcookie(TK_COOKIE, $token, [
        'expires' => $exp, 'path' => TK_COOKIE_PATH, 'secure' => true,
        'httponly' => true, 'samesite' => 'Lax',
    ]);
    $_COOKIE[TK_COOKIE] = $token;
}

function tk_has_access(): bool {
    return tk_token_valid($_COOKIE[TK_COOKIE] ?? null);
}

/** Gate for the downloads page. A ?t= link from the email sets the cookie, then the URL is cleaned. */
function toolkit_require_access(): void {
    if (isset($_GET['t'])) {
        if (tk_token_valid((string) $_GET['t'])) {
            tk_set_cookie((string) $_GET['t']);
            tk_redirect('/book-toolkit/downloads/');
        }
        tk_redirect('/book-toolkit/?access=required');
    }
    if (!tk_has_access()) {
        tk_redirect('/book-toolkit/?access=required');
    }
    header('X-Robots-Tag: noindex, nofollow');
    header('Cache-Control: private, no-store');
    header('Referrer-Policy: same-origin');
}

/* ------------------------------------------------------------- helpers */

function tk_redirect(string $path): void {
    header('Location: ' . $path, true, 303);
    exit;
}

function tk_fail_page(int $code, string $message): void {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    header('X-Robots-Tag: noindex');
    $m = htmlspecialchars($message, ENT_QUOTES, 'UTF-8');
    echo '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        . '<title>Toolkit | Prelude</title><link rel="stylesheet" href="/styles.css"></head><body>'
        . '<main id="main" class="sec"><div class="wrap narrow"><h1 class="section-title">Sorry about this</h1>'
        . '<p>' . $m . '</p><p><a class="text-link" href="/book-toolkit/downloads/">Back to the downloads</a></p></div></main></body></html>';
    exit;
}

/** Plain-text cleaning plus spreadsheet formula-injection guard for CSV storage. */
function tk_clean(string $v, int $max): string {
    $v = trim(preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $v) ?? '');
    $v = function_exists('mb_substr') ? mb_substr($v, 0, $max) : substr($v, 0, $max);
    return $v;
}
function tk_csv_safe(string $v): string {
    return ($v !== '' && strpos('=+-@', $v[0]) !== false) ? "'" . $v : $v;
}

function tk_append_csv(string $file, array $header, array $row): bool {
    $dir = tk_private_dir() . '/data';
    if (!is_dir($dir) && !@mkdir($dir, 0700, true)) {
        error_log('Prelude toolkit: cannot create ' . $dir);
        return false;
    }
    $path = $dir . '/' . $file;
    $new = !file_exists($path);
    $fh = @fopen($path, 'ab');
    if (!$fh) {
        error_log('Prelude toolkit: cannot open ' . $path);
        return false;
    }
    flock($fh, LOCK_EX);
    if ($new) {
        fputcsv($fh, $header);
    }
    fputcsv($fh, array_map('tk_csv_safe', $row));
    fflush($fh);
    flock($fh, LOCK_UN);
    fclose($fh);
    @chmod($path, 0600);
    return true;
}

/** Simple abuse limit: 8 submissions per hour per (hashed) address. Nothing identifiable is kept. */
function tk_rate_limited(): bool {
    $dir = tk_private_dir() . '/data';
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    $key = hash_hmac('sha256', (string) ($_SERVER['REMOTE_ADDR'] ?? ''), tk_secret());
    $path = $dir . '/ratelimit.json';
    $fh = @fopen($path, 'c+');
    if (!$fh) {
        return false;
    }
    flock($fh, LOCK_EX);
    $data = json_decode((string) stream_get_contents($fh), true) ?: [];
    $now = time();
    foreach ($data as $k => $times) {
        $data[$k] = array_values(array_filter((array) $times, function ($t) use ($now) { return $t > $now - 3600; }));
        if (!$data[$k]) unset($data[$k]);
    }
    $limited = count($data[$key] ?? []) >= 8;
    if (!$limited) {
        $data[$key][] = $now;
    }
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($data));
    flock($fh, LOCK_UN);
    fclose($fh);
    return $limited;
}

/* ------------------------------------------------------------- email */

function tk_send_access_email(string $to, string $firstName, string $token): bool {
    $link = TK_SITE . '/book-toolkit/downloads/?t=' . rawurlencode($token);
    $name = $firstName !== '' ? $firstName : 'there';
    $subject = 'Your Training Isn’t Always the Answer Toolkit';
    $text = "Hi {$name},\n\n"
        . "Thanks for reading Training Isn’t Always the Answer.\n\n"
        . "Your editable toolkit is ready here:\n{$link}\n\n"
        . "It includes all 18 tools from the book, plus the One-Day TNA, Five-Day Rapid TNA Workbook and Full TNA Report Template.\n\n"
        . "Jason\nPrelude Learning & Consultancy\n";
    $h = function ($s) { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); };
    $html = '<p>Hi ' . $h($name) . ',</p><p>Thanks for reading <em>Training Isn’t Always the Answer</em>.</p>'
        . '<p>Your editable toolkit is ready here:</p><p><a href="' . $h($link) . '" style="display:inline-block;padding:12px 20px;background:#0E7A5A;color:#ffffff;text-decoration:none;border-radius:4px">Download toolkit</a></p>'
        . '<p>It includes all 18 tools from the book, plus the One-Day TNA, Five-Day Rapid TNA Workbook and Full TNA Report Template.</p>'
        . '<p>Jason<br>Prelude Learning &amp; Consultancy</p>';

    $from = tk_config('mail_from', 'jason.smith@prelude-learning.com');
    $fromName = tk_config('mail_from_name', 'Jason Smith, Prelude');
    $replyTo = tk_config('reply_to', $from);

    $apiKey = tk_config('resend_api_key');
    if ($apiKey !== '' && function_exists('curl_init')) {
        $ch = curl_init('https://api.resend.com/emails');
        curl_setopt_array($ch, [
            CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 10,
            CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $apiKey, 'Content-Type: application/json'],
            CURLOPT_POSTFIELDS => json_encode([
                'from' => "{$fromName} <{$from}>", 'to' => [$to], 'reply_to' => $replyTo,
                'subject' => $subject, 'text' => $text, 'html' => $html,
            ]),
        ]);
        $body = curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        if ($code >= 200 && $code < 300) {
            return true;
        }
        error_log('Prelude toolkit: Resend failed (' . $code . '): ' . substr((string) $body, 0, 300));
        return false;
    }

    // Fallback: the host's mail(). Works on GoDaddy cPanel, but deliverability depends on SPF/DKIM.
    $headers = [
        'From: =?UTF-8?B?' . base64_encode($fromName) . "?= <{$from}>",
        'Reply-To: ' . $replyTo,
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
    ];
    $ok = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $text, implode("\r\n", $headers), '-f' . $from);
    if (!$ok) {
        error_log('Prelude toolkit: mail() returned false for access email.');
    }
    return $ok;
}

/* ------------------------------------------------------------- files */

function tk_manifest(): array {
    static $m = null;
    if ($m === null) {
        $m = json_decode((string) @file_get_contents(__DIR__ . '/manifest.json'), true) ?: [];
    }
    return $m;
}

function tk_mime(string $ext): string {
    $types = [
        'docx' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xlsx' => 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'pptx' => 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'pdf' => 'application/pdf',
        'zip' => 'application/zip',
    ];
    return $types[strtolower($ext)] ?? 'application/octet-stream';
}
