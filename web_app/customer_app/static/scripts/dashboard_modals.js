// SCRIPT FOR:
// 1. Updating dashboard modal content
// 2. Updating user details
// 3. Posting product reviews
// NB Will change editing and adding new data to use
// ajax calls to backend API latter
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
    $(".modal-container").removeClass("show-modal");
  }
  $(".close-modal-x").click(function (event) {
    event.stopPropagation();
    removeModalDetails();
  });

  $(".modal-container").click(function () {
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
    $("#user-phone-number span").text(phoneNumber);
    removeModalDetails();
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

  // Editing an existing address
  $(document).on("click", ".edit-address", function () {
    currentAddressId = $(this).parent().parent().attr("data-id");
    const addressHolder = $(this)
      .parent()
      .siblings(".address-holder")
      .children("p");
    const firstName = addressHolder.attr("f-name");
    const lastName = addressHolder.attr("l-name");
    const addressDetails = $(this).parent().siblings(".address-details").text();
    const phoneNumber = $(this)
      .parent()
      .siblings(".address-phone-number")
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
      .children(".address-holder-names")
      .attr("f-name", firstName);
    currentAddress
      .children()
      .children(".address-holder-names")
      .attr("l-name", lastName);
    currentAddress
      .children()
      .children(".address-holder-names")
      .text(`${firstName} ${lastName}`);
    currentAddress.children(".address-phone-number").text(phoneNumber);
    currentAddress.children(".address-details").text(addressDetails);
    if ($("input#set-default-address").is(":checked")) {
      setDefault(currentAddress, ".address", ".address-holder");
    }
    removeModalDetails();
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
              <p class="address-holder-names" f-name="${firstName}" l-name="${lastName}">
                ${firstName} ${lastName}
              </p>
              <i class="fa-regular fa-star dashboard-content-icon"></i>
            </div>
            <p class="address-phone-number">${phoneNumber}</p>
            <p class="address-details">${addressDetails}</p>
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
        setDefault(currentAddress, ".address", ".address-holder");
      }
      removeModalDetails();
    }
  );

  //  Function to set address or card to default
  function setDefault(currentItem, currentItemClass, defaultSection) {
    currentItem
      .siblings(currentItemClass)
      .children(defaultSection)
      .children(".fa-star")
      .removeClass(["default", "fa-solid"])
      .addClass("fa-regular");
    currentItem
      .children(defaultSection)
      .children(".fa-star")
      .removeClass("fa-regular")
      .addClass(["fa-solid", "default"]);
  }
  // END OF ADDRESS MODULE

  // START OF CARD DETAILS
  let currentCardId;

  // Editing an existing card
  $(document).on("click", ".edit-card", function () {
    currentCardId = $(this).parent().parent().attr("data-id");
    const cardNumber = $(this)
      .parent()
      .siblings(".card-number")
      .attr("data-name");
    const cardHolder = $(this)
      .parent()
      .siblings(".card-holder")
      .children(".card-holder-names")
      .text();
    const expiryDate = $(this)
      .parent()
      .siblings(".expiry-date")
      .attr("expiry-date");
    modalContent = ` <label for="card-number" class="modal-label">Card Number</label>
    <input
        type="text"
        name="card-number"
        id="card-number"
        class="modal-input"
        value= "${cardNumber}"
        minlength="19"
        maxlength="19"
        required
        oninvalid="this.setCustomValidity('Enter the card number')"
      />
      <label for="card-holder" class="modal-label">Card Holder's Name</label>
      <input
        type="text"
        name="last-name"
        id="last-name"
        class="modal-input"
        value= "${cardHolder}"
        required
        oninvalid="this.setCustomValidity('Enter card holder's names')"
      />
      <div class="expiry-date-and-cvv">
      <label for="expiry-date" class="modal-label">Expiry date</label>
      <label for="cvv" class="modal-label">CVV</label>
      <input
        type="text"
        name="expiry-date"
        id="expiry-date"
        class="modal-input"
        value="${expiryDate}"
        minlength="5"
        max-length="5"
        placeholder="MM/YY"
        required
        oninvalid="this.setCustomValidity('Enter cards expiry date')"
      />
      <input
        type="text"
        name="cvv"
        id="cvv"
        size="3"
        minlength="3"
        class="modal-input"
        required
        oninvalid="this.setCustomValidity('Enter correct card verification value')"
      />
      </div>
      <div class="set-default">
        <input
        type="checkbox"
        name="set-default-card"
        id="set-default-card"
        class="modal-input"
      />
        <label for="set-default-card" class="modal-label">
        Set as default payment card </label>
      </div>
      `;
    updateModal("Edit Card", modalContent, "update-card-details", "Update");
  });

  // Submit updated card details
  $(".modal-content").on("click", ".update-card-details", function (event) {
    event.stopPropagation();
    const currentCard = $(`.card[data-id |= "${currentCardId}"]`);
    const cardNumber = $("input#card-number").val();
    const lastDigits = cardNumber.split("-");
    const cardHolder = $("input#card-names").val();
    const expiryDate = $("input#expiry-date").val();
    const cvv = $("input#cvv").val();
    const fields = new Array(cardNumber, cardHolder, expiryDate, cvv);
    if (fields.some((field) => field == "")) return;
    currentCard
      .children(".card-holder")
      .children(".card-holder-names")
      .text(cardHolder);
    currentCard
      .children(".card-number")
      .text(`XXXX-XXXX-XXXX-${lastDigits[lastDigits.length - 1]}`);
    currentCard.children(".card-number").attr("data-name", cardNumber);
    currentCard.children(".expiry-date").text(`Expires on: ${expiryDate}`);
    currentCard.children(".expiry-date").attr("data-name", cardNumber);
    if ($("input#set-default-card").is(":checked")) {
      setDefault(currentCard, ".card", ".card-holder");
    }
    removeModalDetails();
  });

  // Adding a new card
  $(".add-card").click(function () {
    modalContent = ` <label for="card-number" class="modal-label">Card Number</label>
    <input
        type="text"
        name="card-number"
        id="card-number"
        class="modal-input"
        maxlength="19"
        minlength="19"
        required
        oninvalid="this.setCustomValidity('Enter the card number')"
      />
      <label for="card-holder" class="modal-label">Card Holder's Name</label>
      <input
        type="text"
        name="card-holder"
        id="card-holder"
        class="modal-input"
        required
        oninvalid="this.setCustomValidity('Enter card holder's names')"
      />
      <div class="expiry-date-and-cvv">
      <label for="expiry-date" class="modal-label">Expiry date</label>
      <label for="cvv" class="modal-label">CVV</label>
      <input
        type="text"
        name="expiry-date"
        id="expiry-date"
        class="modal-input"
        maxlength="5"
        minlength="5"
        placeholder="MM/YY"
        required
        oninvalid="this.setCustomValidity('Enter cards expiry date')"
      />
      <input
        type="text"
        name="cvv"
        id="cvv"
        minlength="3"
        maxlength="3"
        class="modal-input"
        required
        oninvalid="this.setCustomValidity('Enter correct card verification value')"
      />
      </div>
      <div class="set-default">
        <input
        type="checkbox"
        name="set-default-card"
        id="set-default-card"
        class="modal-input"
      />
        <label for="set-default-card" class="modal-label">
        Set as default payment card </label>
      </div>
      `;
    updateModal("Add New Card", modalContent, "submit-new-card-details", "Add");
  });
  // Submit new card details
  $(".modal-content").on("click", ".submit-new-card-details", function (event) {
    event.stopPropagation();
    const cardNumber = $("input#card-number").val();
    const lastDigits = cardNumber.split("-");
    const cardHolder = $("input#card-holder").val();
    const expiryDate = $("input#expiry-date").val();
    const fields = new Array(cardNumber, cardHolder, expiryDate, cvv);
    if (fields.some((field) => field == "")) return;
    const newCard = $(`
          <article class="card user-item flex-column" data-id="${Math.floor(
            Math.random() * 1000
          )}">
            <div class="card-holder flex-row">
              <p class="card-holder-names">${cardHolder}</p>
              <i class="fa-regular fa-star dashboard-content-icon"></i>
            </div>
            <p class="card-number" data-name="${cardNumber}">
              XXXX-XXXX-XXXX-${lastDigits[lastDigits.length - 1]}
            </p>
            <p class="expiry-date" expiry-date="${expiryDate}">Expires on: ${expiryDate}</p>
            <div class="delete-edit flex-row">
              <i
                class="fa-solid fa-trash-can dashboard-content-icon delete-card"
              ></i>
              <i
                class="fa-solid fa-pen dashboard-content-icon edit-card edit"
              ></i>
            </div>
          </article>
    `);
    $(".card-details-div").prepend(newCard);
    if ($("input#set-default-card").is(":checked")) {
      setDefault(newCard, ".card", ".card-holder");
    }
    removeModalDetails();
  });
  // END OF CARD DETAILS

  //  START OF NOTIFICATION MODAL
  // END OF NOTIFICATION MODAL

  //  START OF REVIEW MODAL
  // END OF REVIEW MODAL

  //  START OF ORDER MODAL
  // END OF ORDER MODAL
});
