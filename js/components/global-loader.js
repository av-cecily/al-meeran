/**
 * Al Meeran Upholstery - Global Component Loader
 * Fixed: Transparent Header ONLY on Home page. Solid on all other pages.
 */

const GlobalComponents = {
    // We will dynamically adjust the classes in the init() function
    getHeaderTemplate(isHome) {
        const navClasses = isHome ? 'bg-transparent text-white border-b border-white/5' : 'bg-[#1A2238] text-white shadow-xl';
        const paddingClasses = isHome ? 'py-6' : 'py-4';
        
        return `
        <header id="main-navbar" class="fixed w-full z-50 nav-transition ${navClasses}">
            <nav class="container mx-auto px-6 ${paddingClasses} flex justify-between items-center transition-all duration-300" id="nav-container">
                <a href="index.html" class="flex flex-col leading-tight">
                    <span class="text-xl font-extrabold tracking-tighter uppercase">AL MEERAN</span>
                    <span class="text-[9px] font-bold tracking-[0.4em] text-[#C5A059] -mt-1 uppercase">UPHOLSTERY</span>
                </a>
                <div class="hidden lg:flex space-x-10 items-center font-bold uppercase text-[10px] tracking-[0.2em]">
                    <a href="index.html" class="hover:text-[#C5A059] transition">Home</a>
                    <a href="about.html" class="hover:text-[#C5A059] transition">About</a>
                    <a href="shop.html" class="hover:text-[#C5A059] transition">Fabric Shop</a>
                    <a href="gallery.html" class="hover:text-[#C5A059] transition">Gallery</a>
                    <a href="visualizer.html" class="hover:text-[#C5A059] transition">Visualizer</a>
                    <a href="quote.html" class="bg-[#C5A059] px-6 py-3 text-white rounded-sm hover:bg-[#b08e4d] transition shadow-lg shadow-[#C5A059]/20">Get a Quote</a>
                    <button id="cart-toggle-btn" class="relative hover:text-[#C5A059] transition ml-4">
                        <i data-lucide="shopping-bag" class="w-5 h-5"></i>
                        <span class="cart-count absolute -top-2 -right-2 bg-[#C5A059] text-[#1A2238] text-[9px] font-black w-4 h-4 rounded-full flex items-center justify-center border border-[#1A2238] hidden">0</span>
                    </button>
                </div>
                <button id="mobile-menu-btn" class="lg:hidden focus:outline-none"><i data-lucide="menu" class="w-6 h-6"></i></button>
            </nav>
            <div id="mobile-menu" class="hidden absolute top-full left-0 w-full bg-[#1A2238] border-t border-white/5 py-8 shadow-2xl lg:hidden text-center">
                <div class="container mx-auto px-6 flex flex-col space-y-6 text-xs font-bold uppercase tracking-widest text-white">
                    <a href="index.html">Home</a>
                    <a href="about.html">About</a>
                    <a href="shop.html">Shop</a>
                    <a href="gallery.html">Gallery</a>
                    <a href="visualizer.html">Visualizer</a>
                    <a href="quote.html" class="text-[#C5A059]">Request Quote</a>
                </div>
            </div>
        </header>
        `;
    },
    drawer: `
        <div id="cart-drawer" class="fixed top-0 right-0 w-80 h-full bg-white z-[999999] shadow-2xl transition-transform duration-500 translate-x-full border-l border-gray-100 flex flex-col">
            <div class="bg-[#1A2238] p-6 text-white flex justify-between items-center">
                <h3 class="font-bold text-xs tracking-widest uppercase">Your Selection</h3>
                <button id="close-cart-btn" class="text-white hover:text-[#C5A059] transition"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>
            <div id="cart-items-list" class="flex-grow overflow-y-auto p-6 flex flex-col gap-4"></div>
            <div class="p-8 border-t border-gray-100 bg-gray-50">
                <div class="flex justify-between items-center mb-6">
                    <span class="text-[10px] font-extrabold uppercase tracking-[0.2em] text-gray-400">Estimate Total</span>
                    <span id="cart-total-price" class="text-xl font-black text-[#1A2238] tracking-tighter">BHD 0.00</span>
                </div>
                <a href="checkout.html" class="block w-full bg-[#1A2238] text-white py-4 rounded-sm text-center font-bold uppercase tracking-widest text-[10px] hover:bg-[#C5A059] transition shadow-xl">Checkout</a>
            </div>
        </div>
    `,
    footer: `
        <footer class="bg-[#F8F9FA] py-20 border-t border-gray-100">
            <div class="container mx-auto px-6 text-center">
                <div class="flex flex-col items-center mb-8">
                    <span class="text-2xl font-black tracking-tighter uppercase text-[#1A2238]">AL MEERAN</span>
                    <span class="text-[10px] font-bold tracking-[0.4em] text-[#C5A059] -mt-1 uppercase">UPHOLSTERY</span>
                </div>
                <p class="text-gray-400 text-[9px] font-bold uppercase tracking-[0.3em]">&copy; 2026 Al Meeran Upholstery. All Rights Reserved.</p>
            </div>
        </footer>

        <!-- Global Lightbox Modal -->
        <div id="lightbox-modal" class="fixed inset-0 z-[999999] bg-[#1A2238]/95 backdrop-blur-sm hidden flex items-center justify-center opacity-0 transition-opacity duration-500">
            <button id="lightbox-close" class="absolute top-6 right-6 text-white/50 hover:text-[#C5A059] transition-colors z-[1000000]">
                <i data-lucide="x" class="w-12 h-12"></i>
            </button>
            <div class="relative w-full max-w-5xl px-6 flex justify-center">
                <img id="lightbox-image" src="" class="max-h-[85vh] max-w-full rounded-lg shadow-2xl transform scale-90 transition-all duration-500 ease-out object-contain" alt="Gallery Zoom">
            </div>
        </div>
    `,

    init() {
        // Detect if we are on the Home Page
        const isHome = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/') || window.location.pathname === '';
        
        const hP = document.getElementById('global-header');
        const dP = document.getElementById('global-drawer');
        const fP = document.getElementById('global-footer');

        if (hP) hP.innerHTML = this.getHeaderTemplate(isHome);
        if (dP) dP.innerHTML = this.drawer;
        if (fP) fP.innerHTML = this.footer;

        if (window.lucide) lucide.createIcons();

        // Scroll Logic - Only for Home Page
        if (isHome) {
            window.addEventListener('scroll', () => {
                const nav = document.getElementById('main-navbar');
                const cont = document.getElementById('nav-container');
                if (window.scrollY > 50) {
                    nav.classList.add('bg-[#1A2238]', 'shadow-2xl');
                    nav.classList.remove('bg-transparent', 'border-b', 'border-white/5');
                    cont.classList.add('py-4');
                    cont.classList.remove('py-6');
                } else {
                    nav.classList.remove('bg-[#1A2238]', 'shadow-2xl');
                    nav.classList.add('bg-transparent', 'border-b', 'border-white/5');
                    cont.classList.add('py-6');
                    cont.classList.remove('py-4');
                }
            });
        }

        // --- GLOBAL LIGHTBOX LOGIC (Event Delegation) ---
        const lightbox = document.getElementById('lightbox-modal');
        const lightboxImg = document.getElementById('lightbox-image');
        const closeBtn = document.getElementById('lightbox-close');

        if (lightbox && lightboxImg) {
            // Open Lightbox (Delegated)
            document.body.addEventListener('click', (e) => {
                const trigger = e.target.closest('.lightbox-trigger');
                if (trigger) {
                    const src = trigger.getAttribute('data-src');
                    if (!src) return;

                    lightboxImg.src = src;
                    lightbox.classList.remove('hidden');

                    requestAnimationFrame(() => {
                        lightbox.classList.remove('opacity-0');
                        lightboxImg.classList.remove('scale-90');
                        lightboxImg.classList.add('scale-100');
                    });
                }
            });

            // Close Lightbox Function
            const closeLightbox = () => {
                lightbox.classList.add('opacity-0');
                lightboxImg.classList.remove('scale-100');
                lightboxImg.classList.add('scale-90');
                
                setTimeout(() => {
                    lightbox.classList.add('hidden');
                    lightboxImg.src = '';
                }, 500); 
            };

            if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
            
            // Close on background click
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox || e.target.closest('.relative') === null) {
                    if (e.target.id !== 'lightbox-image') closeLightbox();
                }
            });

            // Close on ESC key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && !lightbox.classList.contains('hidden')) {
                    closeLightbox();
                }
            });
        }
    }
};

document.addEventListener('DOMContentLoaded', () => GlobalComponents.init());
