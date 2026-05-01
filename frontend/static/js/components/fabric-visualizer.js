/**
 * AI Fabric Visualizer - Final Master Version
 * Fixed: Robust path resolution for fabrics.
 */

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('visualizer-canvas');
    const ctx = canvas.getContext('2d');
    const fileInput = document.getElementById('sofa-upload');
    const fabricGrid = document.getElementById('fabric-grid-selector');
    const shimmer = document.getElementById('shimmer-effect');
    
    const maskCanvas = document.createElement('canvas');
    const maskCtx = maskCanvas.getContext('2d');
    const shadowCanvas = document.createElement('canvas');
    const shadowCtx = shadowCanvas.getContext('2d');
    
    let originalImage = null;
    let selectedFabric = null;
    let aiLayersReady = false;

    async function initFabricGrid() {
        if(!fabricGrid) return;
        try {
            const response = await fetch('/api/products');
            const fabrics = await response.json();
            fabricGrid.innerHTML = fabrics.map(f => {
                let img = f.image_url;
                if (!img.startsWith('http')) {
                    if (img.startsWith('static/')) img = '/' + img;
                    else if (!img.startsWith('/static/')) img = '/static/' + img;
                }
                return `<div class="fabric-circle" style="background-image: url('${img}')" title="${f.name}" onclick="window.selectFabric('${img}')"></div>`;
            }).join('');
        } catch (err) { console.error("Visualizer Fabrics Error"); }
    }

    window.selectFabric = (url) => {
        selectedFabric = url;
        document.querySelectorAll('.fabric-circle').forEach(c => {
            c.classList.toggle('selected', c.style.backgroundImage.includes(url));
        });
        renderFullPreview();
    };

    initFabricGrid();

    fileInput.onchange = async (e) => {
        if (!e.target.files[0]) return;
        const file = e.target.files[0];
        if(shimmer) shimmer.style.display = 'block';
        document.getElementById('upload-prompt').style.display = 'none';
        canvas.style.display = 'block';

        const reader = new FileReader();
        reader.onload = (ev) => {
            const img = new Image();
            img.onload = () => {
                originalImage = img;
                const aspect = img.width / img.height;
                canvas.width = maskCanvas.width = shadowCanvas.width = 1000;
                canvas.height = maskCanvas.height = shadowCanvas.height = 1000 / aspect;
                renderFullPreview();
            };
            img.src = ev.target.result;
        };
        reader.readAsDataURL(file);

        const formData = new FormData();
        formData.append('image', file);
        try {
            const res = await fetch('/api/visualize/process', { method: 'POST', body: formData });
            const data = await res.json();
            const loadL = (c, ctxL, b64) => new Promise(r => {
                const i = new Image();
                i.onload = () => { ctxL.clearRect(0,0,c.width,c.height); ctxL.drawImage(i, 0, 0, c.width, c.height); r(); };
                i.src = `data:image/png;base64,${b64}`;
            });
            await Promise.all([loadL(maskCanvas, maskCtx, data.mask), loadL(shadowCanvas, shadowCtx, data.shadows)]);
            aiLayersReady = true;
            if(shimmer) shimmer.style.display = 'none';
            document.getElementById('visualizer-controls').classList.remove('hidden');
            renderFullPreview();
        } catch (err) { alert("AI Error"); if(shimmer) shimmer.style.display = 'none'; }
    };

    function renderFullPreview() {
        if (!originalImage) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(originalImage, 0, 0, canvas.width, canvas.height);
        
        if (selectedFabric && aiLayersReady) {
            const textureImg = new Image();
            textureImg.onload = () => {
                const fabricCanvas = document.createElement('canvas');
                fabricCanvas.width = canvas.width; fabricCanvas.height = canvas.height;
                const fctx = fabricCanvas.getContext('2d');
                const pattern = fctx.createPattern(textureImg, 'repeat');
                const matrix = new DOMMatrix().scale(0.5, 0.5);
                pattern.setTransform(matrix);
                fctx.fillStyle = pattern; fctx.fillRect(0, 0, fabricCanvas.width, fabricCanvas.height);
                
                const clipCanvas = document.createElement('canvas');
                clipCanvas.width = canvas.width; clipCanvas.height = canvas.height;
                const cctx = clipCanvas.getContext('2d');
                cctx.drawImage(maskCanvas, 0, 0);
                cctx.globalCompositeOperation = 'source-in';
                cctx.drawImage(fabricCanvas, 0, 0);
                
                ctx.drawImage(originalImage, 0, 0, canvas.width, canvas.height);
                ctx.save(); ctx.globalAlpha = 0.85; ctx.drawImage(clipCanvas, 0, 0); ctx.restore();
                
                const shadowClip = document.createElement('canvas');
                shadowClip.width = canvas.width; shadowClip.height = canvas.height;
                const sctx = shadowClip.getContext('2d');
                sctx.drawImage(maskCanvas, 0, 0);
                sctx.globalCompositeOperation = 'source-in'; sctx.drawImage(shadowCanvas, 0, 0);
                ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = 0.7; ctx.drawImage(shadowClip, 0, 0); ctx.restore();
            };
            textureImg.src = selectedFabric;
        }
    }

    const resetBtn = document.getElementById('reset-visualizer');
    if(resetBtn) resetBtn.onclick = () => location.reload();
});
