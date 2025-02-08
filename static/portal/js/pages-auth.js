document.addEventListener("DOMContentLoaded", function () {
  const formAuthentication = document.querySelector("#formAuthentication");
  const btnSubmit = document.getElementById("btnSubmit");
  const btnText = document.getElementById("btnText");
  const btnLoader = document.getElementById("btnLoader");
  const errorContainer = document.getElementById("errorContainer");

  if (formAuthentication) {
      formAuthentication.addEventListener("submit", function (event) {
          event.preventDefault();

          // Disable button and show loading state
          btnSubmit.classList.add("disabled");
          btnText.textContent = "Signing in...";
          btnLoader.classList.remove("visually-hidden");
          errorContainer.style.display = "none"; // Hide previous errors

          const formData = new FormData(formAuthentication);

          fetch(formAuthentication.action, {
              method: "POST",
              body: formData,
              headers: {
                  "X-Requested-With": "XMLHttpRequest",
              },
          })
              .then((response) => response.json())
              .then((data) => {
                  if (data.success) {
                      window.location.href = data.redirect_url;
                  } else {
                      showError(data.message);
                      resetButton();
                  }
              })
              .catch(() => {
                  showError("Something went wrong. Please try again.");
                  resetButton();
              });
      });

      function showError(message) {
          errorContainer.textContent = message;
          errorContainer.style.display = "block";
          setTimeout(() => {
              errorContainer.style.display = "none";
          }, 3000); // Hide after 3 seconds
      }

      function resetButton() {
          btnSubmit.classList.remove("disabled");
          btnText.textContent = "Sign In";
          btnLoader.classList.add("visually-hidden");
      }
  }
});
