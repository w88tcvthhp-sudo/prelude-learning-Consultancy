<?php
/** Toolkit access form handler. Stores the request, grants access, redirects, then emails. */
declare(strict_types=1);
require __DIR__ . '/lib/toolkit.php';

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    tk_redirect('/book-toolkit/');
}
// Honeypot: real people never fill this hidden field.
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    tk_redirect('/book-toolkit/');
}

$first = tk_clean((string) ($_POST['first_name'] ?? ''), 80);
$email = tk_clean((string) ($_POST['email'] ?? ''), 200);
$org   = tk_clean((string) ($_POST['organisation'] ?? ''), 160);
$role  = tk_clean((string) ($_POST['role'] ?? ''), 160);
$optIn = (($_POST['updates'] ?? '') === 'yes');   // unchecked by default; never required

$errors = [];
if ($first === '') { $errors[] = 'first_name'; }
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) { $errors[] = 'email'; }
if ($errors) {
    tk_redirect('/book-toolkit/?error=' . implode(',', $errors) . '#toolkitForm');
}
if (tk_rate_limited()) {
    tk_redirect('/book-toolkit/?error=rate#toolkitForm');
}

$token = tk_make_token();
$accessId = explode('.', $token)[0];
$now = gmdate('c');

$stored = tk_append_csv('toolkit-requests.csv',
    ['received_utc', 'access_id', 'first_name', 'email', 'organisation', 'role', 'updates_opt_in'],
    [$now, $accessId, $first, $email, $org, $role, $optIn ? 'yes' : 'no']);
if (!$stored) {
    tk_redirect('/book-toolkit/?error=server#toolkitForm');
}
// Marketing consent is recorded separately, with the exact wording shown, only when given.
if ($optIn) {
    tk_append_csv('marketing-consent.csv',
        ['consented_utc', 'email', 'first_name', 'source', 'consent_wording', 'wording_version'],
        [$now, $email, $first, 'book-toolkit form', TK_CONSENT_TEXT, TK_CONSENT_VERSION]);
}

tk_set_cookie($token);
header('Location: /book-toolkit/downloads/', true, 303);

// Let the browser move on immediately, then send the email.
if (function_exists('fastcgi_finish_request')) {
    fastcgi_finish_request();
} else {
    ignore_user_abort(true);
    header('Content-Length: 0');
    header('Connection: close');
    @ob_end_flush();
    flush();
}
if (!tk_send_access_email($email, $first, $token)) {
    tk_append_csv('email-failures.csv', ['utc', 'access_id', 'email'], [gmdate('c'), $accessId, $email]);
}
