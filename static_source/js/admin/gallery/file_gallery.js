document.addEventListener("DOMContentLoaded", function () {
  const customButton = document.getElementById("gallery-custom-button");
  const customText = document.getElementById("gallery-custom-text");
  const fileInput = document.querySelector('input[name="gallery_image"]');

  if (customButton && customText && fileInput) {
    customButton.addEventListener("click", function () {
      fileInput.click();
    });

    fileInput.addEventListener("change", function () {
      if (fileInput.files.length > 0) {
        customText.textContent = fileInput.files[0].name;
      } else {
        customText.textContent = "Файл не вибрано";
      }
    });
  }
});
