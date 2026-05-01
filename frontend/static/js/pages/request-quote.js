/**
 * Al Meeran Upholstery - Request Quote Logic
 * Updated: Handles Address, Dynamic Fabric List and Photo.
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upholstery-quote-form');
    const fabricDropdown = document.getElementById('fabric-preference');
    
    // --- Load Live Fabrics into Dropdown ---
    async function loadFabrics() {
        try {
            const res = await fetch('/api/products');
            const fabrics = await res.json();
            fabrics.forEach(f => {
                const opt = document.createElement('option');
                opt.value = f.name;
                opt.textContent = f.name;
                fabricDropdown.appendChild(opt);
            });
        } catch(e) { console.error("Could not load fabrics for dropdown"); }
    }
    loadFabrics();

    if (!form) return;

    form.onsubmit = async (e) => {
        e.preventDefault();
        
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = 'Processing...';

        const formData = new FormData();
        formData.append('name', form.user_name.value);
        formData.append('phone', form.user_phone.value);
        formData.append('address', form.user_address.value);
        formData.append('type', form.furniture_type.value);
        formData.append('fabric', form.fabric_preference.value);
        formData.append('message', form.user_message.value);
        
        if (form.furniture_image.files[0]) {
            formData.append('image', form.furniture_image.files[0]);
        }

        try {
            const response = await fetch('/api/quotes', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                showSuccessModal();
                form.reset();
            } else {
                alert("Submission failed. Please check form details.");
            }
        } catch (error) {
            console.error("Quote Error:", error);
            alert("Connection error. Ensure server is running.");
        } finally {
            btn.disabled = false;
            btn.textContent = originalText;
        }
    };

    function showSuccessModal() {
        const modal = document.getElementById('success-modal');
        const content = document.getElementById('modal-content');
        if (!modal || !content) return;

        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        if(window.lucide) lucide.createIcons();

        setTimeout(() => {
            content.classList.remove('scale-90', 'opacity-0');
            content.classList.add('scale-100', 'opacity-100');
        }, 10);
    }
});
