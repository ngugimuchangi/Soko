// SCRIPT FOR MESSENGER
// Socket integration to be done later
// Opening and closing chat section
const toggleArrow = $(".arrow");
const chatHistory = $(".chat-history");
const chatList = $(".chats");
let toggleSection = chatList;
let headerContent = $(".message-header .fa-message");
let tempContent;
toggleArrow.click(function () {
  $(this).toggleClass("fa-angles-up fa-angles-down");
  $(".messenger").toggleClass("messenger-size");
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
  if (textArea.val().includes("http") && !textArea.val().includes("<script>")) {
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
if (
  toggleSection.hasClass("chats") ||
  toggleSection.hasClass("dashboard-chats")
) {
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
  $(".messenger").click(() => {
    if ($(".delete-chat").is(":visible")) {
      $(".delete-chat").hide();
    }
  });
}

// END OF MESSENGER
