// находим элемент body
const bodyElement = document.querySelector('.page');
// находим контейнер с меню
const menuElement = bodyElement.querySelector('.menu');
// находим кнопку меню
const menuButton = bodyElement.querySelector('.button-menu');
// находим кнопку закрытия меню
const menuCloseButton = bodyElement.querySelector('.menu__button-close');
// находим кнопку категорий
const buttonCategoriesElement = bodyElement.querySelector('.categories__button-title');
// находим список категорий
const listCategoriesElement = bodyElement.querySelector('.categories__list');
// находим все кнопки категорий
const categoriesItemLinks = bodyElement.querySelectorAll('.categories__button');
// находим наименование активной категории
const currentCategoriesElement = bodyElement.querySelector('.categories__current');
// находим кнопку Добавить комментарий
const buttonAddCommentsElement = bodyElement.querySelector('.comments__button');
// находим форму комментарий
const formCommentsElement = bodyElement.querySelector('.form_option_comments');
// находим кнопку Оформить заказ
const buttonOrderElement = bodyElement.querySelector('.cart__button-order');
// находим форму оформления заказа
const formOrderElement = bodyElement.querySelector('.form_option_order');


// swiper
const swiper = new Swiper('.swiper', {
  // Optional parameters
  slidesPerView: 1,
  spaceBetween: 30,
  direction: 'horizontal',
  loop: true,
  centeredSlides: true,
  autoplay: {
    delay: 4000,
    disableOnInteraction: false,
  },

  pagination: {
    el: ".swiper__pagination",
    clickable: true,
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper__button-next',
    prevEl: '.swiper__button-prev',
  },
});

// кнопка меню в мобильной версии
// функция открытия меню
function openMenu() {
  console.log(menuElement);
  menuElement.classList.add('menu_opened');
}

// функция закрытия меню
function closeMenu() {
  console.log(menuElement);
  menuElement.classList.remove('menu_opened');
}

// обработчик клика по кнопке меню
if (menuButton) {
  menuButton.addEventListener('click', () => {
    openMenu();
  });
}

// обработчик клика по кнопке закрытия меню
if (menuCloseButton) {
  menuCloseButton.addEventListener('click', () => {
    closeMenu();
  });
}


// выпадающая кнопка категорий
// функция открытия списка кнопок
function openListButtons() {
  listCategoriesElement.classList.toggle('categories__list_opened');
}

if (buttonCategoriesElement) {
  // обработчик клика по кнопке категорий
  buttonCategoriesElement.addEventListener('click', () => {
    openListButtons();
  })
}


// функция обнуления ссылок
function inactiveLink(link) {
  if (link.classList.contains('categories__button_active')) {
    link.classList.remove('categories__button_active')
  }
}

// функция активации ссылки
function activeLink(link) {
  link.classList.add('categories__button_active');
}

// добавляем класс активной ссылки нужному элементу
categoriesItemLinks.forEach((item) => {
  if (item.textContent === currentCategoriesElement.textContent) {
    activeLink(item)
  } else inactiveLink(item);
});


// функция открытия/закрытия формы 
function toggleForm(el, nameClass) {
  // formCommentsElement.classList.toggle('form_opened');
  el.classList.toggle(nameClass);
}

// функция изменения текста кнопки
// const changeText = (button, text) => {
//   if (button.textContent === 'Добавить комментарий') {
//     button.textContent = 'Скрыть форму';
//   } else {
//     button.textContent = 'Добавить комментарий';
//   };
// }
const changeText = (button, text) => {
  if (button.textContent === text) {
    button.textContent = 'Скрыть форму';
  } else {
    button.textContent = text;
  };
}

// обработчик клика по кнопке Добавить комментарий
if (buttonAddCommentsElement) {
  // обработчик клика по кнопке
  buttonAddCommentsElement.addEventListener('click', () => {
    toggleForm(formCommentsElement, 'form_opened');
    changeText(buttonAddCommentsElement, 'Добавить комментарий');
  });
}

// обработчик клика по кнопке Оформить заказ
if (buttonOrderElement) {
  // обработчик клика по кнопке
  buttonOrderElement.addEventListener('click', () => {
    toggleForm(formOrderElement, 'form_opened');
    changeText(buttonOrderElement, 'Оформить заказ');
  });
}
