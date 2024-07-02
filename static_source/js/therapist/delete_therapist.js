document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".Basket_therapist_image").forEach((button) => {
    button.addEventListener("click", (event) => {
      document
        .querySelectorAll(".Therapist_delete_item_list")
        .forEach((form) => {
          form.style.display = "none";
        });
      const categoryId = button.getAttribute("delete-therapist-id");
      const deleteForm = document.getElementById(
        `therapist_delete_${categoryId}`
      );
      if (deleteForm) {
        deleteForm.style.display = "flex";
      }
    });
  });

  document.querySelectorAll(".therapist_cancel_delete").forEach((button) => {
    button.addEventListener("click", (event) => {
      const categoryId = button.getAttribute("cancel-delete-therapist-id");
      const deleteForm = document.getElementById(
        `therapist_delete_${categoryId}`
      );
      if (deleteForm) {
        deleteForm.style.display = "none";
      }
    });
  });
});
