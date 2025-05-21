document.addEventListener('DOMContentLoaded', () => {
    const chatIcon = document.getElementById('chat-icon');
    const chatContainer = document.getElementById('chat-container');
    const chatOverlay = document.querySelector('.chat-overlay');
    let isChatOpen = false;

    function loadHistory() {
        const messages = document.getElementById('chat-messages');
        messages.innerHTML = '';
        const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        history.forEach(msg => {
            const element = document.createElement('div');
            element.className = `message ${msg.type}-message`;
            element.textContent = msg.text;
            messages.appendChild(element);
        });
        messages.scrollTop = messages.scrollHeight;
    }

    function saveToHistory(text, type) {
        const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        history.push({ type, text, timestamp: Date.now() });
        if(history.length > 50) history.shift();
        localStorage.setItem('chatHistory', JSON.stringify(history));
    }

    function checkHistoryExpiry() {
        const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        const validHistory = history.filter(msg => Date.now() - msg.timestamp < 86400000);
        localStorage.setItem('chatHistory', JSON.stringify(validHistory));
    }

    function toggleChat() {
        isChatOpen = !isChatOpen;
        if(isChatOpen) {
            checkHistoryExpiry();
            loadHistory();
            chatContainer.style.display = 'flex';
            chatOverlay.style.display = 'block';
            setTimeout(() => {
                chatContainer.classList.add('active');
                document.getElementById('user-input').focus();
            }, 10);
        } else {
            chatContainer.classList.remove('active');
            setTimeout(() => {
                chatContainer.style.display = 'none';
                chatOverlay.style.display = 'none';
            }, 300);
        }
    }

    async function sendMessage() {
        const input = document.getElementById('user-input');
        const text = input.value.trim();
        if(!text) return;

        const messages = document.getElementById('chat-messages');
        const userMessage = document.createElement('div');
        userMessage.className = 'message user-message';
        userMessage.textContent = text;
        messages.appendChild(userMessage);
        saveToHistory(text, 'user');
        
        input.value = '';
        messages.scrollTop = messages.scrollHeight;

        try {
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'message bot-message typing-indicator';
            typingIndicator.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
            messages.appendChild(typingIndicator);
            messages.scrollTop = messages.scrollHeight;

            const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
            const formattedHistory = history.map(msg => ({
                role: msg.type === 'user' ? 'user' : 'model',
                parts: [{ text: msg.text }]
            }));

            const response = await fetch(CHAT_API_URL, {
                method: "POST",
                headers: {"Content-Type": "application/json", "X-CSRFToken": CSRF_TOKEN},
                body: JSON.stringify({
                    message: text,
                    history: formattedHistory.slice(0, -1)
                })
            });
            
            messages.removeChild(typingIndicator);
            const data = await response.json();
            const botMessage = document.createElement('div');
            botMessage.className = 'message bot-message';
            botMessage.textContent = data.reply;
            messages.appendChild(botMessage);
            saveToHistory(data.reply, 'bot');
            
        } catch(error) {
            console.error('Ошибка:', error);
            const errorMessage = document.createElement('div');
            errorMessage.className = 'message bot-message error-message';
            errorMessage.textContent = 'Ошибка соединения';
            messages.appendChild(errorMessage);
        }
        messages.scrollTop = messages.scrollHeight;
    }

    chatIcon?.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleChat();
    });

    document.querySelector('#chat-header button')?.addEventListener('click', toggleChat);
    document.querySelector('#chat-input button')?.addEventListener('click', sendMessage);

    document.getElementById('user-input')?.addEventListener('keypress', (e) => {
        if(e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    document.addEventListener('click', (e) => {
        if(isChatOpen && !chatContainer.contains(e.target) && !chatIcon.contains(e.target)) {
            toggleChat();
        }
    });

    chatContainer?.addEventListener('click', (e) => e.stopPropagation());
    checkHistoryExpiry();
});