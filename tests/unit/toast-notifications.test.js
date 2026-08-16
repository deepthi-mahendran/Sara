import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';

describe('toast-notifications.js — SaraNotifications', () => {
  beforeEach(async () => {
    vi.useFakeTimers();
    document.body.innerHTML = '';
    vi.resetModules();
    const existing = document.getElementById('sara-notif-container');
    if (existing) existing.remove();
    await import('../../frontend/js/toast-notifications.js');
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.resetModules();
  });

  function advanceFadeIn() {
    // Advance requestAnimationFrame (synthetic timer in vitest)
    vi.advanceTimersByTime(0);
  }

  function advanceDismiss() {
    // Advance the 300ms dismiss fade-out timer
    vi.advanceTimersByTime(300);
  }

  it('info() creates a notification with correct message', () => {
    window.SaraNotifications.info('Test info message', 5000);
    advanceFadeIn();
    const container = document.getElementById('sara-notif-container');
    expect(container).not.toBeNull();
    const el = container.querySelector('[role="alert"]');
    expect(el).not.toBeNull();
    expect(el.textContent).toBe('Test info message');
  });

  it('success() creates a notification', () => {
    window.SaraNotifications.success('Success!', 5000);
    advanceFadeIn();
    const el = document.querySelector('[role="alert"]');
    expect(el).not.toBeNull();
    expect(el.textContent).toBe('Success!');
  });

  it('warning() creates a notification', () => {
    window.SaraNotifications.warning('Warning text', 5000);
    advanceFadeIn();
    const el = document.querySelector('[role="alert"]');
    expect(el).not.toBeNull();
    expect(el.textContent).toBe('Warning text');
  });

  it('error() creates a notification', () => {
    window.SaraNotifications.error('Error text', 5000);
    advanceFadeIn();
    const el = document.querySelector('[role="alert"]');
    expect(el).not.toBeNull();
    expect(el.textContent).toBe('Error text');
  });

  it('notifications have role="alert" for accessibility', () => {
    window.SaraNotifications.info('Alert test', 5000);
    advanceFadeIn();
    const el = document.querySelector('[role="alert"]');
    expect(el).not.toBeNull();
    expect(el.getAttribute('role')).toBe('alert');
  });

  it('click on notification triggers dismiss', () => {
    window.SaraNotifications.info('Click to dismiss', 100000);
    advanceFadeIn();
    const el = document.querySelector('[role="alert"]');
    expect(el).not.toBeNull();
    el.click();
    advanceDismiss();
    const remaining = document.querySelectorAll('[role="alert"]');
    expect(remaining.length).toBe(0);
  });

  it('auto-dismiss removes notification after duration', () => {
    window.SaraNotifications.info('Auto-dismiss me', 2000);
    advanceFadeIn();
    // Advance past the 2000ms auto-dismiss timer
    vi.advanceTimersByTime(2000);
    advanceDismiss();
    const remaining = document.querySelectorAll('[role="alert"]');
    expect(remaining.length).toBe(0);
  });

  it('dismiss() API manually removes the notification', () => {
    window.SaraNotifications.info('Manual dismiss', 100000);
    advanceFadeIn();
    expect(document.querySelector('[role="alert"]')).not.toBeNull();
    window.SaraNotifications.dismiss(document.querySelector('[role="alert"]'));
    advanceDismiss();
    expect(document.querySelector('[role="alert"]')).toBeNull();
  });

  it('shows queued notifications in order', () => {
    // Run animation frames synchronously so the queue keeps flushing.
    window.requestAnimationFrame = (cb) => {
      cb();
      return 1;
    };

    window.SaraNotifications.info('First', 500);
    window.SaraNotifications.info('Second', 500);
    window.SaraNotifications.info('Third', 500);
    vi.advanceTimersByTime(0);

    const messages = Array.from(
      document.querySelectorAll('[role="alert"]'),
    ).map((el) => el.textContent);
    // All three are queued and shown in the order they were added.
    expect(messages).toEqual(['First', 'Second', 'Third']);
  });
});
