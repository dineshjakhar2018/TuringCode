function AnswerSubmit() {
    var Nat = $("input[name=NAT]").val();
    var option1 = $("input[name=option1]:checked").val();
    var option2 = $("input[name=option2]:checked").val();
    var option3 = $("input[name=option3]:checked").val();
    var option4 = $("input[name=option4]:checked").val();
    var form_data = $("input[type=radio]:checked").val();
    // Send the data to the Django view using AJAX
    $.ajax({
        type: 'POST',
        url: '/api/save-answer/',
        data: {
            'Nat': Nat,
            'option1' : option1,
            'option2' : option2,
            'option3' : option3,
            'option4' : option4,
            'form_data' : form_data,
            // Include the CSRF token in the request data
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        beforeSend: function(xhr, settings) {
            // Include the CSRF token in the request headers
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data) {
            // On successful form submission, load the next content
            $(".content,.tab-content").load("/api/save-next/");
            // Set the scroll position back to the stored value
        },
        error: function() {
            alert('An error occurred while submitting the form.');
        }
    });
}

// Helper function to get the CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


//this code for clear response
function ClearResponseSubmit() {
    var Nat = 'e'
    // Send the data to the Django view using AJAX
    $.ajax({
        type: 'POST',
        url: '/api/clear-answer/',
        data: {
            'Nat': Nat,
            // Include the CSRF token in the request data
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        beforeSend: function(xhr, settings) {
            // Include the CSRF token in the request headers
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data) {
            // On successful form submission, load the next content
            $(".content,.tab-content").load("/api/question-reload/");
        },
        error: function() {
            alert('An error occurred while submitting the form.');
        }
    });
}

// Helper function to get the CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//this code for clear response
function MarkForReviewSubmit() {
    var Nat = $("input[name=NAT]").val();
    var option1 = $("input[name=option1]:checked").val();
    var option2 = $("input[name=option2]:checked").val();
    var option3 = $("input[name=option3]:checked").val();
    var option4 = $("input[name=option4]:checked").val();
    var form_data = $("input[type=radio]:checked").val();
    // Send the data to the Django view using AJAX
    $.ajax({
        type: 'POST',
        url: '/api/mark-for-review/',
        data: {
            'Nat': Nat,
            'option1' : option1,
            'option2' : option2,
            'option3' : option3,
            'option4' : option4,
            'form_data' : form_data,
            // Include the CSRF token in the request data
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        beforeSend: function(xhr, settings) {
            // Include the CSRF token in the request headers
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data) {
            // On successful form submission, load the next content
            $(".content,.tab-content").load("/api/save-next/");
        },
        error: function() {
            alert('An error occurred while submitting the form.');
        }
    });
}

// Helper function to get the CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}





//this code for clear response
function PaperChange_1() {
    var mydata = $("input[name=CurrentPaper]").val();
    // Send the data to the Django view using AJAX
    $.ajax({
        type: 'POST',
        url: '/api/paper-change-1/',
        data: {
            'mydata': mydata,
            // Include the CSRF token in the request data
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        beforeSend: function(xhr, settings) {
            // Include the CSRF token in the request headers
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data) {
            // On successful form submission, load the next content
            $(".content,.tab-content").load("/api/question-reload/");
        },
        error: function() {
            alert('An error occurred while submitting the form.');
        }
    });
}

// Helper function to get the CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




//this code for paper change
function PaperChange_2() {
    var mydata = $("input[name=CurrentPaper]").val();
    // Send the data to the Django view using AJAX
    $.ajax({
        type: 'POST',
        url: '/api/paper-change-2/',
        data: {
            'mydata': mydata,
            // Include the CSRF token in the request data
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        beforeSend: function(xhr, settings) {
            // Include the CSRF token in the request headers
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data) {
            // On successful form submission, load the next content
            $(".content,.tab-content").load("/api/question-reload/");
        },
        error: function() {
            alert('An error occurred while submitting the form.');
        }
    });
}

// Helper function to get the CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




//onclick in question no then show this question
var question_no;
function MyQuestion(question_no) {
    // Send the data to the Django view using AJAX
    $.ajax({
        type: 'POST',
        url: '/api/question-change/',
        data: {
            'question_no': question_no,
            // Include the CSRF token in the request data
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        beforeSend: function(xhr, settings) {
            // Include the CSRF token in the request headers
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data) {
            // On successful form submission, load the next content
            $(".content,.tab-content").load("/api/question-reload/");
        },
        error: function() {
            alert('An error occurred while submitting the form.');
        }
    });
}

// Helper function to get the CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



//this code for clear response
function PreviousQuestion() {
    var mydata = $("input[name=NAT]").val();
    // Send the data to the Django view using AJAX
    $.ajax({
        type: 'POST',
        url: '/api/previous-question/',
        data: {
            'mydata': mydata,
            // Include the CSRF token in the request data
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        beforeSend: function(xhr, settings) {
            // Include the CSRF token in the request headers
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data) {
            // On successful form submission, load the next content
            $(".content,.tab-content").load("/api/question-reload/");
        },
        error: function() {
            alert('An error occurred while submitting the form.');
        }
    });
}

// Helper function to get the CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




//test final submit 
function onSubmitForm() {
    // Show the confirmation dialog
    var result = window.confirm("Are you sure you want to submit the test!");

    if (result) {
        // User clicked "OK" (Submit), proceed with form submission
        return true;
    } else {
        // User clicked "Cancel", prevent form submission
        return false;
    }
}


//numeric question white space and character not allowed
function onlyNumberKey(evt) {
             
    // Only ASCII character in that range allowed
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode
    if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
        return false;
    return true;
}

function removeSpaces(input) {
    const originalValue = input.value;
    const trimmedValue = originalValue.trim();
    if (originalValue !== trimmedValue) {
        input.value = trimmedValue;
    }
}

