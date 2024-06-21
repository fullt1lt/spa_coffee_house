const cloose_button_register = document.getElementById("cloose_button_register");
const active_button_register = document.getElementById("active_button_register");
const active_button_login_in_registr = document.getElementById("active_button_login_in_registr");
const register_form = document.getElementById("register_form");

cloose_button_register.addEventListener("click", function () {
  register_form.style.display = "none";
});

active_button_register.addEventListener("click", function () {
  register_form.style.display = "flex";
});

active_button_login_in_registr.addEventListener("click", function () {
  register_form.style.display = "none";
  login_form.style.display = "flex";
});
