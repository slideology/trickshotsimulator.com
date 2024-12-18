// Initialize Lucide icons
lucide.createIcons();

// Language selector functionality
document.addEventListener('DOMContentLoaded', function() {
    const languageButton = document.getElementById('language-menu-button');
    const languageMenu = document.getElementById('language-menu');
    const selectedLanguage = document.getElementById('selected-language');
    const languageOptions = document.querySelectorAll('.language-option');

    // Toggle dropdown
    languageButton?.addEventListener('click', () => {
        const isExpanded = languageButton.getAttribute('aria-expanded') === 'true';
        languageButton.setAttribute('aria-expanded', !isExpanded);
        languageMenu?.classList.toggle('hidden');
    });

    // Handle language selection
    languageOptions?.forEach(option => {
        option.addEventListener('click', (e) => {
            e.preventDefault();
            selectedLanguage.textContent = option.textContent;
            languageMenu?.classList.add('hidden');
            languageButton?.setAttribute('aria-expanded', 'false');
            // Here you can add logic to change the language
            const lang = option.getAttribute('data-lang');
            console.log('Selected language:', lang);
            // You can store the selected language in localStorage
            localStorage.setItem('selectedLanguage', lang);
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!languageButton?.contains(e.target)) {
            languageMenu?.classList.add('hidden');
            languageButton?.setAttribute('aria-expanded', 'false');
        }
    });

    // Mobile menu functionality
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = mobileMenuButton?.querySelector('[data-lucide="menu"]');
    const closeIcon = mobileMenuButton?.querySelector('[data-lucide="x"]');

    mobileMenuButton?.addEventListener('click', () => {
        const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
        mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
        mobileMenu?.classList.toggle('hidden');
        menuIcon?.classList.toggle('hidden');
        closeIcon?.classList.toggle('hidden');
    });

    // Load saved language preference
    const savedLanguage = localStorage.getItem('selectedLanguage');
    if (savedLanguage) {
        const option = document.querySelector(`[data-lang="${savedLanguage}"]`);
        if (option) {
            selectedLanguage.textContent = option.textContent;
        }
    }
});
