/**
 * Al Meeran Upholstery - Gallery Logic
 * Handles filtering and masonry-style presentation of projects.
 */

document.addEventListener('DOMContentLoaded', () => {
    const galleryGrid = document.getElementById('gallery-grid');
    const filterButtons = document.querySelectorAll('.filter-btn');

    const fallbackProjects = [
        { id: 1, name: 'Royal Velvet Suite', category: 'luxury', img: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?q=80&w=800&auto=format&fit=crop' },
        { id: 2, name: 'Minimalist Tan Leather', category: 'modern', img: 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?q=80&w=800&auto=format&fit=crop' },
        { id: 3, name: 'Royal Blue Chesterfield', category: 'classic', img: 'https://images.unsplash.com/photo-1540518614846-7eded433c457?q=80&w=800&auto=format&fit=crop' },
        { id: 4, name: 'Contemporary Accent Chair', category: 'modern', img: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=800&auto=format&fit=crop' },
        { id: 5, name: 'Modern Suite Integration', category: 'modern', img: 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=800&auto=format&fit=crop' },
        { id: 6, name: 'Golden Era Armchair', category: 'classic', img: 'https://images.unsplash.com/photo-1592078615290-033ee584e267?q=80&w=800&auto=format&fit=crop' },
        { id: 7, name: 'Luxury Penthouse Sofa', category: 'luxury', img: 'https://images.unsplash.com/photo-1631679706909-1844bbd07221?q=80&w=800&auto=format&fit=crop' },
        { id: 8, name: 'Victorian Restoration', category: 'classic', img: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?q=80&w=800&auto=format&fit=crop&v=2' },
        { id: 9, name: 'Emerald Wingback', category: 'luxury', img: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=800&auto=format&fit=crop' }
    ];

    async function fetchGallery() {
        try {
            const response = await fetch('/api/gallery');
            if (!response.ok) throw new Error('API fetch failed');
            const data = await response.json();
            return data.map(p => ({
                id: p.id,
                name: p.title, 
                category: p.category.toLowerCase(), 
                img: p.image_url 
            }));
        } catch (error) {
            console.warn("Backend not running, using fallback gallery data.");
            return fallbackProjects;
        }
    }

    async function renderGallery(filter = 'all') {
        if (!galleryGrid) return;
        galleryGrid.innerHTML = '';
        const projects = await fetchGallery();
        
        const filteredProjects = filter === 'all' 
            ? projects 
            : projects.filter(p => p.category === filter);

        if (filteredProjects.length === 0) {
            galleryGrid.innerHTML = `<div class="col-span-3 text-center py-20 text-gray-400">No projects found in this category.</div>`;
            return;
        }

        filteredProjects.forEach(project => {
            const item = document.createElement('div');
            item.className = 'gallery-item break-inside-avoid mb-8 group relative overflow-hidden rounded-xl shadow-lg cursor-pointer lightbox-trigger';
            item.setAttribute('data-category', project.category);
            item.setAttribute('data-src', project.img);
            
            item.innerHTML = `
                <img src="${project.img}" alt="${project.name}" class="w-full h-auto object-cover transition duration-700 group-hover:scale-110" onerror="this.src='https://images.unsplash.com/photo-1555041469-a586c61ea9bc?q=80&w=800&auto=format&fit=crop'">
                <div class="absolute inset-0 bg-gradient-to-t from-[#1A2238] via-transparent to-transparent opacity-0 group-hover:opacity-95 transition-opacity duration-500 flex flex-col justify-end p-8">
                    <span class="text-[#C5A059] font-bold text-sm uppercase tracking-widest mb-2">${project.category}</span>
                    <h3 class="text-white text-2xl font-bold">${project.name}</h3>
                </div>
            `;
            galleryGrid.appendChild(item);
        });
    }

    // Filter Button Clicks
    if (filterButtons) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update UI
                filterButtons.forEach(b => b.classList.remove('bg-[#1A2238]', 'text-white'));
                filterButtons.forEach(b => b.classList.add('bg-white', 'text-gray-600'));
                
                btn.classList.remove('bg-white', 'text-gray-600');
                btn.classList.add('bg-[#1A2238]', 'text-white');

                const filter = btn.getAttribute('data-filter');
                renderGallery(filter);
            });
        });
    }

    // Initial Render
    renderGallery();
});
