/**
 * Al Meeran Upholstery - Global Cart Logic
 * Updated to support Quantity (Meters).
 */

window.AlMeeranCart = {
    items: JSON.parse(localStorage.getItem('al_meeran_cart')) || [],

    init() {
        this.updateCartUI();
        this.attachEventListeners();
        console.log("Cart System Initialized");
    },

    addItem(product, qty) {
        const existingItem = this.items.find(item => item.id === product.id);
        if (existingItem) {
            existingItem.quantity += qty;
        } else {
            this.items.push({ ...product, quantity: qty });
        }
        this.save();
        this.updateCartUI();
        this.showNotification(`Added ${qty}m of ${product.name} to selection!`);
    },

    removeItem(id) {
        this.items = this.items.filter(item => item.id !== id);
        this.save();
        this.updateCartUI();
    },

    save() {
        localStorage.setItem('al_meeran_cart', JSON.stringify(this.items));
    },

    getTotal() {
        return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2);
    },

    getCount() {
        return this.items.reduce((sum, item) => sum + item.quantity, 0);
    },

    updateCartUI() {
        // Update badge counts in the navbar
        const badges = document.querySelectorAll('.cart-count');
        const itemsCount = this.items.reduce((sum, item) => sum + item.quantity, 0);
        
        badges.forEach(badge => {
            badge.textContent = Math.round(itemsCount);
            badge.style.display = this.items.length > 0 ? 'flex' : 'none';
        });

        // Update Cart Drawer if placeholders exist
        const drawerList = document.getElementById('cart-items-list');
        const drawerTotal = document.getElementById('cart-total-price');
        
        if (drawerList) {
            drawerList.innerHTML = this.items.length === 0 
                ? '<div class="text-center py-20"><i data-lucide="shopping-bag" class="w-12 h-12 mx-auto text-gray-100 mb-4"></i><p class="text-gray-400 text-xs italic">Your selection is empty.</p></div>' 
                : this.items.map(item => `
                    <div class="flex items-center justify-between border-b border-gray-50 py-4">
                        <div class="flex items-center">
                            <img src="${item.image}" class="w-12 h-12 rounded-lg object-cover mr-4 shadow-sm">
                            <div>
                                <p class="font-bold text-[11px] uppercase tracking-wider text-[#1A2238]">${item.name}</p>
                                <p class="text-[10px] text-[#C5A059] font-black">${item.quantity}M x BHD ${item.price.toFixed(2)}</p>
                            </div>
                        </div>
                        <button onclick="AlMeeranCart.removeItem('${item.id}')" class="text-gray-300 hover:text-red-500 transition">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                `).join('');
            
            if (window.lucide) lucide.createIcons();
        }

        if (drawerTotal) {
            drawerTotal.textContent = `BHD ${this.getTotal()}`;
        }
    },

    showNotification(msg) {
        const toast = document.createElement('div');
        toast.className = 'fixed top-24 right-10 bg-[#1A2238] text-white px-8 py-4 rounded-xl shadow-2xl z-[999999] border-l-4 border-[#C5A059] animate-bounce';
        toast.innerHTML = `<span class="text-[#C5A059] font-bold uppercase text-[10px] tracking-widest block mb-1">Success</span> <p class="text-sm font-medium">${msg}</p>`;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-20px)';
            toast.style.transition = '0.5s';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    },

    attachEventListeners() {
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.add-to-cart-btn');
            if (btn) {
                const id = btn.dataset.id;
                const qtyInput = document.getElementById(`qty-${id}`);
                const qty = qtyInput ? parseInt(qtyInput.value) || 1 : 1;

                const product = {
                    id: id,
                    name: btn.dataset.name,
                    price: parseFloat(btn.dataset.price),
                    image: btn.dataset.image
                };
                this.addItem(product, qty);
            }

            // Cart Drawer Toggles
            if (e.target.closest('#cart-toggle-btn')) {
                document.getElementById('cart-drawer')?.classList.remove('translate-x-full');
            }
            if (e.target.closest('#close-cart-btn')) {
                document.getElementById('cart-drawer')?.classList.add('translate-x-full');
            }
        });
    }
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => AlMeeranCart.init());
} else {
    AlMeeranCart.init();
}
