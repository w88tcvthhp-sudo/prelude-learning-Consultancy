/* =====================================================================
   The Capability Readiness Review(TM) — self-assessment scoring
   Runs entirely client-side. No data leaves the browser.
   ===================================================================== */
(function () {
  'use strict';
  var root = document.getElementById('crr');
  if (!root) return;

  var TOTAL = 10;
  var DIM = ["Problem definition", "Behaviour change", "Target impact", "Standards of 'good'",
    "Success measurement", "Evidence base", "Training vs capability", "Organisational barriers",
    "Risk of inaction", "Capability requirement"];
  var CAUSE = ["No agreed definition of the real problem", "Unclear which behaviours must change",
    "No defined target impact or outcome", "'Good' isn't defined or shared", "No agreed measures of success",
    "Decisions resting on assumption rather than evidence", "Defaulting to training before diagnosing the cause",
    "Structural or governance barriers left unaddressed", "Risk of inaction not understood or owned",
    "Required capability not yet defined"];

  var bar = document.getElementById('crr-bar');
  var count = document.getElementById('crr-count');
  var hint = document.getElementById('crr-hint');
  var result = document.getElementById('crr-result');

  function answered() {
    var n = 0;
    for (var i = 1; i <= TOTAL; i++) {
      if (document.querySelector('input[name="q' + i + '"]:checked')) n++;
    }
    return n;
  }

  root.addEventListener('change', function () {
    var n = answered();
    bar.style.width = (n / TOTAL * 100) + '%';
    count.textContent = n + ' of ' + TOTAL + ' answered';
    if (hint && n === TOTAL) hint.textContent = 'All answered — calculate your score.';
  });

  function li(items) { return items.map(function (t) { return '<li>' + t + '</li>'; }).join(''); }

  document.getElementById('crr-calc').addEventListener('click', function () {
    if (answered() < TOTAL) {
      if (hint) hint.textContent = 'Please answer all ten questions first.';
      return;
    }
    var total = 0, low = [];
    for (var i = 1; i <= TOTAL; i++) {
      var v = parseInt(document.querySelector('input[name="q' + i + '"]:checked').value, 10);
      total += v;
      if (v <= 1) low.push(i - 1);
    }
    var pct = Math.round(total / (TOTAL * 3) * 100);

    var band, text;
    if (pct >= 80) { band = "Strong readiness"; text = "You have real clarity on the problem and how to solve it. The priority now is execution and assurance — making sure the right capability is built and measured."; }
    else if (pct >= 60) { band = "Developing readiness"; text = "The foundations are there, but a few gaps could undermine your investment. Closing them before you commit will sharpen the outcome."; }
    else if (pct >= 40) { band = "At risk"; text = "There's enough uncertainty here that investing in a solution now carries real risk. A structured review would protect the spend and the outcome."; }
    else { band = "High risk — not yet ready"; text = "The real problem isn't yet defined clearly enough to solve. This is exactly where a Capability Readiness Review pays for itself."; }

    document.getElementById('crr-score').textContent = pct + '%';
    document.getElementById('crr-ring').style.setProperty('--p', pct);
    document.getElementById('crr-bandtitle').textContent = band;
    document.getElementById('crr-bandtext').textContent = text;

    var risks = low.map(function (idx) { return DIM[idx]; });
    var causes = low.map(function (idx) { return CAUSE[idx]; });

    var steps = [];
    if (low.indexOf(0) !== -1) steps.push("Define the single problem you're solving before commissioning any solution.");
    if (low.indexOf(6) !== -1) steps.push("Test whether training is genuinely the answer using the Training vs Capability Decision Model.");
    if (low.indexOf(4) !== -1 || low.indexOf(5) !== -1) steps.push("Agree how success will be measured, and gather a baseline, up front.");
    if (low.indexOf(7) !== -1) steps.push("Map the organisational barriers before designing any intervention.");
    if (low.indexOf(9) !== -1) steps.push("Define the capability actually required to achieve the outcome.");
    if (pct < 60) steps.unshift("Commission a full Capability Readiness Review to turn these gaps into an evidence-based plan.");
    if (!steps.length) steps.push("Move to design and assurance — you're ready to act with confidence.");
    steps = steps.slice(0, 4);
    steps.push("Discuss the findings in a short, no-obligation call.");

    if (!risks.length) { risks = ["No major gaps — strong across all ten dimensions."]; causes = ["Nothing significant flagged."]; }

    document.getElementById('crr-risks').innerHTML = li(risks);
    document.getElementById('crr-causes').innerHTML = li(causes);
    document.getElementById('crr-steps').innerHTML = li(steps);

    result.classList.add('show');
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  document.getElementById('crr-print').addEventListener('click', function () { window.print(); });
})();
