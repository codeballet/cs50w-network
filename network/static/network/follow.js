document.addEventListener('DOMContentLoaded', function() {
    // profile being looked at
    profile_id = window.location.pathname.split('/')[1];

    // listen to follow or unfollow submits
    document.querySelector('#follow-form').onsubmit = e => {
        e.preventDefault();
        follow(profile_id)
    }

    // populate the followers element
    followers(profile_id);

    // populate the following element
    following(profile_id);
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


function followers(profile_id) {
    // fetch the count of users following the profile_id
    fetch(`followers/${profile_id}`)
    .then(response => response.json())
    .then(message => {
        // update the followers HTML element
        document.querySelector('#followers').innerHTML = message.count;
    })
    .catch(error => {
        console.log('Error:', error);
    })
}


function following(profile_id) {
    // fetch the count of users the profile_id is following
    fetch(`following/${profile_id}`)
    .then(response => response.json())
    .then(message => {
        // update the following HTML element
        document.querySelector('#following').innerHTML = message.count;
    })
    .catch(error => {
        console.log('Error:', error);
    });
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