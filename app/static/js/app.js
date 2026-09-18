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

/**
 * A tiny toast notification helper.
 */
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer') || (() => {
    const el = document.createElement('div');
    el.id = 'toastContainer';
    el.className = 'toast-container';
    document.body.appendChild(el);
    return el;
  })();

  const icons = { success: '✅', danger: '⛔', info: 'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(toast);

  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 350);
  }, 3800);
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
    }, 4500);
  });

  /* ---------- Animate elements on load (staggered) ---------- */
  const animatedItems = document.querySelectorAll(
    '.task-card, .timeline-item, .stat-card, .mini-item, .panel, .hero'
  );
  animatedItems.forEach((el, index) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(14px)';
    setTimeout(() => {
      el.style.transition = 'opacity 0.4s cubic-bezier(0.22, 1, 0.36, 1), transform 0.4s cubic-bezier(0.22, 1, 0.36, 1)';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, Math.min(index * 40, 600));
  });

  /* ---------- Animated progress ring ---------- */
  const ring = document.querySelector('.ring-fg');
  if (ring) {
    const target = ring.style.strokeDashoffset;
    ring.style.strokeDashoffset = '327';
    requestAnimationFrame(() => {
      setTimeout(() => { ring.style.strokeDashoffset = target; }, 120);
    });
  }

  /* ---------- Animated stat counters ---------- */
  document.querySelectorAll('.stat-card strong').forEach((el) => {
    const finalValue = parseInt(el.textContent, 10);
    if (Number.isNaN(finalValue) || finalValue === 0) return;
    let current = 0;
    const step = Math.max(1, Math.ceil(finalValue / 24));
    const timer = setInterval(() => {
      current += step;
      if (current >= finalValue) {
        current = finalValue;
        clearInterval(timer);
      }
      el.textContent = current;
    }, 28);
  });

  /* ---------- Visual feedback for toggle buttons ---------- */
  document.querySelectorAll('.check').forEach((btn) => {
    btn.addEventListener('click', () => {
      btn.style.transform = 'scale(0.82)';
      setTimeout(() => (btn.style.transform = ''), 160);
    });
  });

  /* ---------- Keyboard shortcut: "n" for new task ---------- */
  document.addEventListener('keydown', (e) => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === 'n' || e.key === 'N') {
      const newBtn = document.querySelector('a[href$="/tasks/new"]');
      if (newBtn) window.location.href = newBtn.getAttribute('href');
    }
  });
});
