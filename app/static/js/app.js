/**
 * Athena LMS Frontend Helper Library
 */

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast pointer-events-auto flex items-center px-4 py-3 rounded-lg shadow-lg text-sm text-white space-x-3 transition-all duration-300 ${
        type === 'success' ? 'bg-emerald-600' :
        type === 'error' ? 'bg-rose-600' :
        type === 'warning' ? 'bg-amber-600' : 'bg-sky-600'
    }`;

    const icon = type === 'success' ? 'fa-check-circle' :
                 type === 'error' ? 'fa-circle-xmark' :
                 type === 'warning' ? 'fa-triangle-exclamation' : 'fa-circle-info';

    toast.innerHTML = `
        <i class="fa-solid ${icon} text-lg"></i>
        <span class="font-medium">${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// Close modals on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-backdrop').forEach(modal => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        });
    }
});
