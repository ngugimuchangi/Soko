$("document").ready(function () {
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

  //   Assigned fuctions for click events
  $(".next").click(() => nextSlide(1));
  $(".prev").click(() => nextSlide(-1));
  $(".banner-nav").click(function () {
    const idx = $(this).attr("slide-idx");
    currentSlide(idx);
  });
  // END OF BANNER ANIMATION

  // START OF CART
  const itemsOnCart = $(".cart-num");
  const subtotalElement = $(".cart-subtotal");
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
  $(".add").click(function () {
    addOrSubtract($(this).prev(), "add");
  });
  $(".subtract").click(function () {
    addOrSubtract($(this).next(), "subtract");
  });

  // Delete cart-item
  $(".delete-item").click(function () {
    $(this).parent().remove();
    calculateSubtotal();
    if ($(".cart-item").length === 0) {
      $(".subtotal, .disclaimer").hide();
      $(".checkout").prop("disabled", true);
    }
  });
  // END OF CART

  // START OF MESSANGER
  // Socket integration to be done
  // Opening and closing chat section
  const toggleArrow = $(".arrow");
  const chatHistory = $(".chat-history");
  const chatList = $(".chats");
  let toggleSection = chatList;
  let headerContent = $(".message-header .fa-message");
  let tempContent;
  toggleArrow.click(function () {
    $(this).toggleClass("fa-angles-up fa-angles-down");
    $(".messanger").toggleClass("messanger-size");
    $(".message-header").toggleClass("message-header-properties");
    toggleSection.toggle();
    if (toggleSection.hasClass("chat-active")) {
      $(".back-to-chat-list").click(() => goBack());
      $(".back-to-chat-list").toggle();
    }
  });

  // Loading messages
  const chat = $(".chat");
  chat.click(function (event) {
    event.stopPropagation();
    toggleSection.hide();
    toggleSection = $(".chat-active");
    toggleSection.show();
    chatHistory.scrollTop(chatHistory.prop("scrollHeight"));
    tempContent = $(
      `<div class="chat-active-header"><span class="back-to-chat-list">&#10094;</span><span class="seller-name">  ${$(
        this
      )
        .children(".seller-name")
        .text()} </span></div>`
    );
    $(".message-header .fa-message").replaceWith(tempContent);
    headerContent = tempContent;
    $(".back-to-chat-list").click(() => goBack());
  });

  // Navigating back to chat list
  function goBack() {
    toggleSection.hide();
    toggleSection = chatList;
    toggleSection.show();
    $(".chat-active-header").replaceWith(
      $('<i class="fa-regular fa-message fa-lg"><span>Messages</span></i>')
    );
  }

  // Sending message
  const send = $(".fa-paper-plane");
  send.click(function () {
    const textArea = $("textarea#message");
    if (textArea.val() === "") return;
    let newMessage = $('<p class="customer-message"></p>');
    if (
      textArea.val().includes("http") &&
      !textArea.val().includes("<script>")
    ) {
      // Add link as a tag
    } else {
      newMessage.text(textArea.val());
    }
    newMessage = $('<div class="customer-message-container"></div>').append(
      newMessage
    );
    textArea.val("");
    chatHistory.append(newMessage);
    chatHistory.scrollTop(chatHistory.prop("scrollHeight"));
  });

  // Deleting entire chat
  if (toggleSection.hasClass("chats")) {
    // Click on ellipsis to show delete menu
    $(".fa-ellipsis").click(function (event) {
      event.stopPropagation();
      const deletePrompt = $(this).parent().next(".delete");
      deletePrompt.parent().siblings().children(".delete").hide();
      deletePrompt.toggle();
    });
    // Delete message on click trash can
    $(".delete .fa-trash-can").click(function (event) {
      event.stopPropagation();
      $(this).parent().toggle();
      $(this).parent().parent().remove();
    });
    // Close delete pop-up on click anywhere
    // on the messanger body except the pop-up
    $(".messanger").click(() => {
      if ($(".delete").is(":visible")) {
        $(".delete").hide();
      }
    });
  }
  // END OF MESSANGER
});
