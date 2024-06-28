document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".Basket_image").forEach((button) => {
    button.addEventListener("click", (event) => {
      document
        .querySelectorAll(".Categories_delete_item_list")
        .forEach((form) => {
          form.style.display = "none";
        });
      const categoryId = button.getAttribute("delete-category-id");
      const deleteForm = document.getElementById(
        `categories_delete_${categoryId}`
      );
      if (deleteForm) {
        deleteForm.style.display = "flex";
      }
    });
  });

  document.querySelectorAll(".cancel_delete").forEach((button) => {
    button.addEventListener("click", (event) => {
      const categoryId = button.getAttribute("cancel-delete-category-id");
      const deleteForm = document.getElementById(
        `categories_delete_${categoryId}`
      );
      if (deleteForm) {
        deleteForm.style.display = "none";
      }
    });
  });
});
