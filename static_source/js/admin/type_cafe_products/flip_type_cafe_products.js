document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll(".Update_TypeCafeProduct_image")
    .forEach((button) => {
      button.addEventListener("click", (event) => {
        const typeCafeProductId = button.getAttribute(
          "update-type_cafe_product-id"
        );
        const frontCard = document.getElementById(
          `type_cafe_product_front_${typeCafeProductId}`
        );
        const backCard = document.getElementById(
          `type_cafe_product_back_${typeCafeProductId}`
        );

        rotateAllCardsToFront();
        if (frontCard && backCard) {
          frontCard.style.transform = "rotateY(-180deg)";
          backCard.style.transform = "rotateY(0deg)";

          // Заполнение формы
          const nameField = backCard.querySelector(
            '.update-form-control-type-cafe-product[name="name"]'
          );
          if (nameField) {
            const nameText =
              frontCard.querySelector(".item_header h2").innerText;
            nameField.value = nameText;
          }
        }
      });
    });

  document
    .querySelectorAll(".Cloose_type_cafe_product_image")
    .forEach((button) => {
      button.addEventListener("click", (event) => {
        const typeCafeProductId = button.getAttribute(
          "close-type_cafe_product-id"
        );
        const frontCard = document.getElementById(
          `type_cafe_product_front_${typeCafeProductId}`
        );
        const backCard = document.getElementById(
          `type_cafe_product_back_${typeCafeProductId}`
        );

        if (frontCard && backCard) {
          frontCard.style.transform = "rotateY(0deg)";
          backCard.style.transform = "rotateY(180deg)";
        }
      });
    });

  function rotateAllCardsToFront() {
    document
      .querySelectorAll(".TypeCafeProduct_item_list")
      .forEach((frontCard) => {
        frontCard.style.transform = "rotateY(0deg)";
      });

    document
      .querySelectorAll(".TypeCafeProduct_update_item_list")
      .forEach((backCard) => {
        backCard.style.transform = "rotateY(180deg)";
      });
  }
});
