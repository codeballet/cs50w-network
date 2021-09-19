document.addEventListener('DOMContentLoaded', function() {
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
    // TODO: add csrf token verification

    fetch(`like/${post_id}`, {
        method: 'POST'
    })
    .then( response => response.json())
    .then(message => {
        console.log(message);
    })
}