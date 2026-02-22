/**
 * Al Meeran Global AI Assistant - GUARANTEED GLOBAL VERSION
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
            .bubble { padding: 10px 14px; border-radius: 12px; font-size: 12px; max-width: 85%; }
            .asst { background: #eee; color: #1A2238; align-self: flex-start; }
            .user { background: #C5A059; color: white; align-self: flex-end; }
            .footer { padding: 10px; border-top: 1px solid #eee; display: flex; gap: 5px; }
            input { flex-grow: 1; border: none; outline: none; font-size: 12px; }
            button { background: none; border: none; color: #C5A059; font-weight: bold; cursor: pointer; }
        `;

        shadow.innerHTML = `
            <style>${styles}</style>
            <div class="window" id="win">
                <div class="header"><span style="font-weight:bold; font-size:11px;">MEERAN AI</span><button id="close" style="color:white; border:none; background:none; cursor:pointer;">✕</button></div>
                <div class="chat" id="chat"><div class="bubble asst">Salam! I am your Al Meeran expert. How can I help?</div></div>
                <div class="footer"><input type="text" id="input" placeholder="Ask anything..."><button id="send">Send</button></div>
            </div>
            <div class="btn" id="toggle"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg></div>
        `;

        const win = shadow.getElementById('win');
        const chat = shadow.getElementById('chat');
        const input = shadow.getElementById('input');

        shadow.getElementById('toggle').onclick = () => win.classList.toggle('active');
        shadow.getElementById('close').onclick = () => win.classList.remove('active');
        
        function send() {
            const v = input.value.trim();
            if(!v) return;
            const u = document.createElement('div'); u.className='bubble user'; u.textContent=v; chat.appendChild(u);
            input.value='';
            setTimeout(() => {
                const a = document.createElement('div'); a.className='bubble asst'; 
                a.textContent="Our experts are here to help. You can explore our Shop or request a Quote!";
                chat.appendChild(a); chat.scrollTop = chat.scrollHeight;
            }, 600);
        }
        shadow.getElementById('send').onclick = send;
        input.onkeydown = (e) => { if(e.key === 'Enter') send(); };

        document.body.appendChild(root);
    }

    if (document.readyState === 'complete') createAssistant();
    else window.addEventListener('load', createAssistant);
})();
