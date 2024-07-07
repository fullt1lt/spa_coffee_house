document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".Basket_Gallery_image").forEach((button) => {
    button.addEventListener("click", (event) => {
      document.querySelectorAll(".Gallery_delete_item_list").forEach((form) => {
        form.style.display = "none";
      });
      const galleryId = button.getAttribute("delete-gallery-id");
      const deleteForm = document.getElementById(`gallery_delete_${galleryId}`);
      if (deleteForm) {
        deleteForm.style.display = "flex";
      }
    });
  });

  document.querySelectorAll(".cancel_delete_gallery").forEach((button) => {
    button.addEventListener("click", (event) => {
      const galleryId = button.getAttribute("cancel-delete-gallery-id");
      const deleteForm = document.getElementById(`gallery_delete_${galleryId}`);
      if (deleteForm) {
        deleteForm.style.display = "none";
      }
    });
  });
});
