document.addEventListener("DOMContentLoaded", function () {
  const customButton = document.getElementById("type-category-custom-button");
  const fileInput = document.getElementById("custom_file_input");
  const customText = document.getElementById("type-category-custom-text");

  customButton.addEventListener("click", function () {
    fileInput.click();
  });

  fileInput.addEventListener("change", function () {
    if (this.files.length > 0) {
      const fileName = this.files[0].name;
      customText.textContent = fileName;
    } else {
    }
  });
});
