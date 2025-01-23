function FilterMaster(page) {
  if (page == "") {
    page = $("#current_page").val();
  }
  var keyword = $("#keyword_search").val();
  var search_url = $("#keyword_search").attr("data-url");
  var status = $("#filter_status").val();
  var discount_type = $("#discount_type").val();
  var search_url = $("#searchForm").attr("action");
  var date = $("#filter_date").val();
  var mail_status = $("#mail_status").val();

  $.ajax({
    url: search_url,
    headers: {
      "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
    },
    method: "GET",
    data: {
      page: page,
      keyword: keyword,
      discount_type: discount_type,
      status: status,
      date: date,
      mail_status: mail_status,
    },
    beforeSend: function () {},
    success: function (response) {
      if (search_url) {
        if (!search_url.includes("products_category")) {
          $("#master-tbody").html(response.template);
          $("#master-pagination").html(response.pagination);
        } else {
          if (keyword | page) {
            $("#master-tbody").html(response.template);
            $("#master-pagination").html(response.pagination);
          } else {
            window.location.reload();
          }
        }
      }
    },
  });
}

function ResetFilter() {
  $("#filter_status").val("all").trigger("change");
  $("#filter_plan").val("all").trigger("change");
  $("#keyword_search").val("");
  $("#search_loc").val("");
  $("#filter_date").val("");
  $("#discount_type").val("").trigger("change");
  $("#mail_status").val("");
  FilterMaster("1");
}

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
        if (form == "heading-form") {
          $("#headingeditform-div").html(response.template);
        } else if (form == "tip-form") {
          $("#tipeditform-div").html(response.template);
        }
      }
    },
  });
}

function validateFileAndSize(fileInput) {
  const file = fileInput.files[0];
  const dropifyWrapper = fileInput.closest(".dropify-wrapper"); // Find the closest dropify-wrapper
  let errorMessageElement = document.getElementById("errorMessage"); // Check if an error message already exists

  if (file) {
    const fileSizeInMB = file.size / (1024 * 1024); // Convert bytes to MB
    const allowedImageSize = 1; // 1 MB for images
    const allowedVideoSize = 20; // 20 MB for videos
    const allowedImageTypes = ["image/jpeg", "image/jpg", "image/png", "image/webp"]; // Allowed MIME types for images
    const allowedVideoTypes = ["video/mp4"]; // Allowed MIME types for videos

    // Check file type and size
    if (allowedImageTypes.includes(file.type)) {
      if (fileSizeInMB > allowedImageSize) {
        displayError(
          "The image size must be less than 1 MB.",
          dropifyWrapper,
          fileInput
        );
        return; // Exit the function
      }
    } else if (allowedVideoTypes.includes(file.type)) {
      if (fileSizeInMB > allowedVideoSize) {
        displayError(
          "The video size must be less than 20 MB.",
          dropifyWrapper,
          fileInput
        );
        return; // Exit the function
      }
    } else {
      displayError(
        "Invalid file type. Only jpeg, jpg, png, webp images, and mp4 videos are allowed.",
        dropifyWrapper,
        fileInput
      );
      return; // Exit the function
    }

    console.log("File is valid.");
  }
}

function displayError(message, wrapper, input) {
  let errorMessageElement = document.getElementById("errorMessage");
  if (!errorMessageElement) {
    errorMessageElement = document.createElement("div"); // Create error message div
    errorMessageElement.id = "errorMessage"; // Set ID
    errorMessageElement.style.color = "red"; // Style the error message
    errorMessageElement.style.fontSize = "14px";
    errorMessageElement.style.marginTop = "10px";
  }

  errorMessageElement.textContent = message;
  wrapper.insertAdjacentElement("afterend", errorMessageElement); // Insert after dropify-wrapper
  input.value = ""; // Clear the input

  setTimeout(() => {
    errorMessageElement.remove(); // Remove the message after 2 seconds
  }, 2000);
}

function validateMediaFile(imageInput) {
  const file = imageInput.files[0];
  const dropifyWrapper = imageInput.closest(".dropify-wrapper"); // Find the closest dropify-wrapper
  let errorMessageElement = document.getElementById("errorMessage"); // Check if an error message already exists

  if (file) {
    const fileSizeInMB = file.size / (1024 * 1024); // Convert bytes to MB
    const allowedImageTypes = [
      "image/jpeg",
      "image/jpg",
      "image/png",
      "image/webp",
    ]; // Allowed image MIME types
    const allowedVideoTypes = ["video/mp4"]; // Allowed video MIME types
    const maxImageSize = 1; // 1 MB for images
    const maxVideoSize = 10; // 10 MB for videos

    // Determine if the file is an image or video
    if (allowedImageTypes.includes(file.type)) {
      // Validate image
      if (fileSizeInMB > maxImageSize) {
        displayErrorMessage(
          "The image size must be less than 1 MB.",
          dropifyWrapper,
          imageInput
        );
        return;
      }
    } else if (allowedVideoTypes.includes(file.type)) {
      // Validate video
      if (fileSizeInMB > maxVideoSize) {
        displayErrorMessage(
          "The video size must be less than 10 MB.",
          dropifyWrapper,
          imageInput
        );
        return;
      }
    } else {
      // Invalid file type
      displayErrorMessage(
        "Invalid file type. Only jpeg, jpg, png, webp for images and mp4 for videos are allowed.",
        dropifyWrapper,
        imageInput
      );
      return;
    }

    console.log("File is valid.");
  }
}

function displayErrorMessage(message, dropifyWrapper, imageInput) {
  let errorMessageElement = document.getElementById("errorMessage"); // Check if an error message already exists

  if (!errorMessageElement) {
    errorMessageElement = document.createElement("div"); // Create error message div
    errorMessageElement.id = "errorMessage"; // Set ID
    errorMessageElement.style.color = "red"; // Style the error message
    errorMessageElement.style.fontSize = "14px";
    errorMessageElement.style.marginTop = "10px";
  }

  errorMessageElement.textContent = message;
  dropifyWrapper.insertAdjacentElement("afterend", errorMessageElement); // Insert after dropify-wrapper
  imageInput.value = ""; // Clear the input

  setTimeout(() => {
    errorMessageElement.remove(); // Remove the message after 2 seconds
  }, 2000);
}
