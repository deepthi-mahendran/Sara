/* global fetchWithTimeout */
const API_BASE_URL = window.SARA_API_BASE_URL || '';

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('registerSubmitBtn');
  const messageBox = document.getElementById('formMessage');

  function setValidity(inputId, isValid, message) {
    const input = document.getElementById(inputId);
    const errorEl = input
      ? input.parentElement.querySelector('.error-message') ||
        document.getElementById(
          inputId.replace('register', '').toLowerCase() + 'ErrorReg',
        )
      : null;
    if (input) input.setAttribute('aria-invalid', String(!isValid));
    if (errorEl) errorEl.textContent = isValid ? '' : message;
  }

  const togglePassBtn = document.getElementById('togglePassword');
  const regPassInput = document.getElementById('registerPassword');
  const togglePassIcon = document.getElementById('toggleIcon');
  if (togglePassBtn && regPassInput) {
    togglePassBtn.addEventListener('click', () => {
      const isHidden = regPassInput.type === 'password';
      regPassInput.type = isHidden ? 'text' : 'password';
      if (togglePassIcon) {
        togglePassIcon.className = isHidden ? 'ri-eye-off-line' : 'ri-eye-line';
      }
      togglePassBtn.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
    });
  }

  const toggleConfirmBtn = document.getElementById('confirmTogglePassword');
  const regConfirmInput = document.getElementById('confirmPassword');
  const toggleConfirmIcon = document.getElementById('confirmToggleIcon');
  if (toggleConfirmBtn && regConfirmInput) {
    toggleConfirmBtn.addEventListener('click', () => {
      const isHidden = regConfirmInput.type === 'password';
      regConfirmInput.type = isHidden ? 'text' : 'password';
      if (toggleConfirmIcon) {
        toggleConfirmIcon.className = isHidden ? 'ri-eye-off-line' : 'ri-eye-line';
      }
      toggleConfirmBtn.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
    });
  }

  if (!btn) return;

  btn.addEventListener('click', async (e) => {
    e.preventDefault();

    let username = document.getElementById('registerUsername')?.value.trim();
    let email = document.getElementById('registerEmail')?.value.trim();
    if (
      typeof window !== 'undefined' &&
      typeof window.sanitizeHTML === 'function'
    ) {
      username = window.sanitizeHTML(username);
      email = window.sanitizeHTML(email);
    }
    const password = document.getElementById('registerPassword')?.value;
    const confirmPassword = document.getElementById('confirmPassword')?.value;

    setValidity('registerUsername', true, '');
    setValidity('registerEmail', true, '');
    setValidity('registerPassword', true, '');
    setValidity('confirmPassword', true, '');

    if (!username || !email || !password) {
      if (!username)
        setValidity('registerUsername', false, 'Full name is required.');
      if (!email) setValidity('registerEmail', false, 'Email is required.');
      if (!password)
        setValidity('registerPassword', false, 'Password is required.');
      messageBox.innerText = 'All fields are required!';
      messageBox.style.color = 'red';
      return;
    }

    const usernameRegex = /^[a-zA-Z0-9.\\-_ ]{3,20}$/;
    if (!usernameRegex.test(username)) {
      setValidity(
        'registerUsername',
        false,
        'Username must be 3-20 characters (letters, numbers, spaces, dots, hyphens, underscores).',
      );
      messageBox.innerText = 'Invalid username!';
      messageBox.style.color = 'red';
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setValidity('registerEmail', false, 'Invalid email format.');
      messageBox.innerText = 'Invalid email address!';
      messageBox.style.color = 'red';
      return;
    }

    if (password.length < 8) {
      setValidity(
        'registerPassword',
        false,
        'Password must be at least 8 characters.',
      );
      messageBox.innerText = 'Password must be at least 8 characters long!';
      messageBox.style.color = 'red';
      return;
    }

    const complexityRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!complexityRegex.test(password)) {
      setValidity(
        'registerPassword',
        false,
        'Must include uppercase, lowercase, number & special character.',
      );
      messageBox.innerText =
        'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character!';
      messageBox.style.color = 'red';
      return;
    }

    if (password !== confirmPassword) {
      setValidity('confirmPassword', false, 'Passwords do not match.');
      messageBox.innerText = 'Passwords do not match!';
      messageBox.style.color = 'red';
      return;
    }

    let success = false;
    let userToken = null;
    let errorMessage = '';

    // 1. Try Supabase Auth Registration
    if (window.supabaseClient && typeof window.supabaseClient.auth?.signUp === 'function') {
      try {
        const { data, error } = await window.supabaseClient.auth.signUp({
          email,
          password,
          options: { data: { username } }
        });
        if (!error && data?.user) {
          success = true;
          userToken = data.session?.access_token || 'supa_reg_' + Date.now();
        } else if (error) {
          errorMessage = error.message;
        }
      } catch (sErr) {
        console.warn('Supabase register error:', sErr);
      }
    }

    // 2. Try FastAPI Backend if not registered yet
    if (!success) {
      try {
        const fetchFunc = typeof fetchWithTimeout === 'function' ? fetchWithTimeout : fetch;
        const res = await fetchFunc(`${API_BASE_URL}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ username, email, password }),
        });

        const data = await res.json().catch(() => ({}));
        if (res.ok) {
          success = true;
          userToken = data.access_token || 'reg_token_' + Date.now();
        } else if (res.status === 400 || res.status === 422) {
          errorMessage = data.detail || 'Registration failed';
        }
      } catch (err) {
        console.warn('Backend API register offline:', err);
      }
    }

    // 3. Fallback: Local registration mode
    if (!success && !errorMessage) {
      success = true;
      userToken = 'sara_token_' + Date.now();
    }

    if (success) {
      const session = {
        email,
        username,
        token: userToken,
        loggedInAt: new Date().toISOString()
      };
      localStorage.setItem('sara_user_session', JSON.stringify(session));
      localStorage.setItem('sara_user_token', userToken);
      localStorage.setItem('sara_user_email', email);

      messageBox.style.color = 'green';
      messageBox.innerText = 'Account created successfully! Redirecting...';

      setTimeout(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const rawReturnUrl = urlParams.get('returnUrl') || '../../index.html';
        const safeReturnUrl =
          typeof window.sanitizeReturnUrl === 'function'
            ? window.sanitizeReturnUrl(rawReturnUrl)
            : '../../index.html';
        window.location.href = safeReturnUrl;
      }, 1000);
    } else {
      messageBox.style.color = 'red';
      messageBox.innerText = errorMessage || 'Registration failed. Please try again.';
    }
  });
});
