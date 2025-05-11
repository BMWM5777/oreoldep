document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById("chat-box");
    const form = document.getElementById("chat-form");
    const input = document.getElementById("user-message");
    const url = window.CHATBOT_API_URL;
    const clearUrl = window.CHATBOT_CLEAR_URL;
    const chatWindowEl = document.getElementById("chatWindow");
  
    fetch(url, { method: 'GET' })
      .then(r => {
        if (r.status === 401) {
          appendSystem("Пожалуйста, войдите, чтобы обратиться к консультанту.");
          form.querySelector('input').disabled = true;
          form.querySelector('button').disabled = true;
          throw "no-auth";
        }
        return r.json();
      })
      .then(data => {
        if (data.history) {
          data.history.forEach(msg => {
            appendMessage(msg.from, msg.text);
          });
        }
      })
      .catch(console.warn);
  
    form.addEventListener("submit", async e => {
      e.preventDefault();
      const msg = input.value.trim();
      if (!msg) return;
      appendMessage("user", msg);
      input.value = "";
      
      const typingIndicator = appendTypingIndicator();
  
      try {
        const resp = await fetch(url, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: `message=${encodeURIComponent(msg)}`
        });
        const data = await resp.json();
        if (typingIndicator && typingIndicator.parentNode) {
          typingIndicator.parentNode.removeChild(typingIndicator);
        }
        if (resp.ok) {
          appendMessage("bot", data.response);
        } else {
          appendSystem("Ошибка: " + (data.error || data.response));
        }
      } catch {
        if (typingIndicator && typingIndicator.parentNode) {
          typingIndicator.parentNode.removeChild(typingIndicator);
        }
        appendSystem("Не удалось получить ответ. Попробуйте позже.");
      }
    });
  
    const clearBtn = document.getElementById('clear-chat');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        showConfirmation();
      });
    }
  
    function showConfirmation() {
      const confirmationModal = document.createElement('div');
      confirmationModal.className = "confirmation-modal";
      confirmationModal.innerHTML = `
        <div class="confirmation-box">
          <p>Вы точно хотите очистить чат?</p>
          <div class="confirmation-buttons">
            <button class="confirm-clear">Очистить</button>
            <button class="cancel-clear">Отмена</button>
          </div>
        </div>
      `;
      chatWindowEl.appendChild(confirmationModal);
      setTimeout(() => {
        confirmationModal.classList.add('show');
      }, 50);
  
      confirmationModal.querySelector('.confirm-clear').addEventListener('click', async () => {
        try {
          const resp = await fetch(clearUrl, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
          });
          if (resp.ok) {
            chatBox.innerHTML = '';
            appendSystem('История чата очищена.');
          } else {
            appendSystem('Не удалось очистить историю.');
          }
        } catch {
          appendSystem('Ошибка при очистке чата.');
        }
        setTimeout(() => {
          chatWindowEl.removeChild(confirmationModal);
        }, 300);
      });
  
      confirmationModal.querySelector('.cancel-clear').addEventListener('click', () => {
        confirmationModal.classList.remove('show');
        setTimeout(() => {
          chatWindowEl.removeChild(confirmationModal);
        }, 300);
      });
    }
  
    function appendMessage(who, text) {
      const div = document.createElement("div");
      div.className = `message ${who}-message`;
      div.innerHTML = `<strong>${who === "user" ? "Вы" : "Консультант"}:</strong> ${text}`;
      chatBox.appendChild(div);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    function appendSystem(text) {
      const div = document.createElement("div");
      div.className = "message system-message";
      div.innerHTML = text;
      chatBox.appendChild(div);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    function appendTypingIndicator() {
      const div = document.createElement("div");
      div.className = "message typing-indicator";
      div.innerHTML = `<strong>Консультант:</strong> <span class="dots"><span>.</span><span>.</span><span>.</span></span>`;
      chatBox.appendChild(div);
      chatBox.scrollTop = chatBox.scrollHeight;
      return div;
    }
  
    function getCookie(name) {
      let cookieValue = null;
      document.cookie.split(";").forEach(c => {
        c = c.trim();
        if (c.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(c.substring(name.length + 1));
        }
      });
      return cookieValue;
    }
  
    document.addEventListener('click', function (e) {
      const chatContainer = document.getElementById('chatContainer');
      if (chatContainer && !chatContainer.contains(e.target)) {
        const chatWindow = document.getElementById('chatWindow');
        if (chatWindow.classList.contains('show')) {
          toggleChat();
        }
      }
    });
  });
  
  function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    const chatButton = document.querySelector('.chat-button');
    chatWindow.classList.toggle('show');
    chatButton.classList.toggle('active');
  }
  