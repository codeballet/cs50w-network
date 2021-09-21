document.addEventListener('DOMContentLoaded', function() {
    // listen to follow unfollow submits
    document.querySelector('#follow-form').onsubmit = e => {
        e.preventDefault();
        console.log(e);
        // identify who is to be followed
        profile_id = window.location.pathname.split('/')[1];
        follow(profile_id)
    }
})


function follow(user_id) {
    // acquire csrf token
    const csrftoken = getCookie('csrftoken');

    // fetch the user to follow
    fetch(`follow/${user_id}`, {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
    })
    .catch(error => {
        console.log('Error:', error);
    })
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}