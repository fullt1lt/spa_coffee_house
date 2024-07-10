document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("next")) {
    document.getElementById("login_form").style.display = "flex";
  }
});
