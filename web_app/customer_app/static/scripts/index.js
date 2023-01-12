//  SCRIPT FOR:
// 1. Banner animation
// 2. Cart function
$("document").ready(function () {
  // Scroll to the top of the window
  $(window).stop(true, true);
  // START OF BANNER ANIMATION
  let slideIndex = 0;
  let timer;
  showSlides(slideIndex);

  // Next and previous control
  function nextSlide(n) {
    clearTimeout(timer);
    showSlides((slideIndex += n));
  }
  // Thumbnail image control
  function currentSlide(n) {
    clearTimeout(timer);
    showSlides((slideIndex = n));
  }

  //   Main slide navigation function
  function showSlides(n) {
    let slides = $(".slide");
    if (typeof n === "string") n = parseInt(n);
    let thumbnails = $(".banner-nav");
    if (n >= slides.length) slideIndex = 0;
    else if (n < 0) slideIndex = slides.length - 1;
    else slideIndex = n;
    slides.hide();
    thumbnails.removeClass("active");
    $(slides[slideIndex]).show();
    $(thumbnails[slideIndex]).toggleClass("active");

    timer = setTimeout(() => {
      showSlides(++slideIndex);
    }, 5000);
  }

  //   Assigned functions for click events
  $(".next").click(() => nextSlide(1));
  $(".prev").click(() => nextSlide(-1));
  $(".banner-nav").click(function () {
    const idx = $(this).attr("slide-idx");
    currentSlide(idx);
  });
  // END OF BANNER ANIMATION

  // START OF SHOP NOW BUTTON
  $("#shop-now").click(() => {
    $(window).scrollTop(410);
  });
  // END OF SHOP NOW BUTTON

  // START OF CART
  const itemsOnCart = $(".cart-num");
  const subtotalElement = $(".cart-subtotal");
  let cartItemsIds = [];

  // Get ids of items in cart
  $(".cart-item").each(function () {
    cartItemsIds.push($(this).attr("data-id"));
  });

  // Subtotal calculation
  function calculateSubtotal() {
    // let subtotal = parseFloat(subtotalElement.val.slice(1));
    let subtotal = 0;
    const cartItems = $(".cart-item");
    itemsOnCart.text(`Cart(${cartItems.length})`);
    cartItems.each(function () {
      const price = parseFloat($(this).children(".price").text().slice(1));
      const quantity = parseInt(
        $(this).children(".add-subtract").children(".quantity").val()
      );
      subtotal += price * quantity;
    });
    subtotalElement.text(`$${subtotal.toFixed(2)}`);
  }
  calculateSubtotal();

  // Add or subtract quantity of cart item
  function addOrSubtract(item, operation) {
    if (operation === "add") {
      item.val(parseInt(item.val()) + 1);
    }
    if (operation === "subtract" && parseInt(item.val()) > 1) {
      item.val(parseInt(item.val()) - 1);
    }
    calculateSubtotal();
  }
  $(document).on("click", ".add", function () {
    addOrSubtract($(this).prev(), "add");
  });

  $(document).on("click", ".subtract", function () {
    addOrSubtract($(this).next(), "subtract");
  });
  // Edit input
  $(".quantity").click(function () {
    $(this).prop("disabled", false);
  });

  // Delete cart-item
  $(document).on("click", ".delete-item", function () {
    cartItemsIds = cartItemsIds.filter(
      (id) => id !== $(this).parent().attr("data-id")
    );
    $(this).parent().remove();
    calculateSubtotal();
    if ($(".cart-item").length === 0) {
      $(".subtotal, .disclaimer").hide();
      $(".checkout").prop("disabled", true);
    }
    cartButtonStatus();
  });

  // Disable add to cart button if item
  // is already in the cart or item is
  // in stock Check item stock
  function cartButtonStatus() {
    const addToCartButtons = $(".add-to-cart");
    addToCartButtons.each(function () {
      if (parseInt($(this).parent().attr("stock")) === 0) {
        $(this).prop("disabled", true);
      } else if (cartItemsIds.includes($(this).parent().attr("data-id"))) {
        $(this).prop("disabled", true);
      } else {
        $(this).prop("disabled", false);
      }
    });
  }
  cartButtonStatus();

  // Add item to cart
  $(".product .add-to-cart").click(function (event) {
    event.stopPropagation();
    const product = $(this).parent();
    const img = $(this).siblings("img").attr("src");
    const productName = $(this).siblings("h3").text();
    const price = $(this).prev("p").text();
    const dataName = product.attr("data-name");
    const dataId = product.attr("data-id");
    const newCartItem =
      $(`<article class="cart-item data-name="${dataName}" data-id="${dataId}">
          <img src="${img}" />
          <h3>${productName}</h3>
          <span class="price" data-name="price">${price}</span>
          <div class="add-subtract">
            <i class="fa-solid fa-minus fa-lg subtract"></i>
            <input type="text" class="quantity" disabled value="1" />
            <i class="fa-solid fa-plus fa-lg add"></i>
          </div>
          <i class="fa-solid fa-trash-can fa-lg delete-item"></i>
        </article>`);
    $(".cart-container").append(newCartItem);
    cartItemsIds.push(dataId);
    cartButtonStatus();
    if ($(".cart-item").length > 0) {
      $(".subtotal, .disclaimer").show();
      $(".checkout").prop("disabled", false);
    }
    calculateSubtotal();
  });
  // END OF CART
});
