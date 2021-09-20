document.addEventListener('DOMContentLoaded', function() {
    // fill in the like form buttons
    document.querySelectorAll('.like-button').forEach(button => {
        button_text(button.id);
    })

    // listen to like submits
    document.querySelectorAll('.like-form').forEach(form => {        
        form.onsubmit = function(e) {
            // get the post id from form id
            form_id = e.target.id;
            post_id = form_id.split("_")[1];

            likes(post_id);
        };
    });
});


function button_text(button_id) {
    post_id = button_id.split('_')[1];
    // fetch the post

    // check if the post is liked by the current user
    // if so, write 'Unlike' in the button
    const current_user = document.querySelector('#current-user').text
}


function likes(post_id) {
    // acquire csrf token
    const csrftoken = getCookie('csrftoken');

    // register the like
    fetch(`like/${post_id}`, {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
        // update the likes count
        fetch(`likes/${post_id}`)
        .then(response => response.json())
        .then(message => {
            console.log(message);
            document.querySelector(`#likes-count_${post_id}`).innerHTML = message.likes;
        })
        .catch(error => {
            console.log('Error:', error);
        })
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