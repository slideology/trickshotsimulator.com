document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('chat-messages');
    const emojiButton = document.getElementById('emoji-button');
    const emojiPicker = document.getElementById('emoji-picker');
    const imageButton = document.getElementById('image-button');

    let isTyping = false;
    let typingTimeout;

    // Initialize emoji picker
    const picker = new EmojiMart.Picker({
        onEmojiSelect: (emoji) => {
            messageInput.value += emoji.native;
            emojiPicker.classList.remove('visible');
        }
    });
    emojiPicker.appendChild(picker);

    emojiButton.addEventListener('click', () => {
        emojiPicker.classList.toggle('visible');
    });

    document.addEventListener('click', (e) => {
        if (!emojiPicker.contains(e.target) && e.target !== emojiButton) {
            emojiPicker.classList.remove('visible');
        }
    });

    // Handle image generation
    imageButton.addEventListener('click', () => {
        const prompt = messageInput.value.trim();
        if (prompt) {
            socket.emit('generate_image', { prompt });
            messageInput.value = '';
            addMessage('Generating image...', true);
        }
    });

    function formatTimestamp() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function addMessage(content, isAI = false, imageUrl = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isAI ? 'ai-message' : 'user-message'}`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';

        if (isAI && content === 'Typing...') {
            const typingAnimation = document.createElement('div');
            typingAnimation.className = 'typing-animation';
            for (let i = 0; i < 3; i++) {
                const dot = document.createElement('span');
                dot.className = 'dot';
                typingAnimation.appendChild(dot);
            }
            messageContent.appendChild(typingAnimation);
        } else {
            const messageText = document.createElement('div');
            messageText.className = 'message-text';
            messageText.textContent = content;
            messageContent.appendChild(messageText);

            if (imageUrl) {
                const imageContainer = document.createElement('div');
                imageContainer.className = 'message-image';
                const image = document.createElement('img');
                image.src = imageUrl;
                image.alt = 'Generated image';
                imageContainer.appendChild(image);
                messageContent.appendChild(imageContainer);
            }
        }

        const timestamp = document.createElement('div');
        timestamp.className = 'message-time';
        timestamp.textContent = formatTimestamp();

        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(timestamp);
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function showTypingIndicator() {
        if (!isTyping) {
            isTyping = true;
            addMessage('Typing...', true);
        }
    }

    function hideTypingIndicator() {
        if (isTyping) {
            isTyping = false;
            const typingMessage = messagesContainer.querySelector('.message:last-child');
            if (typingMessage && typingMessage.querySelector('.typing-animation')) {
                messagesContainer.removeChild(typingMessage);
            }
        }
    }

    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        
        if (message) {
            addMessage(message, false);
            socket.emit('message', { message });
            messageInput.value = '';
            showTypingIndicator();
        }
    });

    socket.on('response', (data) => {
        hideTypingIndicator();
        addMessage(data.message, true);
    });

    socket.on('image_generated', (data) => {
        hideTypingIndicator();
        addMessage('Here\'s your generated image:', true, data.image_url);
    });

    socket.on('error', (data) => {
        hideTypingIndicator();
        addMessage('Error: ' + data.message, true);
    });

    socket.on('typing', () => {
        showTypingIndicator();
        clearTimeout(typingTimeout);
        typingTimeout = setTimeout(hideTypingIndicator, 3000);
    });
});
