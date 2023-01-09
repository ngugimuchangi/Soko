// SCRIPT FOR USER DASHBOARD
$(document).ready(function () {
  let currentSection = $(".active-dashboard-content");
  currentSection.show();

  // Delete Saved Item
  $(".delete-saved-item").click(function () {
    $(this).parent().parent().remove();
  });

  // View order filters
  $(".order-filter-toggle").click(function () {
    $(".order-filters").toggle();
  });
  $(".order-filters li").click(function () {
    $(".order-filters").toggle();
  });
});
