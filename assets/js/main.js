/* Ride Rescue — page behavior */
(function () {
  'use strict';

  // Replace YOUR_FORM_ID with the ID from your Formspree form (formspree.io).
  // The same URL is set as the form's `action` in index.html so the form
  // still works if JavaScript fails to load.
  var FORM_ENDPOINT = 'https://formspree.io/f/YOUR_FORM_ID';

  /* ---------- Footer year ---------- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ---------- Mobile nav ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  function setNav(open) {
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setNav(false);
        toggle.focus();
      }
    });
  }

  /* ---------- Booking form ---------- */
  var form = document.getElementById('booking-form');
  if (!form) return;

  var zipField = document.getElementById('zip-field');
  var zipInput = document.getElementById('zip');
  var statusEl = document.getElementById('form-status');
  var submitBtn = form.querySelector('button[type="submit"]');

  function deliveryValue() {
    var checked = form.querySelector('input[name="delivery"]:checked');
    return checked ? checked.value : 'remote';
  }

  function syncZip() {
    var needsZip = deliveryValue() === 'onsite';
    zipField.hidden = !needsZip;
    zipInput.required = needsZip;
    if (!needsZip) clearError(zipInput);
  }

  form.addEventListener('change', function (e) {
    if (e.target.name === 'delivery') syncZip();
  });

  // "Book remote" / "Book on-site" buttons preselect the delivery option.
  document.querySelectorAll('[data-delivery]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var radio = form.querySelector('input[name="delivery"][value="' + btn.dataset.delivery + '"]');
      if (radio) {
        radio.checked = true;
        syncZip();
      }
    });
  });

  syncZip();

  /* Validation */
  var VIN_RE = /^[A-HJ-NPR-Z0-9]{17}$/; // 17 chars, no I, O or Q
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var ZIP_RE = /^\d{5}(-\d{4})?$/;

  function errorEl(input) {
    return document.getElementById(input.id + '-error');
  }

  function setError(input, msg) {
    input.setAttribute('aria-invalid', 'true');
    var el = errorEl(input);
    if (el) el.textContent = msg;
  }

  function clearError(input) {
    input.removeAttribute('aria-invalid');
    var el = errorEl(input);
    if (el) el.textContent = '';
  }

  function validateField(input) {
    var v = input.value.trim();
    clearError(input);

    if (input.required && !v) {
      setError(input, 'This field is required.');
      return false;
    }
    if (!v) return true;

    switch (input.id) {
      case 'email':
        if (!EMAIL_RE.test(v)) { setError(input, 'Enter a valid email address.'); return false; }
        break;
      case 'phone':
        if (v.replace(/\D/g, '').length < 10) { setError(input, 'Enter a 10-digit phone number.'); return false; }
        break;
      case 'year':
        var y = Number(v);
        var max = new Date().getFullYear() + 1;
        if (!/^\d{4}$/.test(v) || y < 1990 || y > max) { setError(input, 'Enter a 4-digit year between 1990 and ' + max + '.'); return false; }
        break;
      case 'vin':
        input.value = v.toUpperCase();
        if (!VIN_RE.test(input.value)) { setError(input, 'A VIN is 17 letters and numbers and never contains I, O or Q.'); return false; }
        break;
      case 'zip':
        if (!ZIP_RE.test(v)) { setError(input, 'Enter a 5-digit ZIP code.'); return false; }
        break;
    }
    return true;
  }

  var validated = form.querySelectorAll('input[id]:not([type="radio"]):not(#company), select[required], textarea[required]');

  validated.forEach(function (input) {
    input.addEventListener('blur', function () {
      if (input.value.trim() || input.getAttribute('aria-invalid')) validateField(input);
    });
    input.addEventListener('input', function () {
      if (input.getAttribute('aria-invalid')) validateField(input);
    });
  });

  function setStatus(msg, kind) {
    statusEl.textContent = msg;
    statusEl.className = 'form-status' + (kind ? ' is-' + kind : '');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    setStatus('', null);

    var firstInvalid = null;
    validated.forEach(function (input) {
      if (input.closest('[hidden]')) return;
      if (!validateField(input) && !firstInvalid) firstInvalid = input;
    });

    if (firstInvalid) {
      setStatus('Please fix the highlighted fields.', 'error');
      firstInvalid.focus();
      return;
    }

    // Honeypot: bots fill hidden fields. Pretend success, send nothing.
    if (document.getElementById('company').value) {
      showSuccess();
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending…';

    fetch(FORM_ENDPOINT, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    })
      .then(function (res) {
        if (!res.ok) throw new Error('Request failed: ' + res.status);
        showSuccess();
      })
      .catch(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Request my quote';
        setStatus('Something went wrong sending your request. Please try again, or contact us directly.', 'error');
      });
  });

  function showSuccess() {
    var name = (document.getElementById('name').value.trim().split(/\s+/)[0]) || 'there';
    var wrap = document.createElement('div');
    wrap.className = 'form-success';
    wrap.setAttribute('role', 'status');
    wrap.setAttribute('tabindex', '-1');

    var h = document.createElement('h3');
    h.textContent = 'Thanks, ' + name + '. Request received.';
    var p = document.createElement('p');
    p.className = 'muted';
    p.textContent = "We'll confirm your vehicle is compatible and reply with a quote and available times, usually within one business day.";

    wrap.appendChild(h);
    wrap.appendChild(p);
    form.replaceChildren(wrap);
    wrap.focus();
  }
})();
