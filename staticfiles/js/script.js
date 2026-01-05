setTimeout(() => {
    const messages = document.querySelectorAll('.message');
    messages.forEach((message) => {
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 400);
    })
}, 3000)


// Menu DropDown Button
const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
    dropdownButton.addEventListener("click", () => {
        dropdownMenu.classList.toggle("show");
    });
}


// Eye Icon Toggle while Registering
document.querySelectorAll(".toggle-password").forEach(icon => {
    icon.addEventListener("click", () => {
        const input = document.getElementById(icon.dataset.target);

        if (input.type === "password") {
            input.type = "text";
            icon.classList.remove("bi-eye");
            icon.classList.add("bi-eye-slash");
        } else {
            input.type = "password";
            icon.classList.remove("bi-eye-slash");
            icon.classList.add("bi-eye");
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file-upload');
    const fileCountSpan = document.getElementById('file-count');
    const chatForm = document.querySelector('.chat-form');

    if (fileInput && fileCountSpan) {

        fileInput.addEventListener('change', () => {
            const count = fileInput.files.length;

            if (count === 0) {
                fileCountSpan.textContent = '';
            } else if (count === 1) {
                fileCountSpan.textContent = '1 file selected';
            } else {
                fileCountSpan.textContent = `${count} files selected`;
            }
        });
    }

    if (chatForm && fileCountSpan) {
        chatForm.addEventListener('submit', () => {
            fileCountSpan.textContent = '';
        });
    }
});


const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;