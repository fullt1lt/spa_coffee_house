const url = window.location.href;

// Функция для установки класса на элемент body
function setBodyClass() {
  const body = document.body;
  const footer = document.getElementById("footer");
  const section = document.getElementById("Block_content");

  section.className = "";
  footer.className = "";
  body.className = "";

  // Примеры проверок URL и добавления соответствующего класса
  if (url.includes("spa_category")) {
    section.classList.add("Block_content");
    body.classList.add("Background_Categories");
    footer.classList.add("Background_Categories");
    footer.classList.add("Main_Footer");
  } else if (url.includes("cafe")) {
    section.classList.add("Block_info_content");
    body.classList.add("Background_Cafe_Categories");
    footer.classList.add("Background_Cafe_Categories");
    footer.classList.add("Main_Footer");
  } else if (url.includes("cafe-categories")) {
    section.classList.add("Block_info_content");
    body.classList.add("Background_Cafe_Categories");
    footer.classList.add("Background_Cafe_Categories");
    footer.classList.add("Main_Footer");
  } else if (url.includes("blog-news")) {
    section.classList.add("Block_info_content");
    body.classList.add("Background_Blog_News_Categories");
    footer.classList.add("Background_Blog_News_Categories");
    footer.classList.add("Main_Footer");
  } else if (url.includes("blog-news-categories")) {
    section.classList.add("Block_info_content");
    body.classList.add("Background_Blog_News_Categories");
    footer.classList.add("Background_Blog_News_Categories");
    footer.classList.add("Main_Footer");
  } else {
    footer.classList.add("Background_Main_Page_Footer");
    footer.classList.add("Main_Footer");
  }
}

// Вызов функции при загрузке страницы
window.onload = setBodyClass;
