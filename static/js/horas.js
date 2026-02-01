document.addEventListener('DOMContentLoaded', function() {
    const detailOpenButton = document.getElementById('open-delete-modal');
    const detailModal = document.getElementById('delete-modal');
    const detailCloseButtons = document.querySelectorAll('[data-close-delete-modal]');
    const detailCancelButton = detailModal ? detailModal.querySelector('[data-close-delete-modal]') : null;
    const listForm = document.getElementById('delete-modal-form');
    let lastTrigger = null;

    if (detailOpenButton && detailModal) {
        const openDetailModal = () => {
            detailModal.classList.remove('hidden');
            detailModal.setAttribute('aria-hidden', 'false');
            if (detailCancelButton) detailCancelButton.focus();
        };

        const closeDetailModal = () => {
            detailModal.classList.add('hidden');
            detailModal.setAttribute('aria-hidden', 'true');
            detailOpenButton.focus();
        };

        detailOpenButton.addEventListener('click', openDetailModal);
        detailCloseButtons.forEach(button => button.addEventListener('click', closeDetailModal));

        detailModal.addEventListener('click', (event) => {
            if (event.target === detailModal) {
                closeDetailModal();
            }
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && !detailModal.classList.contains('hidden')) {
                closeDetailModal();
            }
        });
    }

    if (detailModal && listForm) {
        const openListModal = (trigger) => {
            const deleteUrl = trigger.getAttribute('data-delete-url');
            if (!deleteUrl) return;

            listForm.setAttribute('action', deleteUrl);
            detailModal.classList.remove('hidden');
            detailModal.setAttribute('aria-hidden', 'false');
            lastTrigger = trigger;

            const cancelButton = detailModal.querySelector('[data-close-delete-modal]');
            if (cancelButton) cancelButton.focus();
        };

        const closeListModal = () => {
            detailModal.classList.add('hidden');
            detailModal.setAttribute('aria-hidden', 'true');
            if (lastTrigger) lastTrigger.focus();
        };

        document.querySelectorAll('[data-open-delete-modal]').forEach(button => {
            button.addEventListener('click', () => openListModal(button));
        });

        detailCloseButtons.forEach(button => button.addEventListener('click', closeListModal));

        detailModal.addEventListener('click', (event) => {
            if (event.target === detailModal) {
                closeListModal();
            }
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && !detailModal.classList.contains('hidden')) {
                closeListModal();
            }
        });
    }
});
