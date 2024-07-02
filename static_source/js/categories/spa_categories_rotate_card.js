document.addEventListener("DOMContentLoaded", () => {
  const updateButtons = document.querySelectorAll(".Update_image");

  updateButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const categoryId = this.getAttribute("update-category-id");

      // Переворачиваем все карточки на фронтальную часть
      document
        .querySelectorAll(".Categories_content_item_list")
        .forEach((frontCard) => {
          frontCard.style.transform = "rotateY(0deg)";
        });
      document.querySelectorAll(".label_upload_block").forEach((frontCard) => {
        frontCard.style.transform = "rotateY(180deg)";
      });
      document
        .querySelectorAll(".Categories_update_item_list")
        .forEach((backCard) => {
          backCard.style.transform = "rotateY(180deg)";
        });

      const categoryFront = document.getElementById(
        `categories_front_${categoryId}`
      );
      const categoryBack = document.getElementById(
        `categories_back_${categoryId}`
      );
      const label_upload_block = document.getElementById(
        `label_upload_block_${categoryId}`
      );

      // Обновляем форму данными из карточки
      const categoryData = JSON.parse(
        categoryFront.getAttribute("data-category")
      );
      const form = categoryBack.querySelector("form");

      form.querySelector('[name="name"]').value = categoryData.name;
      form.querySelector('[name="description"]').value =
        categoryData.description;

      const imgInput = form.querySelector('[name="categories_image"]');
      let imgPreview = form.querySelector(".img-preview");
      if (categoryData.categories_image) {
        if (!imgPreview) {
          imgPreview = document.createElement("img");
          imgPreview.classList.add("img-preview");
          imgInput.parentNode.insertBefore(imgPreview, imgInput.nextSibling);
        }
        imgPreview.src = categoryData.categories_image;
        imgPreview.alt = "Category Image";
      } else {
        if (imgPreview) {
          imgPreview.remove();
        }
      }

      if (categoryFront) {
        categoryFront.style.transform = "rotateY(-180deg)";
      }

      if (categoryBack) {
        categoryBack.style.transform = "rotateY(0deg)";
      }
      if (label_upload_block) {
        label_upload_block.style.transform = "rotateY(0deg)";
      }
    });
  });

  const closeButtons = document.querySelectorAll(".Cloose_image");

  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const categoryId = this.getAttribute("close-category-id");

      const categoryFront = document.getElementById(
        `categories_front_${categoryId}`
      );
      const categoryBack = document.getElementById(
        `categories_back_${categoryId}`
      );

      const label_upload_block = document.getElementById(
        `label_upload_block_${categoryId}`
      );

      if (categoryFront) {
        categoryFront.style.transform = "rotateY(0deg)";
      }

      if (categoryBack) {
        categoryBack.style.transform = "rotateY(180deg)";
      }

      if (label_upload_block) {
        label_upload_block.style.transform = "rotateY(180deg)";
      }
    });
  });
});
