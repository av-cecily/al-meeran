/**
 * Al Meeran Upholstery - Gallery Logic
 * Fixed: Robust static path resolution for project images.
 */

document.addEventListener('DOMContentLoaded', () => {
    const galleryGrid = document.getElementById('gallery-grid');

    async function fetchGallery() {
        try {
            const response = await fetch('/api/gallery');
            const data = await response.json();
            
            return data.filter(p => p.category !== 'Fabric').map(p => {
                let img = p.image_url;
                if (!img.startsWith('http')) {
                    if (img.startsWith('static/')) img = '/' + img;
                    else if (!img.startsWith('/static/')) img = '/static/' + img;
                }
                return { id: p.id, name: p.title, category: p.category || 'Interior', img: img };
            });
        } catch (error) { return []; }
    }

    async function renderGallery() {
        if (!galleryGrid) return;
        const projects = await fetchGallery();
        galleryGrid.innerHTML = projects.map(project => `
            <div class="gallery-item break-inside-avoid mb-8 group relative overflow-hidden rounded-xl shadow-lg cursor-pointer lightbox-trigger" data-src="${project.img}">
                <img src="${project.img}" alt="${project.name}" class="w-full h-auto object-cover transition duration-700 group-hover:scale-110">
                <div class="absolute inset-0 bg-gradient-to-t from-[#1A2238] via-transparent to-transparent opacity-0 group-hover:opacity-95 transition p-8 flex flex-col justify-end">
                    <span class="text-[#C5A059] font-bold text-[9px] uppercase tracking-widest mb-2">${project.category}</span>
                    <h3 class="text-white text-xl font-bold uppercase">${project.name}</h3>
                </div>
            </div>
        `).join('');
        if (window.lucide) lucide.createIcons();
    }

    renderGallery();
});
