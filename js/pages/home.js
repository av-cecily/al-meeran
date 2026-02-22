/**
 * Al Meeran Upholstery - Fabric Rendering Logic
 * Homepage: Shows top 6 fabrics.
 * Shop Page: Shows the full expanded collection.
 * Using Local Images from images/fabric-samples/
 */

const fallbackProducts = [
    { id: 'f1', name: 'Premium Velvet', price: 45.00, image: 'assets/images/fabric-samples/premium-velvet.jpg' },
    { id: 'f2', name: 'Italian Leather', price: 85.00, image: 'assets/images/fabric-samples/italian-leather.jpg' },
    { id: 'f3', name: 'Premium Linen', price: 35.00, image: 'assets/images/fabric-samples/premium-linen.jpg' },
    { id: 'f4', name: 'Modern Tweed', price: 40.00, image: 'assets/images/fabric-samples/modern-tweed.jpg' },
    { id: 'f5', name: 'Royal Silk', price: 65.00, image: 'assets/images/fabric-samples/royal-silk.jpg' },
    { id: 'f6', name: 'Cotton Canvas', price: 25.00, image: 'assets/images/fabric-samples/cotton-canvas.jpg' },
    // 10 New Shop-Only Fabrics
    { id: 'f7', name: 'Persian Chenille', price: 55.00, image: 'assets/images/fabric-samples/persian-camille.jpg' },
    { id: 'f8', name: 'Artisan Jacquard', price: 70.00, image: 'assets/images/fabric-samples/Artisan-jacquard.jpg' },
    { id: 'f9', name: 'Organic Hemp', price: 38.00, image: 'assets/images/fabric-samples/organic-hemp.jpg' },
    { id: 'f10', name: 'Damask Rose', price: 62.00, image: 'assets/images/fabric-samples/Damask-Rose.jpg' },
    { id: 'f11', name: 'Suede Finish', price: 50.00, image: 'assets/images/fabric-samples/Suede-Finish.jpg' },
    { id: 'f12', name: 'Vintage Denim', price: 30.00, image: 'assets/images/fabric-samples/Vintage-Denim.jpg' },
    { id: 'f13', name: 'Moroccan Weave', price: 48.00, image: 'assets/images/fabric-samples/Moroccan-Weave.jpg' },
    { id: 'f14', name: 'Brushed Mohair', price: 95.00, image: 'assets/images/fabric-samples/Brushed-Mohair.jpg' },
    { id: 'f15', name: 'Heavy Jute', price: 28.00, image: 'assets/images/fabric-samples/Heavy-Jute.jpg' },
    { id: 'f16', name: 'Golden Brocade', price: 88.00, image: 'assets/images/fabric-samples/Golden-Brocade.jpg' }
];

async function fetchProducts() {
    try {
        const response = await fetch('http://localhost:5000/api/products');
        if (!response.ok) throw new Error('API fetch failed');
        const data = await response.json();
        // Map backend structure to frontend structure if needed
        return data.map(p => ({
            id: p.id,
            name: p.name,
            price: p.price,
            image: p.image_url.startsWith('http') ? p.image_url : (p.image_url.startsWith('/') ? p.image_url : p.image_url) // robust path handling
        }));
    } catch (error) {
        console.warn("Backend not running, using fallback data.");
        return fallbackProducts;
    }
}

async function renderFabrics() {
    const grid = document.getElementById('fabric-collection-grid');
    if (!grid) return;

    const products = await fetchProducts();
    const isHome = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/') || window.location.pathname === '';
    const itemsToShow = isHome ? products.slice(0, 6) : products;

    grid.innerHTML = itemsToShow.map(p => `
        <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden group hover:shadow-xl transition-all duration-500">
            <div class="aspect-square overflow-hidden relative bg-[#F8F9FA]">
                <img src="${p.image}" alt="${p.name}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" onerror="this.src='assets/images/fabric-samples/premium-velvet.jpg'">
            </div>
            <div class="p-5">
                <h3 class="font-bold text-[#1A2238] text-[11px] mb-1 uppercase tracking-tight">${p.name}</h3>
                <p class="text-[#C5A059] font-black text-sm mb-4">BHD ${Number(p.price).toFixed(2)}<span class="text-[9px] text-gray-400 font-normal uppercase"> / meter</span></p>
                
                <div class="flex items-center gap-2">
                    <div class="flex-grow flex items-center border border-gray-200 rounded-md overflow-hidden h-10 px-2 bg-gray-50">
                        <input type="number" id="qty-${p.id}" value="1" min="1" class="w-full text-center text-xs font-bold outline-none bg-transparent" placeholder="Qty">
                        <span class="text-[9px] font-bold text-gray-400">M</span>
                    </div>
                    <button class="add-to-cart-btn bg-[#1A2238] text-white h-10 px-4 rounded-md hover:bg-[#C5A059] transition shadow-lg"
                            data-id="${p.id}" 
                            data-name="${p.name}" 
                            data-price="${p.price}" 
                            data-image="${p.image}">
                        <i data-lucide="shopping-cart" class="w-4 h-4"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');

    if (window.lucide) lucide.createIcons();
}

window.addEventListener('load', renderFabrics);
document.addEventListener('DOMContentLoaded', () => {
    renderFabrics();
});
setInterval(() => {
    if (document.getElementById('fabric-collection-grid')?.innerHTML === '') renderFabrics();
}, 2000);
