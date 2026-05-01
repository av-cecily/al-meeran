/**
 * Al Meeran Upholstery - Navbar Component
 * Handles scroll effects and mobile menu state.
 */

window.initNavbar = function() {
    const navbar = document.getElementById('main-navbar');
    
    // Handle scroll background change
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('bg-[#1A2238]', 'shadow-lg');
            navbar.classList.remove('bg-transparent');
        } else {
            navbar.classList.remove('bg-[#1A2238]', 'shadow-lg');
            navbar.classList.add('bg-transparent');
        }
    });

    console.log("Navbar initialized");
};
