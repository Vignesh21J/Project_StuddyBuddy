setTimeout(() => {
    const messages = document.querySelectorAll('.message');
    messages.forEach((message) => {
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 400);
    })
}, 3000)