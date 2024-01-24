function validateForm() {
    var email = document.getElementById('email').value;
    var mobile = document.getElementById('mobile').value;
    var category = document.getElementById('category').value;
    var url = document.getElementById('url').value;

    // Email validation
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Please enter a valid email address.');
        return false;
    }

    // Mobile validation
    var mobileRegex = /^[0-9]{10}$/;
    if (!mobileRegex.test(mobile)) {
        alert('Please enter a valid 10-digit mobile number.');
        return false;
    }

    // Category validation
    if (category === 'Select Category') {
        alert('Please select a category.');
        return false;
    }

    // URL validation
    var urlRegex = /^(ftp|http|https):\/\/[^ "]+$/;
    if (!urlRegex.test(url)) {
        alert('Please enter a valid URL.');
        return false;
    }

    SubmitForm();
    return false; // Prevent form submission
}


function closeModal() {
    document.getElementById('emailVerifyModal').style.display = 'none';
}

//save the form data in db
function SubmitForm() {
    // Get the CSRF token from the cookie
    $.ajax({
        type: 'POST',
        url: '/ugcnet-student-save/',
        data: {
            'email': $("input[name='email']").val(),
            'mobile': $("input[name='mobile']").val(),
            'category': $("select[name='category']").val(),
            'url': $("input[name='url']").val(),
            'examname': 'UGC NET December 2023',
            'subject': '87 Computer Science and Applications',
            'shift': 'Morning',
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data) {
            if(data.status === 'success'){
                if(data.email_already_verified == '1'){
                    window.location.href = '{% url "ugcnet_response" %}';
                }
                else{
                    document.getElementById('emailVerifyModal').style.display = 'block';
                }
            }
        },
        error: function() {
            alert('Something went wrong, please try again');
            
        }
    });
}

function verifyEmailOTP() {
    var otp = document.getElementById('otp').value;
    // Send the OTP to the server for verification
    $.ajax({
        type: 'POST',
        url: '/verify-email-otp/',
        data: {
            'otp': otp,
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data) {
            if(data.error){
                alert(data.error);
            }
            if(data.status === 'success'){
                window.location.href = '{% url "ugcnet_response" %}';   
            }
        },
        error: function(data) {
            alert(data.error);
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



function toggleFAQ(answerId) {
    var selectedAnswer = document.getElementById(answerId);
    var selectedIcon = document.getElementById('icon' + answerId.charAt(answerId.length - 1));

    if (selectedAnswer.style.display === 'none' || selectedAnswer.style.display === '') {
        selectedAnswer.style.display = 'block';
        selectedIcon.textContent = '-';
    } else {
        selectedAnswer.style.display = 'none';
        selectedIcon.textContent = '+';
    }
}