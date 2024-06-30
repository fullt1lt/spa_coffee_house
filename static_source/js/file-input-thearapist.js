document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".file-input").forEach((input) => {
    input.addEventListener("change", function () {
      const fileName = this.files[0] ? this.files[0].name : "Файл не вибрано";
      const fileLabel = document.getElementById(
        `file-name-${this.id.split("_")[2]}`
      );
      fileLabel.textContent = fileName;
    });
  });
});
