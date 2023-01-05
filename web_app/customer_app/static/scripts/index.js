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

  // START OF MESSANGER
  // Opening an closing window
  const toggleArrow = $(".arrow");
  const chatHistory = $(".chat-history");
  const chatList = $(".chats");
  let toggleSection = chatList;
  let headerContent = $(".message-header .fa-message");
  let tempContent;
  let prevContent;
  toggleArrow.click(function () {
    if ($(this).hasClass("fa-angles-up")) {
      $(this).removeClass("fa-angles-up");
      $(this).addClass("fa-angles-down");
      $(".messanger").addClass("messanger-size");
      $(".message-header").addClass("message-header-properties");
      toggleSection.show();
      if (toggleSection.hasClass("chat-active")) {
        headerContent.replaceWith(prevContent);
        headerContent = prevContent;
      }
      $(".back-to-chat-list").click(() => goBack());
    } else {
      $(this).removeClass("fa-angles-down");
      $(this).addClass("fa-angles-up");
      $(".messanger").removeClass("messanger-size");
      $(".message-header").removeClass("message-header-properties");
      toggleSection.hide();
      tempContent = $(
        '<i class="fa-regular fa-message fa-lg"><span>Messages</span></i>'
      );
      if (toggleSection.hasClass("chat-active")) {
        prevContent = headerContent;
        headerContent.replaceWith(tempContent);
        headerContent = tempContent;
      }
    }
  });

  // Loading messages
  const chat = $(".chat");
  chat.click(function () {
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

  // Deleting message
  // Show message on ellipsis click
  $(".fa-ellipsis").click(() => {
    $(".delete").show();
  });
  // Delete message on trash-can click
  $(".delete .trash-can").click(function () {
    $(this).parent().toggle();
    $(this).parent().parent().remove();
  });
  // Hide delete option on click body
  $("body *").click(() => {
    if ($(".delete").css("display") === "block") {
      $(".delete").hide();
    }
  });

  // END OF MESSANGER
});
