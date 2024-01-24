/* question solution pagination code */
document.addEventListener('DOMContentLoaded', function() {
    // Get necessary elements
    const paginationContainer = document.getElementById('pagination');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const pageNumberContainer = document.getElementById('page-numbers');
  
    // Set the number of pages and items per page
    const totalPages = Math.ceil(paginationContainer.children.length / 10);
    let currentPage = 1;
  
    // Function to display the current page
    function showPage(page) {
      // Hide all items
      for (let i = 0; i < paginationContainer.children.length; i++) {
        paginationContainer.children[i].style.display = 'none';
      }
  
      // Calculate the range of items to show on the current page
      const startIndex = (page - 1) * 10;
      const endIndex = startIndex + 10;
  
      // Display the items in the range
      for (let i = startIndex; i < endIndex && i < paginationContainer.children.length; i++) {
        paginationContainer.children[i].style.display = 'block';
      }
  
      // Update the page numbers
      pageNumberContainer.innerHTML = '';
      for (let i = 1; i <= totalPages; i++) {
        const pageNumberButton = document.createElement('span');
        pageNumberButton.classList.add('page-number');
        pageNumberButton.textContent = i;
        if (i === page) {
          pageNumberButton.classList.add('active');
        }
        pageNumberContainer.appendChild(pageNumberButton);
      }
  
      // Disable/enable prev/next buttons based on current page
      prevButton.disabled = page === 1;
      nextButton.disabled = page === totalPages;
    }
  
    // Show the initial page
    showPage(currentPage);
  
    // Event listener for previous button
    prevButton.addEventListener('click', function() {
      if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
      }
    });
  
    // Event listener for next button
    nextButton.addEventListener('click', function() {
      if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
      }
    });
  
    // Event listener for page number buttons
    pageNumberContainer.addEventListener('click', function(event) {
      if (event.target.classList.contains('page-number')) {
        const pageNumber = parseInt(event.target.textContent);
        if (pageNumber !== currentPage) {
          currentPage = pageNumber;
          showPage(currentPage);
        }
      }
    });
  });

//video solution
var coll = document.getElementsByClassName("collapsible");
            var i;
            
            for (i = 0; i < coll.length; i++) {
              coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.maxHeight){
                  content.style.maxHeight = null;
                } else {
                  content.style.maxHeight = content.scrollHeight + "px";
                } 
              });
            }

            /* video player  */
            var video = document.getElementById('my-video');
            var playButton = document.querySelector('.play-button');

            playButton.addEventListener('click', function() {
            video.play();
            playButton.style.display = 'none';
});