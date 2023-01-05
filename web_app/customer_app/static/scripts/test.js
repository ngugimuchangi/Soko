$(function () {
  console.log("Soko test live");
  const socket = io.connect("http://localhost:5006");
  socket.on("connect", function () {
    socket.send("Connection successful");
  });

  // Submit message to server
  $("form").submit(function (event) {
    event.preventDefault();

    const textArea = $("textarea");
    const chatHistory = $("div.chat-history");

    if (textArea.val() === "") return;

    socket.send(textArea.val());
    const message = $("<p class='chat-message'></p>").html(textArea.val());
    chatHistory.append(message);
    $("textarea").val("");
  });
});
