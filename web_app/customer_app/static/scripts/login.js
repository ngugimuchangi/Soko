$("document").ready(function () {
  // Toggling password viewing
  $(".toggle-password").click(function () {
    $(this).toggleClass("fa-lock fa-lock-open");
    if ($(this).hasClass("fa-lock")) {
      $(this).prev().attr("type", "password");
    } else {
      $(this).prev().attr("type", "text");
    }
  });

  //   Password confirmation check
  $(".pwd-check form").submit(function (event) {
    const formData = $(this).serializeArray();
    if (formData.some((element) => element.value === "")) return;
    const [pwd, confirmPwd] = [formData[1].value, formData[2].value];
    if (confirmPwd !== pwd) {
      event.preventDefault();
      const alert = $(
        '<div class="alert alert-danger alert-dismissible fade show"> ' +
          '<button type="button" class="btn-close" data-bs-dismiss="alert"> ' +
          "</button> <strong>Your passwords must match</strong></div>"
      );
      if (!$(".alert-danger").length) $("body").prepend(alert);
    }
  });
});
