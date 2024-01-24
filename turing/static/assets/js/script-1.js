    var fullscreenElement = document.getElementById("fullscreenElement");
  
    function toggleFullscreen() {
      if (document.fullscreenElement) {
        exitFullscreen();
      } else {
        enterFullscreen();
      }
    }
  
    function enterFullscreen() {
      if (fullscreenElement.requestFullscreen) {
        fullscreenElement.requestFullscreen();
      } else if (fullscreenElement.mozRequestFullScreen) { // Firefox
        fullscreenElement.mozRequestFullScreen();
      } else if (fullscreenElement.webkitRequestFullscreen) { // Chrome, Safari, and Opera
        fullscreenElement.webkitRequestFullscreen();
      } else if (fullscreenElement.msRequestFullscreen) { // Internet Explorer and Edge
        fullscreenElement.msRequestFullscreen();
      }
    }
  
    function exitFullscreen() {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.mozCancelFullScreen) { // Firefox
        document.mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) { // Chrome, Safari, and Opera
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) { // Internet Explorer and Edge
        document.msExitFullscreen();
      }
    }

    /*loading */
    window.addEventListener('load', function() {
      var loadingContainer = document.getElementById('loadingContainer');
      loadingContainer.style.display = 'none';
    });

//test series timer code
