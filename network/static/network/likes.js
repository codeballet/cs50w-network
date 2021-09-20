document.addEventListener('DOMContentLoaded', function() {

    // change eventlistener to listen for like-form instead of button
    document.querySelectorAll('.like-button').forEach(button => {
        button.onclick = function(e) {
            // get the post id from button id
            button_id = e.target.id;
            post_id = button_id.split("_")[1];

            likes(post_id);
        };
    });
});

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
    .then( response => response.json())
    .then(message => {
        console.log(message);
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