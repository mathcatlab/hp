
const btn = document.querySelector(".hamburger-menu");
const nav = document.querySelector(".nav-contents");

btn.addEventListener("click", () => {
  nav.classList.toggle("open");
  if (btn.innerHTML === "Menu") {
    btn.innerHTML = "Close";
  } else {
    btn.innerHTML = "Menu";
  }
});
