//  CART SCRIPT FOR:
// 1. Product addition
// 2. Product deletion
// 3. Check if product is available
// 4. Modifying product quantity on cart
// 5. Calculating unique cart items on cart
// 6. Calculating subtotal
$(document).ready(function () {
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
    if (
      operation === "add" &&
      parseInt(item.val()) < parseInt(item.parent().parent().attr("stock"))
    ) {
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
        $(this).addClass("btn-disabled");
      } else if (cartItemsIds.includes($(this).parent().attr("data-id"))) {
        $(this).addClass("btn-disabled");
      } else {
        $(this).removeClass("btn-disabled");
      }
    });
  }
  cartButtonStatus();

  // Function to add item to cart
  function addItemsToCart(productName, product, price, img) {
    const dataName = product.attr("data-name");
    const stock = product.attr("stock");
    const dataId = product.attr("data-id");
    const newCartItem =
      $(`<article class="cart-item data-name="${dataName}" data-id="${dataId}" stock=${stock}>
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
    if ($(".cart-item").length > 0) {
      $(".subtotal, .disclaimer").show();
      $(".checkout").prop("disabled", false);
    }
    calculateSubtotal();
  }
  //  Add items to cart from product section
  $(".product .add-to-cart").click(function (event) {
    event.stopPropagation();
    if ($(this).hasClass("btn-disabled")) return;
    const product = $(this).parent();
    const img = $(this).siblings("img").attr("src");
    const productName = $(this).siblings("h3").text();
    const price = $(this).prev("p").text();
    addItemsToCart(productName, product, price, img);
    cartButtonStatus();
  });

  // Add item to cart from saved items page
  $(".saved-item .add-to-cart").click(function (event) {
    event.stopPropagation();
    if ($(this).hasClass("btn-disabled")) return;
    const product = $(this).parent();
    const img = $(this)
      .siblings(".saved-item-details")
      .children("a")
      .children("img")
      .attr("src");
    const productName = $(this)
      .siblings(".saved-item-details")
      .children(".price-and-name")
      .children("h3")
      .text();
    const price = $(this)
      .siblings(".saved-item-details")
      .children(".price-and-name")
      .children("span")
      .text();
    addItemsToCart(productName, product, price, img);
    cartButtonStatus();
  });
});
