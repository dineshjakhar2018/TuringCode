/* password show code start */
function togglePasswordVisibility() {
    var passwordInput = document.getElementById("passwordInput");
    var passwordIcon = document.getElementById("passwordIcon");
  
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      passwordIcon.classList.add("fa-eye");
      passwordIcon.classList.remove("fa-eye-slash");
    } else {
      passwordInput.type = "password";
      passwordIcon.classList.add("fa-eye-slash");
      passwordIcon.classList.remove("fa-eye");
    }
  }


  function togglePasswordVisibility1() {
    var passwordInput = document.getElementById("passwordInput1");
    var passwordIcon = document.getElementById("passwordIcon1");
  
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      passwordIcon.classList.add("fa-eye");
      passwordIcon.classList.remove("fa-eye-slash");
    } else {
      passwordInput.type = "password";
      passwordIcon.classList.add("fa-eye-slash");
      passwordIcon.classList.remove("fa-eye");
    }
  }
  
  /* password show code end */


/* register checkbox start */
function toggleCheckbox() {
    var checkbox = document.getElementById("myCheckbox");
    
    if (checkbox.checked) {
      // Checkbox is checked
      console.log("Checkbox is checked");
      // Perform actions when the checkbox is checked
    } else {
      // Checkbox is unchecked
      console.log("Checkbox is unchecked");
      // Perform actions when the checkbox is unchecked
    }
  }


/* testseries numeric type answer */
function insertValue(value) {
  var textbox = document.getElementById('nat-answer');
  textbox.value += value;
}

function backspace() {
  var textbox = document.getElementById('nat-answer');
  var currentValue = textbox.value;
  textbox.value = currentValue.slice(0, -1);
}

function moveCursorLeft() {
  var textbox = document.getElementById('nat-answer');
  if (textbox.selectionStart > 0) {
    textbox.selectionStart--;
    textbox.selectionEnd = textbox.selectionStart;
  }
}

function moveCursorRight() {
  var textbox = document.getElementById('nat-answer');
  if (textbox.selectionStart < textbox.value.length) {
    textbox.selectionStart++;
    textbox.selectionEnd = textbox.selectionStart;
  }
}



function SolutionVideo() {
  // Get all elements with the class "video-solution-button"
  var buttons = document.getElementsByClassName("video-solution-button");

  // Get the modal element
  var modal = document.getElementById("myModal");
  var videoPlayer = document.getElementById("videoPlayer");

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // Function to open the modal and update the video source
  function openModal() {
    var videoUrl = this.getAttribute("data-video-url");
    videoPlayer.setAttribute("src", videoUrl);

    // Calculate the position to display the modal
    var buttonRect = this.getBoundingClientRect();
    var buttonTop = buttonRect.top + window.pageYOffset;
    modal.style.top = buttonTop + "px";

    modal.style.display = "block";
    videoPlayer.play(); // Play the video
  }

  // Function to close the modal and pause the video
  function closeModal() {
    videoPlayer.pause(); // Pause the video
    videoPlayer.removeAttribute("src"); // Clear the video source
    modal.style.display = "none";
  }

  // Attach click event handlers to all buttons with the class "video-solution-button"
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", openModal);
  }

  // Attach click event handler to the <span> element to close the modal
  span.addEventListener("click", closeModal);

  // Attach click event handler to window to close the modal when clicking outside of it
  window.addEventListener("click", function (event) {
    if (event.target == modal) {
      closeModal();
    }
  });
}

// Call the function to enable the solution video functionality
SolutionVideo();

