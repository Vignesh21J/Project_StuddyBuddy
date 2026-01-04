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