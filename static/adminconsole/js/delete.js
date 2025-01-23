$(document).on("click", ".delete-item", function (event) {
  event.preventDefault();

  var data_url = $(this).attr("data-url");
  var item_id = $(this).attr("data-item-id");
  var button = document.getElementById("delete-btn-confirm");
  button.setAttribute("data-url", data_url);
  button.setAttribute("data-item-id", item_id);
});

$(document).on("click", "#delete-btn-confirm", function (event) {
  event.preventDefault();

  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var data_url = $(this).attr("data-url");
  var item_id = $(this).attr("data-item-id");
  var headers = {
    "X-CSRFToken": csrfToken,
  };

  $.ajax({
    type: "post",
    url: data_url,
    data: {
      id: item_id,
    },
    headers: headers,
    beforeSend: function () {
      $("#modal-close-btn").click();
    },

    success: function (response) {
      console.log(response);
      if (response.status) {
        notif({
          msg: response.message,
          type: "success",
        });
        FilterMaster("");
        // location.href = response.redirect_url;
      } else {
        notif({
          msg: response.message,
          type: "error",
          position: "center",
        });
      }
    },
    complete: function () {},
  });
});
