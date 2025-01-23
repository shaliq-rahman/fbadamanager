function ToggleMaster(id, status, toggle_url) {
  $.ajax({
    url: toggle_url,
    headers: {
      "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
    },
    method: "POST",
    data: {
      id: id,
      status: status,
    },
    beforeSend: function () {},
    success: function (response) {
      if (response.status) {
        notif({
          msg: response.message,
          type: "success",
        });
        if (response.filter){
          FilterMaster('')
        }
      } else {
        $("#submitButton").prop("disabled", false);
        notif({
          msg: response.message,
          type: "error",
          position: "center",
        });
      }
    },
  });
}

function updateseq(item_id, element, type) {
  // Get CSRF token
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

  // Ensure only numbers
  let val = element.value.replace(/\D/g, ""); // Remove non-numeric characters
  element.value = val; // Update field to only show numbers

  // Send AJAX request if input has a value
  if (val) {
    $.ajax({
      url: "/update-sequence/",
      type: "POST",
      headers: { "X-CSRFToken": csrfToken },
      data: {
        item_id: item_id,
        sequence: val,
        type: type,
      },
      success: function (response) {
        console.log("Success", response);
      },
      error: function (error) {
        console.log("Error", error);
      },
    });
  }
}


$(document).on("change", ".master-toggle", function () {
  var id = $(this).attr("data-item_id");
  var toggle_url = $(this).attr("data-url");
  if ($(this).is(":checked")) {
    ToggleMaster(id, "checked", toggle_url);
  } else {
    console.log("Toggle button is unchecked");
    ToggleMaster(id, "unchecked", toggle_url);
  }
});

