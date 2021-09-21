document.addEventListener('DOMContentLoaded', function() {
    // profile being looked at
    profile_id = window.location.pathname.split('/')[1];

    // populate the follow button
    if (document.querySelector('#follow-form')) {
        follow_button(profile_id)
    }

    // populate the followers element
    followers(profile_id);

    // populate the following element
    following(profile_id);

    // listen to follow or unfollow submits
    if (document.querySelector('#follow-form')) {
        document.querySelector('#follow-form').onsubmit = e => {
            e.preventDefault();
            follow(profile_id)
        }
    }
})


function follow(user_id) {
    // acquire csrf token
    const csrftoken = getCookie('csrftoken');

    // fetch the user to follow or unfollow
    button_status = document.querySelector('#follow-button').innerHTML.toLowerCase()

    if (button_status === "follow") {
        fetch(`api/follow/${user_id}`, {
            method: 'POST',
            mode: 'same-origin',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(message => {
            console.log(message);
            // update follow button
            follow_button(user_id);
            followers(user_id);
            following(user_id);
        })
        .catch(error => {
            console.log('Error:', error);
        })
    } else {
        fetch(`api/unfollow/${user_id}`, {
            method: 'POST',
            mode: 'same-origin',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(message => {
            console.log(message);
            // update follow button
            follow_button(user_id);
            followers(user_id);
            following(user_id);
        })
        .catch(error => {
            console.log('Error:', error);
        })
    }
}


function followers(profile_id) {
    // fetch the count of users following the profile_id
    fetch(`api/followers/${profile_id}`)
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
    fetch(`api/following/${profile_id}`)
    .then(response => response.json())
    .then(message => {
        // update the following HTML element
        document.querySelector('#following').innerHTML = message.count;
    })
    .catch(error => {
        console.log('Error:', error);
    });
}


function follow_button(profile_id) {
    // check if the current user is following the viewed profile
    fetch(`api/followed/${profile_id}`)
    .then(response => response.json())
    .then(message => {
        console.log(message)
        res = message.following
        // update the follow button
        document.querySelector('#follow-button').innerHTML = res ? 'Unfollow' : 'Follow';
    })
    .catch(error => {
        console.log('Error:', error)
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