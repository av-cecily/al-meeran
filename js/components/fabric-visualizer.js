/**
 * AI Fabric Visualizer - Advanced Prototype with Masking
 * Updated to use local images from images/fabric-samples/
 */

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('visualizer-canvas');
    const ctx = canvas.getContext('2d');
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('sofa-upload');
    const fabricGrid = document.getElementById('fabric-grid-selector');
    const aiProcessBtn = document.getElementById('ai-process-btn');
    const resetBtn = document.getElementById('reset-visualizer');
    const newProjectBtn = document.getElementById('new-project-btn');
    const shimmer = document.getElementById('shimmer-effect');
    
    // Masking State
    const brushBtn = document.getElementById('brush-tool');
    const eraserBtn = document.getElementById('eraser-tool');
    let isDrawing = false;
    let currentTool = 'brush'; // 'brush' or 'eraser'
    
    // Mask Canvas (Offscreen)
    const maskCanvas = document.createElement('canvas');
    const maskCtx = maskCanvas.getContext('2d');
    
    let originalImage = null;
    let selectedFabric = null;

    // --- LOCAL FABRIC TEXTURES ---
    const fabricTextures = [
        { id: 't1', url: 'images/fabric-samples/premium-velvet.jpg' },
        { id: 't2', url: 'images/fabric-samples/italian-leather.jpg' },
        { id: 't3', url: 'images/fabric-samples/premium-linen.jpg' },
        { id: 't4', url: 'images/fabric-samples/modern-tweed.jpg' },
        { id: 't5', url: 'images/fabric-samples/royal-silk.jpg' },
        { id: 't6', url: 'images/fabric-samples/cotton-canvas.jpg' },
        { id: 't7', url: 'images/fabric-samples/persian-camille.jpg' },
        { id: 't8', url: 'images/fabric-samples/Artisan-jacquard.jpg' }
    ];

    // --- NEW PROJECT LOGIC ---
    if (newProjectBtn) {
        newProjectBtn.onclick = () => {
            originalImage = null;
            selectedFabric = null;
            canvas.style.display = 'none';
            document.getElementById('upload-prompt').style.display = 'block';
            document.getElementById('visualizer-controls').classList.add('hidden');
            document.getElementById('ai-action-container').classList.add('hidden');
            document.getElementById('empty-state-msg').classList.remove('hidden');
            newProjectBtn.classList.add('hidden');
            aiProcessBtn.disabled = true;
            document.querySelectorAll('.fabric-circle').forEach(c => c.classList.remove('selected'));
        };
    }

    // --- TOOL SWITCHING ---
    if (brushBtn && eraserBtn) {
        brushBtn.onclick = () => {
            currentTool = 'brush';
            brushBtn.classList.add('bg-[#C5A059]', 'text-white');
            eraserBtn.classList.remove('bg-red-500', 'text-white');
        };
        eraserBtn.onclick = () => {
            currentTool = 'eraser';
            eraserBtn.classList.add('bg-red-500', 'text-white');
            brushBtn.classList.remove('bg-[#C5A059]', 'text-white');
        };
    }

    // --- MASK DRAWING LOGIC ---
    function getMousePos(e) {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {
            x: (e.clientX - rect.left) * scaleX,
            y: (e.clientY - rect.top) * scaleY
        };
    }

    canvas.onmousedown = (e) => {
        if (!originalImage) return;
        isDrawing = true;
        draw(e);
    };

    canvas.onmousemove = (e) => {
        if (isDrawing) draw(e);
    };

    window.onmouseup = () => {
        isDrawing = false;
        maskCtx.beginPath();
    };

    function draw(e) {
        const pos = getMousePos(e);
        maskCtx.lineWidth = 40;
        maskCtx.lineCap = 'round';
        maskCtx.lineJoin = 'round';

        if (currentTool === 'brush') {
            maskCtx.globalCompositeOperation = 'source-over';
            maskCtx.strokeStyle = 'white';
        } else {
            maskCtx.globalCompositeOperation = 'destination-out';
        }

        maskCtx.lineTo(pos.x, pos.y);
        maskCtx.stroke();
        maskCtx.beginPath();
        maskCtx.moveTo(pos.x, pos.y);
        renderFullPreview();
    }

    // --- FILE HANDLING ---
    fileInput.addEventListener('change', (e) => {
        if (e.target.files[0]) handleFile(e.target.files[0]);
    });

    function handleFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                originalImage = img;
                canvas.width = img.width;
                canvas.height = img.height;
                maskCanvas.width = img.width;
                maskCanvas.height = img.height;
                maskCtx.fillStyle = 'white';
                maskCtx.fillRect(0, 0, maskCanvas.width, maskCanvas.height);
                renderFullPreview();
                canvas.style.display = 'block';
                document.getElementById('upload-prompt').style.display = 'none';
                document.getElementById('visualizer-controls').classList.remove('hidden');
                document.getElementById('ai-action-container').classList.remove('hidden');
                document.getElementById('empty-state-msg').classList.add('hidden');
                if (newProjectBtn) newProjectBtn.classList.remove('hidden');
                aiProcessBtn.disabled = false;
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    // --- RENDER LOGIC ---
    function renderFullPreview() {
        if (!originalImage) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(originalImage, 0, 0);
        if (selectedFabric) applyFabricWithMask();
    }

    function applyFabricWithMask() {
        const texture = new Image();
        texture.onload = () => {
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = canvas.width;
            tempCanvas.height = canvas.height;
            const tempCtx = tempCanvas.getContext('2d');
            const pattern = tempCtx.createPattern(texture, 'repeat');
            tempCtx.fillStyle = pattern;
            tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
            tempCtx.globalCompositeOperation = 'destination-in';
            tempCtx.drawImage(maskCanvas, 0, 0);
            ctx.save();
            ctx.globalAlpha = 0.7;
            ctx.globalCompositeOperation = 'source-atop';
            ctx.drawImage(tempCanvas, 0, 0);
            ctx.restore();
            ctx.save();
            ctx.globalCompositeOperation = 'multiply';
            ctx.drawImage(originalImage, 0, 0);
            ctx.restore();
        };
        texture.src = selectedFabric;
    }

    function initFabricGrid() {
        fabricGrid.innerHTML = '';
        fabricTextures.forEach(fabric => {
            const circle = document.createElement('div');
            circle.className = 'fabric-circle';
            circle.style.backgroundImage = `url(${fabric.url})`;
            circle.onclick = () => {
                document.querySelectorAll('.fabric-circle').forEach(c => c.classList.remove('selected'));
                circle.classList.add('selected');
                selectedFabric = fabric.url;
                renderFullPreview();
            };
            fabricGrid.appendChild(circle);
        });
    }

    initFabricGrid();

    aiProcessBtn.onclick = () => {
        shimmer.style.display = 'block';
        setTimeout(() => {
            renderFullPreview();
            shimmer.style.display = 'none';
        }, 1500);
    };

    if (resetBtn) {
        resetBtn.onclick = () => {
            if (!originalImage) return;
            ctx.drawImage(originalImage, 0, 0);
            maskCtx.fillStyle = 'white';
            maskCtx.fillRect(0, 0, maskCanvas.width, maskCanvas.height);
            selectedFabric = null;
            document.querySelectorAll('.fabric-circle').forEach(c => c.classList.remove('selected'));
        };
    }
});
