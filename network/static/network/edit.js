document.addEventListener('DOMContentLoaded', function() {
    // check if user is logged in
    if (document.querySelector('#current-user')) {
        // identify current user
        const username = document.querySelector('#current-user').text;

        // find all the post contents on the page
        document.querySelectorAll('.post-content').forEach(content => {
            let post_id = content.id.split('_')[1];
            const content_username = content.id.split('_')[2];
            let user_id = content.id.split('_')[3];
    
            // insert edit button for current user's posts
            if (username === content_username) {
                const edit_div = document.createElement('div');
                edit_div.id = `edit_${post_id}`
    
                const edit_button = document.createElement('button');
                edit_button.id = `edit-button_${post_id}_${user_id}`
                edit_button.className = 'edit-button btn btn-outline-secondary btn-sm mt-2'
                edit_button.innerHTML = 'Edit';
    
                document.querySelector(`#post_${post_id}`).append(edit_div);
                document.querySelector(`#edit_${post_id}`).append(edit_button);
            }        
        });
    
        // create eventlistener for edit buttons
        document.querySelectorAll('.edit-button').forEach(button => {
            button.onclick = function() {
                // get post_id and user_id from button
                post_id = this.id.split('_')[1];
                user_id = this.id.split('_')[2];
    
                // get existing content
                const current_content = document.querySelector(`#post-content_${post_id}_${username}_${user_id}`).innerHTML;
    
                // replace post content with textarea form
                const replace_text = document.querySelector(`#post-content_${post_id}_${username}_${user_id}`);
                replace_text.style.display = 'none';
                const form = document.querySelector(`#content-form_${post_id}`);

                // display the content form
                form.style.display = 'block';

                // add current_content to textarea
                document.querySelector(`#content-text_${post_id}`).value = current_content.trim();
    
                // change edit button to submit button
                document.querySelector(`#edit-button_${post_id}_${user_id}`).style.display = 'none';

                // content form eventlistener
                document.querySelector(`#content-form_${post_id}`).addEventListener('submit', e => {
                    e.preventDefault();

                    // acquire text value of textfield
                    const new_text = document.querySelector(`#content-text_${post_id}`).value;
                    console.log(new_text);

                    // acquire csrf token
                    const csrftoken = getCookie('csrftoken');

                    // fetch update api
                    fetch(`api/update/${user_id}/${post_id}`, {
                        method: 'PUT',
                        mode: 'same-origin',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify({
                            content: new_text
                        })
                    })
                    .then(response => response.json())
                    .then(message => {
                        console.log(message);

                        // TODO: hide the form

                        // TODO: update the post with the new content
                    })
                    .catch(error => {
                        console.log('Error:', error);
                    })
                })

            }
        });


    }
});


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