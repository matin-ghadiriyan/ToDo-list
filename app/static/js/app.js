// TaskFlow client-side interactions

/**
 * Read the CSRF token that Flask-WTF renders into every page.
 * Used for fetch() requests to the JSON API.
 */
function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) return meta.getAttribute('content');
  const input = document.querySelector('input[name="csrf_token"]');
  return input ? input.value : '';
}

/**
 * Wrapper around fetch() that automatically attaches the CSRF header
 * for state-changing requests.
 */
async function secureFetch(url, options = {}) {
  const opts = { credentials: 'same-origin', ...options };
  const method = (opts.method || 'GET').toUpperCase();
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    opts.headers = {
      'X-CSRFToken': getCsrfToken(),
      'Content-Type': 'application/json',
      ...(opts.headers || {}),
    };
  }
  return fetch(url, opts);
}

document.addEventListener('DOMContentLoaded', () => {
  /* ---------- Mobile sidebar ---------- */
  const sidebar = document.getElementById('sidebar');
  const menuToggle = document.getElementById('menuToggle');
  const overlay = document.getElementById('overlay');

  const closeSidebar = () => {
    if (!sidebar) return;
    sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('show');
  };

  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('show');
    });
  }

  if (overlay) overlay.addEventListener('click', closeSidebar);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSidebar();
  });

  /* ---------- Auto-dismiss flash messages ---------- */
  document.querySelectorAll('.flash').forEach((flash) => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateY(-8px)';
      setTimeout(() => flash.remove(), 400);
    }, 4000);
  });

  /* ---------- Animate task cards on load ---------- */
  const animatedItems = document.querySelectorAll(
    '.task-card, .timeline-item, .stat-card, .mini-item'
  );
  animatedItems.forEach((el, index) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(12px)';
    setTimeout(() => {
      el.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, index * 45);
  });

  /* ---------- Visual feedback for toggle buttons ---------- */
  document.querySelectorAll('.check').forEach((btn) => {
    btn.addEventListener('click', () => {
      btn.style.transform = 'scale(0.85)';
      setTimeout(() => (btn.style.transform = ''), 150);
    });
  });

  /* ---------- Keyboard shortcut: "n" for new task ---------- */
  document.addEventListener('keydown', (e) => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
    if (e.key === 'n' || e.key === 'N') {
      const newBtn = document.querySelector('a[href$="/tasks/new"]');
      if (newBtn) window.location.href = newBtn.getAttribute('href');
    }
  });
});
