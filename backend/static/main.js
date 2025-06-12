document.getElementById("chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const perguntaInput = document.getElementById("pergunta");
  const pergunta = perguntaInput.value.trim();
  if (!pergunta) return;

  const chatBox = document.getElementById("chat-box");

  const userMessage = document.createElement("div");
  userMessage.className = "chat-message user-message";
  userMessage.innerHTML = `<strong>🧑 Tu:</strong> ${pergunta}`;
  chatBox.appendChild(userMessage);

  perguntaInput.value = "";

  const typingIndicator = document.createElement("div");
  typingIndicator.className = "typing-indicator";
  typingIndicator.innerHTML = `<span></span><span></span><span></span>`;
  chatBox.appendChild(typingIndicator);
  typingIndicator.style.display = "flex";

  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta })
    });

    typingIndicator.remove();

    const data = await response.json();
    const resposta = data.resposta;

    const botMessage = document.createElement("div");
    botMessage.className = "chat-message bot-message";
    botMessage.innerHTML = `<strong>🤖 Bot:</strong> ${resposta}`;
    chatBox.appendChild(botMessage);
  } catch (error) {
    typingIndicator.remove();

    const errorMessage = document.createElement("div");
    errorMessage.className = "chat-message error-message";
    errorMessage.innerHTML = `❌ Erro ao contactar o backend.`;
    chatBox.appendChild(errorMessage);
  }

  chatBox.scrollTop = chatBox.scrollHeight;
});