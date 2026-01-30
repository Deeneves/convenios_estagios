/**
 * Sistema de Convênios e Estágios - JavaScript Global
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeDropdowns();
    initializeMobileMenu();
    initializeAlerts();
});

/**
 * Gerenciamento de Dropdowns
 */
function initializeDropdowns() {
    // Fechar dropdowns ao clicar fora
    document.addEventListener('click', function(event) {
        const dropdowns = document.querySelectorAll('[data-dropdown]');
        dropdowns.forEach(dropdown => {
            const button = dropdown.previousElementSibling;
            if (!dropdown.contains(event.target) && !button?.contains(event.target)) {
                dropdown.classList.add('hidden');
            }
        });
    });
}

/**
 * Alterna a visibilidade de um dropdown
 * @param {string} id - ID do elemento dropdown
 */
function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    if (!dropdown) return;

    const allDropdowns = document.querySelectorAll('[data-dropdown]');

    // Fecha outros dropdowns
    allDropdowns.forEach(d => {
        if (d.id !== id) {
            d.classList.add('hidden');
        }
    });

    // Alterna o dropdown atual
    dropdown.classList.toggle('hidden');
}

/**
 * Gerenciamento do Menu Mobile
 */
function initializeMobileMenu() {
    // Configuração inicial já feita no HTML
}

/**
 * Alterna a visibilidade do menu mobile
 */
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');

    if (!mobileMenu || !menuIcon || !closeIcon) return;

    mobileMenu.classList.toggle('hidden');
    menuIcon.classList.toggle('hidden');
    closeIcon.classList.toggle('hidden');
}

/**
 * Gerenciamento de Alertas
 */
function initializeAlerts() {
    // Auto-dismiss de alertas após 5 segundos (opcional)
    const alerts = document.querySelectorAll('[role="alert"]');
    alerts.forEach(alert => {
        // Só auto-dismiss se tiver a classe auto-dismiss
        if (alert.classList.contains('auto-dismiss')) {
            setTimeout(() => {
                alert.remove();
            }, 5000);
        }
    });
}

/**
 * Fecha um alerta específico
 * @param {HTMLElement} button - Botão que disparou o evento
 */
function closeAlert(button) {
    const alert = button.closest('[role="alert"]');
    if (alert) {
        alert.remove();
    }
}

/**
 * Utilitário para confirmar ações destrutivas
 * @param {string} message - Mensagem de confirmação
 * @returns {boolean}
 */
function confirmAction(message) {
    return confirm(message || 'Tem certeza que deseja realizar esta ação?');
}
