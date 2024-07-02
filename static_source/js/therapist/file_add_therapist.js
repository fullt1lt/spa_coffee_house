document
  .getElementById("id_Therapist_image")
  .addEventListener("change", function () {
    var fileName = this.files[0] ? this.files[0].name : "Файл не выбран";
    document.getElementById("file-name").textContent = fileName;
  });
