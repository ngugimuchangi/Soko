// SCRIPT FOR USER DASHBOARD
$(document).ready(function () {
  // START OF SAVED ITEMS
  // Delete Saved Item
  $(".delete-saved-item").click(function () {
    $(this).parent().parent().remove();
  });
  // END OF SAVED ITEMS

  // START OF COMMON FILTERS
  // Toggle dashboard filters
  $(".dashboard-filter-toggle").click(function () {
    $(".dashboard-filters").toggle();
    $(this).toggleClass("fa-chevron-up fa-chevron-down");
    $(".notification-options-pop-up").hide();
  });
  $(".dashboard-filters li").click(function () {
    $(this).parent().toggle();
    $(this)
      .parent()
      .siblings(".dashboard-filter-toggle")
      .toggleClass("fa-chevron-up fa-chevron-down");
    $(".notification-options-pop-up").hide();
  });
  // END OF COMMON FILTERS

  // START OF NOTIFICATIONS OPTIONS
  // Notifications options toggle
  $(document).on("click", ".notification-options-toggle", function () {
    $(this)
      .parent()
      .siblings(".notification")
      .children(".notification-options-pop-up")
      .hide();
    $(this).siblings(".notification-options-pop-up").toggle();
  });

  // Mark notification as read
  $(document).on("click", ".mark-read", function () {
    const notification = $(this).parent().siblings(".notification-content");
    if (notification.hasClass("unread")) {
      notification.toggleClass("unread");
      notification.parent().attr("status", "read");
    }
    $(this).parent().toggle();
  });

  // Mark all as read
  $("#mark-all-as-read").click(() => {
    $(".notification[status|='unread']").children("p").removeClass("unread");
    $(".notification[status|='unread']").attr("status", "read");
  });
  // Delete notification
  $(document).on("click", ".delete-notification", function () {
    $(this).parent().parent().remove();
  });
  // Show all notification
  $("#all-notifications").click(() => {
    $(".notification").show();
  });

  // Show read notifications

  $("#read-notifications").click(() => {
    $(".notification[status|='read']").show();
    $(".notification[status|='unread']").hide();
  });

  // Show unread notifications
  $("#unread-notifications").click(() => {
    $(".notification[status|='unread']").show();
    $(".notification[status|='read']").hide();
  });
  // END OF NOTIFICATIONS OPTIONS

  // START OF ORDER SECTION
  // Show all orders
  $("#all-orders").click(() => {
    $(".order").show();
  });
  // Show completed orders
  $("#completed-orders").click(() => {
    $(".order[status!='completed']").hide();
    $(".order[status|='completed']").show();
  });
  // Show shipped orders
  $("#shipped-orders").click(() => {
    $(".order[status!='shipped']").hide();
    $(".order[status|='shipped']").show();
  });
  // END OF ORDER SECTION

  // START OF REVIEWS
  // Review button
  $(".review-product.btn").click(function (event) {
    event.stopPropagation();
  });
  // END OF REVIEW SECTION

  // START OF MESSENGER
  const chatHistory = $(".chat-history");

  // Load messages
  $(document).on("click", ".chat", function () {
    $(this).parent().hide();
    $(".chat-active .seller-name").text(
      $(this).children(".seller-name").text()
    );
    $(".chat-active").show();
    chatHistory.scrollTop(chatHistory.prop("scrollHeight"));
  });

  $(document).on("click", ".back-to-chat-list", function () {
    $(".chat-active").hide();
    $(".dashboard-chats").show();
  });

  // Sending a new message
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

  // Delete chat message
  // Click on ellipsis to show delete menu
  $(".chat-options-toggle").click(function (event) {
    event.stopPropagation();
    const deletePrompt = $(this).parent().next(".delete-chat");
    deletePrompt.parent().siblings().children(".delete-chat").hide();
    deletePrompt.toggle();
  });
  // Delete message on click trash can
  $(".delete-chat").click(function (event) {
    event.stopPropagation();
    $(this).parent().remove();
  });
  // Close delete pop-up on click anywhere
  // on the messenger body except the pop-up
  $(".dashboard-messenger").click(() => {
    if ($(".delete-chat").is(":visible")) {
      $(".delete-chat").hide();
    }
  });

  // END OF MESSENGER
});
