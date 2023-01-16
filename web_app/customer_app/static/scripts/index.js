//  SCRIPT FOR:
// 1. Banner animation
// 2. Categories menu
// 3. Navigation functions including showing side cart
// 4. Shop now button
$("document").ready(function () {
  // Adjust zoom level depending on the screen size
  document.body.style.zoom = $(window).innerHeight() / $(window).outerHeight();

  // START OF CATEGORIES MENU
  $(".product-nav").hover(function () {
    $(".categories a").removeClass("color-on-hover");
    $(".subcategories-container").html(
      $(".categories").children("a:first-child + .subcategories").html()
    );
    $(".categories").children("a:first-child").addClass("color-on-hover");
  });
  $(".categories a").hover(function () {
    $(this).siblings("a").removeClass("color-on-hover");
    $(this).addClass("color-on-hover");
    $(".subcategories-container").html($(this).next(".subcategories").html());
  });
  // END OF CATEGORIES MENU

  // START OF NAVIGATION ICONS
  // Notification menu
  $(".notification-icon").click(function () {
    $(".profile-icon").removeClass("color-on-hover");
    $(".fa-cart-shopping").removeClass("color-on-hover");
    $(".profile-menu").hide();
    $(".slide-cart").removeClass("slide-cart-width");
    $(this).toggleClass("color-on-hover");
    $(".notification-menu").toggle();
  });

  // Profile menu
  $(".profile-icon").click(function () {
    $(".notification-icon").removeClass("color-on-hover");
    $(".fa-cart-shopping").removeClass("color-on-hover");
    $(".notification-menu").hide();
    $(".slide-cart").removeClass("slide-cart-width");
    $(this).toggleClass("color-on-hover");
    $(".profile-menu").toggle();
  });

  // Slide-cart
  $(".fa-cart-shopping").click(function () {
    $(".notification-icon").removeClass("color-on-hover");
    $(".profile-icon").removeClass("color-on-hover");
    $(".notification-menu").hide();
    $(".profile-menu").hide();
    $(this).toggleClass("color-on-hover");
    $(".slide-cart").toggleClass("slide-cart-width");
    $(".slide-cart").height($(window).outerHeight() - 139);
  });

  $(window).on("zoom", function () {
    $(".slide-cart").height($(window).outerHeight() - 139);
  });

  $(".close-cart").click(function () {
    $(".slide-cart").toggleClass("slide-cart-width");
    $(".fa-cart-shopping").toggleClass("color-on-hover");
  });
  // END OF NAVIGATION ICONS

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

  // START OF SEARCH BUTTON
  $("button.search").click(function (event) {
    if ($(this).prev("input").val() === "") return;
    let params = new URLSearchParams();
    params.append("q", $("input.search").val());
    location.href = "/search?" + params.toString();
  });
  // END OF SEARCH BUTTON
  // START OF NOTIFICATIONS
  $("#notification-menu-mark-all-as-read").click(function () {
    const notifications = $(".pop-up-notification-content");
    const noNotifications = $(
      "<span class='no-notifications'>No notifications</span>"
    );
    notifications.animate({ left: "100%" }, 1000, function () {
      $(this).remove();
      $(".notification-menu").prepend(noNotifications);
    });
  });
  // END OF NOTIFICATIONS
});
