/**
 * Al Meeran Global AI Assistant - Gemini Powered
 */

(function() {
    const assistantID = 'meeran-ai-root';
    if (document.getElementById(assistantID)) return;

    function createAssistant() {
        const root = document.createElement('div');
        root.id = assistantID;
        root.style.cssText = 'position: fixed; bottom: 30px; right: 30px; z-index: 2147483647; font-family: sans-serif;';
        
        const shadow = root.attachShadow({mode: 'open'});

        const styles = `
            .btn { width: 60px; height: 60px; background: #1A2238; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 10px 30px rgba(0,0,0,0.4); border: 2px solid #C5A059; transition: 0.3s; }
            .btn:hover { transform: scale(1.1); background: #C5A059; }
            .btn svg { width: 28px; height: 28px; fill: #C5A059; transition: 0.3s; }
            .btn:hover svg { fill: white; }
            
            .window { position: absolute; bottom: 80px; right: 0; width: 300px; height: 400px; background: white; border-radius: 15px; box-shadow: 0 20px 50px rgba(0,0,0,0.3); display: none; flex-direction: column; overflow: hidden; border: 1px solid #eee; }
            .window.active { display: flex; }
            .header { background: #1A2238; color: white; padding: 15px; display: flex; align-items: center; justify-content: space-between; }
            .chat { flex-grow: 1; padding: 15px; overflow-y: auto; background: #f8f9fa; display: flex; flex-direction: column; gap: 10px; }
            .bubble { padding: 10px 14px; border-radius: 12px; font-size: 12px; max-width: 85%; word-wrap: break-word; }
            .asst { background: #eee; color: #1A2238; align-self: flex-start; }
            .user { background: #C5A059; color: white; align-self: flex-end; }
            .typing { font-style: italic; color: #888; font-size: 10px; }
            .footer { padding: 10px; border-top: 1px solid #eee; display: flex; gap: 5px; }
            input { flex-grow: 1; border: none; outline: none; font-size: 12px; }
            button { background: none; border: none; color: #C5A059; font-weight: bold; cursor: pointer; }
        `;

        shadow.innerHTML = `
            <style>${styles}</style>
            <div class="window" id="win">
                <div class="header">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="width:8px; height:8px; background:#4CAF50; border-radius:50%;"></div>
                        <span style="font-weight:bold; font-size:11px; letter-spacing:1px;">MEERAN AI</span>
                    </div>
                    <button id="close" style="color:white; border:none; background:none; cursor:pointer; font-size:16px;">✕</button>
                </div>
                <div class="chat" id="chat">
                    <div class="bubble asst">Salam! I am Meeran AI, your furniture restoration expert. How can I assist you today?</div>
                </div>
                <div class="footer">
                    <input type="text" id="input" placeholder="Ask about upholstery, fabrics...">
                    <button id="send">Send</button>
                </div>
            </div>
            <div class="btn" id="toggle">
                <svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            </div>
        `;

        const win = shadow.getElementById('win');
        const chat = shadow.getElementById('chat');
        const input = shadow.getElementById('input');

        shadow.getElementById('toggle').onclick = () => win.classList.toggle('active');
        shadow.getElementById('close').onclick = () => win.classList.remove('active');
        
        async function send() {
            const v = input.value.trim();
            if(!v) return;

            // User message
            const u = document.createElement('div'); 
            u.className='bubble user'; 
            u.textContent=v; 
            chat.appendChild(u);
            input.value='';
            chat.scrollTop = chat.scrollHeight;

            // Typing indicator
            const typing = document.createElement('div');
            typing.className = 'bubble asst typing';
            typing.textContent = 'Thinking...';
            chat.appendChild(typing);
            chat.scrollTop = chat.scrollHeight;

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: v })
                });
                const data = await response.json();
                
                chat.removeChild(typing);
                const a = document.createElement('div'); 
                a.className='bubble asst'; 
                a.textContent = data.reply || "I'm sorry, I couldn't process that.";
                chat.appendChild(a);
            } catch (error) {
                chat.removeChild(typing);
                const e = document.createElement('div'); 
                e.className='bubble asst'; 
                e.textContent = "Offline. Please ensure the Al Meeran server is running.";
                chat.appendChild(e);
            }
            chat.scrollTop = chat.scrollHeight;
        }

        shadow.getElementById('send').onclick = send;
        input.onkeydown = (e) => { if(e.key === 'Enter') send(); };

        document.body.appendChild(root);
    }

    if (document.readyState === 'complete') createAssistant();
    else window.addEventListener('load', createAssistant);
})();
