// SCRIPT FOR:
// 1. Updating dashboard modal content
// 2. Updating user details
// 3. Posting product reviews
$(document).ready(function () {
  // START OF COMMON MODAL FEATURES
  //  Modal dimensions adjustments
  $(window).on("zoom", function () {
    $(".modal-container").width($(window).outerWidth());
    $(".modal-container").height($(window).outerHeight());
  });

  $(window).on("resize", function () {
    $(".modal-container").width($(window).outerWidth());
    $(".modal-container").height($(window).outerHeight());
  });
  // Prevent click event propagation for labels and inputs
  $(".modal-content").on("click", ".modal-label", function (event) {
    event.stopPropagation();
  });
  $(".modal-content").on("click", ".modal-input", function (event) {
    event.stopPropagation();
  });

  // Updating modal content
  function updateModal(
    header,
    modalContent,
    submitButtonClass,
    submitButtonText
  ) {
    $(".modal-header h3").text(header);
    $(".submit-modal-info").addClass(submitButtonClass);
    $(".submit-modal-info").text(submitButtonText);
    $(".modal-content").prepend(modalContent);
    $(".modal-container").width($(window).outerWidth());
    $(".modal-container").height($(window).outerHeight());
    $(".modal-container").toggleClass("show-modal");
  }
  // Close modal
  function removeModalDetails() {
    $(".modal-content input").remove();
    $(".modal-content label").remove();
    $(".submit-modal-info").removeClass([
      "update-profile-details",
      "update-address-details",
      "update-card-details",
      "submit-new-address-details",
      "submit-new-card-details",
    ]);
  }
  $(".close-modal-x").click(function (event) {
    event.stopPropagation();
    $(".modal-container").toggleClass("show-modal");
    removeModalDetails();
  });

  $(".modal-container").click(function () {
    $(".modal-container").removeClass("show-modal");
    removeModalDetails();
  });
  $(".modal").click(function (event) {
    event.stopPropagation();
  });

  // END OF COMMON MODAL FEATURES

  // START OF MY PROFILE
  // Modal content for editing profile details
  $(".edit-profile").click(function () {
    const firstName =
      $("#user-names").attr("f-name") === "None"
        ? ""
        : $("#user-names").attr("f-name");
    const lastName =
      $("#user-names").attr("l-name") === "None"
        ? ""
        : $("#user-names").attr("l-name");
    const email = $("#user-email span").text();
    const phoneNumber = $("#user-phone-number span").text();
    const modalContent = `<label for="first-name" class="modal-label">First Name</label>
      <input
        type="text"
        name="first-name"
        id="first-name"
        class="modal-input"
        value= "${firstName}"
        required
        oninvalid="this.setCustomValidity('Enter your first name')"
      />
      <label for="last-name" class="modal-label">Second Name</label>
      <input
        type="text"
        name="last-name"
        id="last-name"
        class="modal-input"
        value= "${lastName}"
        required
        oninvalid="this.setCustomValidity('Enter your last name')"
      />
      <label for="email" class="modal-label">Email</label>
      <input
        type="email"
        name="email"
        id="email"
        class="modal-input"
        value= "${email}"
        required
        oninvalid="this.setCustomValidity('Enter your email')"
      />
      <label for="phone-number" class="modal-label">Phone Number</label>
      <input
        type="tel"
        name="phone-number"
        id="phone-number"
        class="modal-input"
        value= "${phoneNumber}"
        required
        oninvalid="this.setCustomValidity('Enter your phone number')"
      />`;
    updateModal(
      "Edit Profile",
      modalContent,
      "update-profile-details",
      "Update"
    );
  });

  // Submit profile module info
  $(".modal-content").on("click", ".update-profile-details", function (event) {
    event.stopPropagation();
    const firstName = $("input#first-name").val();
    const lastName = $("input#last-name").val();
    const email = $("input#email").val();
    const phoneNumber = $("input#phone-number").val();
    const fields = new Array(firstName, lastName, email, phoneNumber);
    if (fields.some((field) => field == "")) return;
    $("#user-names").attr("f-name", firstName);
    $("#user-names").attr("l-name", lastName);
    $("#user-names").text(`${firstName} ${lastName}`);
    $("#user-email span").text(email);
    $("user-phone-number span").text(phoneNumber);
    removeModalDetails();
    $(".modal-container").removeClass("show-modal");
  });
  // END OF MY PROFILE MODAL

  // START OF ADDRESS MODULE
  let currentAddressId;
  // Add new address
  $(document).on("click", ".add-address", function () {
    const modalContent = `<label for="first-name" class="modal-label">First Name</label>
      <input
        type="text"
        name="first-name"
        id="first-name"
        class="modal-input"
        required
        oninvalid="this.setCustomValidity('Enter your first name')"
      />
      <label for="last-name" class="modal-label">Second Name</label>
      <input
        type="text"
        name="last-name"
        id="last-name"
        class="modal-input"
        required
        oninvalid="this.setCustomValidity('Enter your last name')"
      />
      <label for="phone-number" class="modal-label">Phone Number</label>
      <input
        type="tel"
        name="phone-number"
        id="phone-number"
        class="modal-input"
        required
        oninvalid="this.setCustomValidity('Enter your phone number')"
      />
      <label for="address-details" class="modal-label">Address Details</label>
      <input
        type="text"
        name="address-details"
        id="address-details"
        class="modal-input"
        required
        oninvalid="this.setCustomValidity('Enter your address details')"
      />
      <div class="set-default">
        <input
        type="checkbox"
        name="set-default-address"
        id="set-default-address"
        class="modal-input"
      />
        <label for="set-default-address" class="modal-label">
        Set as default address </label>
      </div>
      `;
    updateModal(
      "Add New Address",
      modalContent,
      "submit-new-address-details",
      "Add"
    );
  });
  $(document).on("click", ".edit-address", function () {
    currentAddressId = $(this).parent().parent().attr("data-id");
    const addressHolder = $(this)
      .parent()
      .siblings(".address-holder")
      .children("p");
    const firstName = addressHolder.attr("f-name");
    const lastName = addressHolder.attr("l-name");
    const addressDetails = $(this).parent().siblings("#address-details").text();
    const phoneNumber = $(this)
      .parent()
      .siblings("#address-phone-number")
      .text();
    const modalContent = `<label for="first-name" class="modal-label">First Name</label>
      <input
        type="text"
        name="first-name"
        id="first-name"
        class="modal-input"
        value= "${firstName}"
        required
        oninvalid="this.setCustomValidity('Enter your first name')"
      />
      <label for="last-name" class="modal-label">Second Name</label>
      <input
        type="text"
        name="last-name"
        id="last-name"
        class="modal-input"
        value= "${lastName}"
        required
        oninvalid="this.setCustomValidity('Enter your last name')"
      />
      <label for="phone-number" class="modal-label">Phone Number</label>
      <input
        type="tel"
        name="phone-number"
        id="phone-number"
        class="modal-input"
        value= "${phoneNumber}"
        required
        oninvalid="this.setCustomValidity('Enter your phone number')"
      />
      <label for="address-details" class="modal-label">Address Details</label>
      <input
        type="text"
        name="address-details"
        id="address-details"
        class="modal-input"
        value= "${addressDetails}"
        required
        oninvalid="this.setCustomValidity('Enter your address details')"
      />
      <div class="set-default">
        <input
        type="checkbox"
        name="set-default-address"
        id="set-default-address"
        class="modal-input"
      />
        <label for="set-default-address" class="modal-label">
        Set as default address </label>
      </div>
      `;
    updateModal(
      "Edit Address",
      modalContent,
      "update-address-details",
      "Update"
    );
  });
  // Submit address details info
  $(".modal-content").on("click", ".update-address-details", function (event) {
    event.stopPropagation();
    const firstName = $("input#first-name").val();
    const lastName = $("input#last-name").val();
    const addressDetails = $("input#address-details").val();
    const phoneNumber = $("input#phone-number").val();
    const fields = new Array(firstName, lastName, addressDetails, phoneNumber);
    if (fields.some((field) => field == "")) return;
    const currentAddress = $(`.address[data-id |= "${currentAddressId}"]`);
    currentAddress
      .children()
      .children("#address-holder")
      .attr("f-name", firstName);
    currentAddress
      .children()
      .children("#address-holder")
      .attr("l-name", lastName);
    currentAddress
      .children()
      .children("#address-holder")
      .text(`${firstName} ${lastName}`);
    currentAddress.children("#address-phone-number").text(phoneNumber);
    currentAddress.children("#address-details").text(addressDetails);
    if ($("input#set-default-address").is(":checked")) {
      currentAddress
        .siblings(".address")
        .children(".address-holder")
        .children(".fa-star")
        .removeClass(["default", "fa-solid"]);
      currentAddress
        .siblings(".address")
        .children(".address-holder")
        .children(".fa-star")
        .addClass("fa-regular");
      currentAddress
        .children(".address-holder")
        .children(".fa-star")
        .removeClass("fa-regular");
      currentAddress
        .children(".address-holder")
        .children(".fa-star")
        .addClass(["fa-solid", "default"]);
    }
    removeModalDetails();
    $(".modal-container").removeClass("show-modal");
  });

  // Submit new address details
  $(".modal-content").on(
    "click",
    ".submit-new-address-details",
    function (event) {
      event.stopPropagation();
      const firstName = $("input#first-name").val();
      const lastName = $("input#last-name").val();
      const addressDetails = $("input#address-details").val();
      const phoneNumber = $("input#phone-number").val();
      const fields = new Array(
        firstName,
        lastName,
        addressDetails,
        phoneNumber
      );
      if (fields.some((field) => field == "")) return;
      const currentAddress =
        $(`<article class="address user-item flex-column" data-id="${Math.floor(
          Math.random() * 1000
        )}">
            <div class="address-holder flex-row">
              <p id="address-holder" f-name="${firstName}" l-name="${lastName}">
                ${firstName} ${lastName}
              </p>
              <i class="fa-regular fa-star dashboard-content-icon"></i>
            </div>
            <p id="address-phone-number">${phoneNumber}</p>
            <p id="address-details">${addressDetails}</p>
            <div class="delete-edit flex-row">
              <i
                class="fa-solid fa-trash-can dashboard-content-icon delete-address"
              ></i>
              <i
                class="fa-solid fa-pen dashboard-content-icon edit edit-address"
              ></i>
            </div>
        </article>`);

      $(".user-addresses-div").prepend(currentAddress);
      if ($("input#set-default-address").is(":checked")) {
        currentAddress
          .siblings(".address")
          .children(".address-holder")
          .children(".fa-star")
          .removeClass(["default", "fa-solid"]);
        currentAddress
          .siblings(".address")
          .children(".address-holder")
          .children(".fa-star")
          .addClass("fa-regular");
        currentAddress
          .children(".address-holder")
          .children(".fa-star")
          .removeClass("fa-regular");
        currentAddress
          .children(".address-holder")
          .children(".fa-star")
          .addClass(["fa-solid", "default"]);
      }
      removeModalDetails();
      $(".modal-container").removeClass("show-modal");
    }
  );
  // END OF ADDRESS MODULE

  // START OF CARD DETAILS
  // END OF CARD DETAILS
});
