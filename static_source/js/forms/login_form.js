const cloose_button_login = document.getElementById("cloose_button_login");
const active_button_login = document.getElementById("active_button_login");
const active_button_register_in_login = document.getElementById(
  "active_button_register_in_login"
);
const login_form = document.getElementById("login_form");

cloose_button_login.addEventListener("click", function () {
  login_form.style.display = "none";
});

active_button_login.addEventListener("click", function () {
  login_form.style.display = "flex";
});

active_button_register_in_login.addEventListener("click", function () {
  register_form.style.display = "flex";
  login_form.style.display = "none";
});