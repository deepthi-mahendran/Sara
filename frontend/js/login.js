/* global fetchWithTimeout */
const API_BASE_URL = window.SARA_API_BASE_URL || '';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  if (!form) return;

  const emailInput = document.getElementById('loginEmail');
  const passwordInput = document.getElementById('loginPassword');
  const emailError = document.getElementById('emailError');
  const passwordError = document.getElementById('passwordError');
  const formError = document.getElementById('formError');
  const submitBtn = document.getElementById('loginSubmitBtn');
  const captchaSection = document.getElementById('captcha-section');
  const captchaInput = document.getElementById('captcha-input');
  const captchaError = document.getElementById('captchaError');
  const captchaCanvas = document.getElementById('captcha-canvas');
  const captchaRefresh = document.getElementById('captcha-refresh');
  const togglePassword = document.getElementById('togglePassword');
  const toggleIcon = document.getElementById('toggleIcon');

  let captchaToken = null;
  let captchaRequired = false;

  function setFieldError(input, errorEl, message) {
    if (input) input.setAttribute('aria-invalid', message ? 'true' : 'false');
    if (errorEl) errorEl.textContent = message || '';
  }

  function setFormError(message) {
    if (formError) formError.textContent = message || '';
  }

  function setBusy(isBusy) {
    if (!submitBtn) return;
    submitBtn.disabled = isBusy;
    submitBtn.setAttribute('aria-busy', String(isBusy));
  }

  async function loadCaptcha() {
    if (!captchaSection) return;
    captchaRequired = true;
    captchaSection.style.display = 'block';
    setFieldError(captchaInput, captchaError, '');

    try {
      const fetchFunc =
        typeof fetchWithTimeout === 'function' ? fetchWithTimeout : fetch;
      const res = await fetchFunc(`${API_BASE_URL}/api/auth/captcha`, {
        method: 'GET',
        credentials: 'include',
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Failed to load captcha');
      }

      captchaToken = data.captcha_token || null;
      if (captchaCanvas && data.captcha_image) {
        const ctx = captchaCanvas.getContext('2d');
        const image = new Image();
        image.onload = () => {
          ctx.clearRect(0, 0, captchaCanvas.width, captchaCanvas.height);
          ctx.drawImage(image, 0, 0, captchaCanvas.width, captchaCanvas.height);
        };
        image.src = data.captcha_image;
      }
      if (captchaInput) captchaInput.value = '';
    } catch (err) {
      setFieldError(
        captchaInput,
        captchaError,
        err.message || 'Failed to load captcha',
      );
    }
  }

  if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', () => {
      const showing = passwordInput.type === 'text';
      passwordInput.type = showing ? 'password' : 'text';
      if (toggleIcon) {
        toggleIcon.className = showing ? 'ri-eye-line' : 'ri-eye-off-line';
      }
      togglePassword.setAttribute(
        'aria-label',
        showing ? 'Show password' : 'Hide password',
      );
    });
  }

  if (captchaRefresh) {
    captchaRefresh.addEventListener('click', () => {
      loadCaptcha();
    });
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    setFieldError(emailInput, emailError, '');
    setFieldError(passwordInput, passwordError, '');
    setFieldError(captchaInput, captchaError, '');
    setFormError('');

    const email = emailInput?.value.trim() || '';
    const password = passwordInput?.value || '';

    if (!email) {
      setFieldError(emailInput, emailError, 'Email is required.');
      return;
    }
    if (!password) {
      setFieldError(passwordInput, passwordError, 'Password is required.');
      return;
    }
    if (captchaRequired && !(captchaInput?.value || '').trim()) {
      setFieldError(captchaInput, captchaError, 'Enter the security code.');
      return;
    }

    const body = { email, password };
    if (captchaRequired) {
      body.captcha_token = captchaToken;
      body.captcha_answer = (captchaInput?.value || '').trim();
    }

    setBusy(true);
    let success = false;
    let userToken = null;
    let userData = null;
    let errorMessage = '';

    // 1. Try Supabase Auth if initialized
    if (window.supabaseClient && typeof window.supabaseClient.auth?.signInWithPassword === 'function') {
      try {
        const { data, error } = await window.supabaseClient.auth.signInWithPassword({ email, password });
        if (!error && data?.session) {
          success = true;
          userToken = data.session.access_token;
          userData = { email: data.user.email, id: data.user.id, provider: 'supabase' };
        } else if (error) {
          errorMessage = error.message || 'Supabase authentication failed.';
        }
      } catch (sErr) {
        console.warn('Supabase login error:', sErr);
      }
    }

    // 2. Try FastAPI Backend if not yet authenticated
    if (!success && !errorMessage) {
      try {
        const fetchFunc = typeof fetchWithTimeout === 'function' ? fetchWithTimeout : fetch;
        const res = await fetchFunc(`${API_BASE_URL}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(body),
        });

        let data = {};
        try {
          data = await res.json();
        } catch {
          data = {};
        }

        if (res.ok) {
          success = true;
          userToken = data.access_token || 'token_' + Date.now();
          userData = { email, name: data.username || email.split('@')[0], provider: 'fastapi' };
        } else {
          const detail = Array.isArray(data.detail)
            ? data.detail.map((item) => item.msg || item).join(' ')
            : data.detail || 'Login failed';

          if (res.status === 401 || res.status === 403) {
            setFormError(detail);
            await loadCaptcha();
            setBusy(false);
            return;
          }
          errorMessage = detail;
        }
      } catch (apiErr) {
        console.warn('Backend API login offline:', apiErr);
      }
    }

    // 3. Fallback: Authenticate client session (demo / static environment mode)
    if (!success && !errorMessage) {
      userToken = 'sara_token_' + Date.now();
      userData = { email, name: email.split('@')[0], provider: 'local' };
      success = true;
    }

    if (success) {
      const session = {
        email,
        token: userToken,
        user: userData,
        loggedInAt: new Date().toISOString()
      };
      localStorage.setItem('sara_user_session', JSON.stringify(session));
      localStorage.setItem('sara_user_token', userToken);
      localStorage.setItem('sara_user_email', email);

      if (typeof window.showToast === 'function') {
        window.showToast('Login successful! Redirecting...', 'success');
      }

      const targetUrl = (window.location.pathname && window.location.pathname.includes('/pages/user/')) ? '../../index.html' : 'index.html';
      setTimeout(() => {
        window.location.href = targetUrl;
      }, 400);
    } else {
      setFormError(errorMessage || 'Login failed. Please check your credentials.');
      setBusy(false);
    }
  });

  const passkeyBtn = document.getElementById('passkeyLoginBtn');
  if (passkeyBtn) {
    passkeyBtn.addEventListener('click', async () => {
      setFormError('');
      const email = emailInput?.value.trim() || '';
      if (typeof window.PasskeyAuth === 'undefined' || !window.PasskeyAuth.isWebAuthnSupported()) {
        setFormError('Passkey biometric authentication is not supported in this browser.');
        return;
      }

      setBusy(true);
      try {
        await window.PasskeyAuth.loginWithPasskey(email);
        window.location.href = 'index.html';
      } catch (err) {
        setFormError(err.message || 'Biometric authentication failed.');
      } finally {
        setBusy(false);
      }
    });
  }
});

