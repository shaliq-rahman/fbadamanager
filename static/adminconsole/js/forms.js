$("#bannerForm").validate({
  rules: {
    heading: {
      required: true,
    },
  },
  submitHandler: function (form) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(form);
    var formUrl = $(form).attr("action");
    var headers = {
      "X-CSRFToken": csrfToken,
    };

    $.ajax({
      type: $(form).attr("method"),
      url: formUrl,
      data: formData,
      headers: headers,
      cache: false,
      contentType: false,
      processData: false,

      beforeSend: function () {
        $("#submitButton").prop("disabled", true).html("Please wait ...");
      },

      success: function (response) {
        if (response.status) {
          notif({
            msg: response.message,
            type: "success",
          });
          setTimeout(function () {
            location.href = response.redirect_url;
          }, 2000);
        } else {
          notif({
            msg: response.message,
            type: "error",
            position: "center",
          });
          $("#submitButton").prop("disabled", false).html("Submit");
        }
      },
      complete: function () {},
    });

    return false;
  },
});

$("#testimonialForm").validate({
  rules: {
    client_name: {
      required: true,
    },
    designation: {
      required: true,
    },
    comment: {
      required: true,
    },
  },
  submitHandler: function (form) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(form);
    var formUrl = $(form).attr("action");
    var headers = {
      "X-CSRFToken": csrfToken,
    };

    $.ajax({
      type: $(form).attr("method"),
      url: formUrl,
      data: formData,
      headers: headers,
      cache: false,
      contentType: false,
      processData: false,

      beforeSend: function () {
        $("#submitButton").prop("disabled", true).html("Please wait ...");
      },

      success: function (response) {
        if (response.status) {
          notif({
            msg: response.message,
            type: "success",
          });
          setTimeout(function () {
            location.href = response.redirect_url;
          }, 2000);
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

    return false;
  },
});

$("#careerForm").validate({
  rules: {
    title: {
      required: true,
    },
  },
  submitHandler: function (form) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(form);
    var formUrl = $(form).attr("action");
    var headers = {
      "X-CSRFToken": csrfToken,
    };

    $.ajax({
      type: $(form).attr("method"),
      url: formUrl,
      data: formData,
      headers: headers,
      cache: false,
      contentType: false,
      processData: false,

      beforeSend: function () {
        $("#submitButton").prop("disabled", true).html("Please wait ...");
      },

      success: function (response) {
        if (response.status) {
          notif({
            msg: response.message,
            type: "success",
          });
          setTimeout(function () {
            location.href = response.redirect_url;
          }, 2000);
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

    return false;
  },
});

$("#careerUpdateForm").validate({
  rules: {
    title: {
      required: true,
    },
  },
  submitHandler: function (form) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData(form);
    var formUrl = $(form).attr("action");
    var headers = {
      "X-CSRFToken": csrfToken,
    };

    $.ajax({
      type: $(form).attr("method"),
      url: formUrl,
      data: formData,
      headers: headers,
      cache: false,
      contentType: false,
      processData: false,

      beforeSend: function () {
        $("#careerupdateBtn").prop("disabled", true).html("Please wait ...");
      },

      success: function (response) {
        if (response.status) {
          notif({
            msg: response.message,
            type: "success",
          });
          setTimeout(function () {
            location.href = response.redirect_url;
          }, 2000);
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

    return false;
  },
});

function loadeditForm(id, form) {
  $.ajax({
    url: "/load-edit-form/",
    headers: {
      "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
    },
    method: "GET",
    data: {
      id: id,
      form: form,
    },
    beforeSend: function () {},
    success: function (response) {
      if (response.status) {
        if (form == "career-form") {
          $("#careereditform-div").html(response.template);
        }
      }
    },
  });
}
