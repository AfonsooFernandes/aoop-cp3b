document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector('#chat-form');
    const perguntaInput = document.querySelector('#pergunta');
    const chatBox = document.querySelector('#chat-box');
    const typingIndicator = document.querySelector('#typing-indicator');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const pergunta = perguntaInput.value.trim();
        if (!pergunta) return;

        chatBox.innerHTML += `
            <div class="chat-message user-message">
                <strong>🧑 Tu:</strong> ${pergunta}
            </div>
        `;
        chatBox.scrollTop = chatBox.scrollHeight;
        perguntaInput.value = '';

        typingIndicator.style.display = 'flex';
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pergunta })
            });

            if (!response.ok) {
                throw new Error("Erro na resposta da API");
            }

            const data = await response.json();
            const resposta = data.resposta?.trim() || "❌ Erro ao processar a resposta.";

            typingIndicator.style.display = 'none';

            chatBox.innerHTML += `
                <div class="chat-message bot-message">
                    <strong>🤖 Bot:</strong> ${resposta}
                </div>
            `;
            chatBox.scrollTop = chatBox.scrollHeight;

        } catch (error) {
            typingIndicator.style.display = 'none';

            console.error("Erro ao chamar a API:", error);
            chatBox.innerHTML += `
                <div class="chat-message bot-message">
                    <strong>🤖 Bot:</strong> ❌ Ocorreu um erro ao obter a resposta. Tenta novamente.
                </div>
            `;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    });
});