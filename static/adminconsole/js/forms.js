$.validator.addMethod("validEmail", function(value, element) {
  // Regular expression for validating email
  var emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|net|org|edu|gov|mil|co|info|io|me|biz|us|ca|uk|de|fr|jp|cn|in)$/;
  return this.optional(element) || emailPattern.test(value);
}, "Please enter a valid email address with a proper domain");

$.validator.addMethod("noNumbers", function(value, element) {
  // Regular expression to check for numbers
  return this.optional(element) || /^[a-zA-Z\s]*$/.test(value);
}, "Names cannot contain numbers");


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

$("#userForm").validate({
  rules: {
    name: {
      required: true,
      noNumbers: true, 
      minlength: 3,  
    },
    email: {
      required: true,
      validEmail: true 
    },
    access_token: {
      required: true,
      minlength: 3,  
    },
    ad_account_id: {
      required: true,
      minlength: 3,  
    },
    app_id: {
      required: true,
      minlength: 3,  
    },
    app_secret: {
      required: true,
      minlength: 3,  
    },
    password: {
      required: true,
    },
    c_password: {
      required: true,
      equalTo: "#password", // Ensures c_password matches password
    },
  },
  messages: {
    c_password: {
      equalTo: "Passwords do not match", // Custom error message for mismatch
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
