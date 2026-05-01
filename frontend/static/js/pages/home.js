/**
 * Al Meeran Upholstery - Fabric Collection Logic
 * Fixed: Precision path resolution to match Flask static_url_path.
 */

async function fetchProducts() {
    try {
        const response = await fetch('/api/products');
        const data = await response.json();
        return data.map(p => {
            let img = p.image_url;
            // Ensure path is always /static/assets/...
            if (!img.startsWith('http')) {
                img = img.replace(/^\/?(static\/)?/, '/static/');
            }
            return { id: p.id, name: p.name, category: p.category || 'Classic', price: 0, image: img };
        });
    } catch (error) { return []; }
}

let allProducts = [];

async function renderFabrics(filter = 'all') {
    const grid = document.getElementById('fabric-collection-grid');
    if (!grid) return;
    if (allProducts.length === 0) allProducts = await fetchProducts();
    
    const filtered = filter === 'all' ? allProducts : allProducts.filter(p => p.category === filter);
    grid.innerHTML = filtered.map(p => `
        <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden group hover:shadow-xl transition-all duration-500 animate-in fade-in zoom-in-95">
            <div class="aspect-square overflow-hidden relative bg-[#F8F9FA]">
                <img src="${p.image}" alt="${p.name}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700">
                <div class="absolute top-3 left-3"><span class="bg-white/90 backdrop-blur px-2 py-1 rounded text-[8px] font-black uppercase text-[#1A2238] shadow-sm">${p.category}</span></div>
            </div>
            <div class="p-5">
                <h3 class="font-bold text-[#1A2238] text-[11px] mb-1 uppercase">${p.name}</h3>
                <button class="add-to-cart-btn w-full bg-[#1A2238] text-white h-10 rounded hover:bg-[#C5A059] transition text-[9px] font-bold uppercase tracking-widest flex items-center justify-center gap-2"
                        data-id="${p.id}" data-name="${p.name}" data-price="0" data-image="${p.image}">
                    <i data-lucide="plus" class="w-3 h-3"></i> Add Free Sample
                </button>
            </div>
        </div>
    `).join('');
    if (window.lucide) lucide.createIcons();
}

document.addEventListener('DOMContentLoaded', () => {
    const filterBtns = document.querySelectorAll('.shop-filter-btn');
    filterBtns.forEach(btn => {
        btn.onclick = () => {
            filterBtns.forEach(b => b.classList.remove('active', 'bg-[#1A2238]', 'text-white'));
            btn.classList.add('active', 'bg-[#1A2238]', 'text-white');
            renderFabrics(btn.dataset.filter);
        };
    });
    renderFabrics();
});
