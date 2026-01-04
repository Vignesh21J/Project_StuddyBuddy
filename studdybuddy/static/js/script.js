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