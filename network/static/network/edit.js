document.addEventListener('DOMContentLoaded', function() {
    // identify current user
    const username = document.querySelector('#current-user').text;

    // find all the post contents on the page
    document.querySelectorAll('.post-content').forEach(content => {
        post_id = content.id.split('_')[1];
        content_username = content.id.split('_')[2];

        // insert edit button for current user's posts
        if (username === content_username) {
            const edit_div = document.createElement('div');
            edit_div.id = `edit_${post_id}`

            const edit_button = document.createElement('button');
            edit_button.id = `edit-button_${post_id}`
            edit_button.className = 'edit-button btn btn-outline-secondary btn-sm mt-2'
            edit_button.innerHTML = 'Edit';

            document.querySelector(`#post_${post_id}`).append(edit_div);
            document.querySelector(`#edit_${post_id}`).append(edit_button);
        }        
    });

    // create eventlistener for edit buttons
    document.querySelectorAll('.edit-button').forEach(button => {
        button.onclick = function() {
            console.log(this.id);
            console.log(post_id);

            // get existing content
            const current_content = document.querySelector(`#post-content_${post_id}_${username}`).innerHTML;
            console.log(current_content);

            // create a text element
            const text_div = document.createElement('div');
            text_div.id = `textarea_${post_id}`;
            const textarea = document.createElement('textarea');
            textarea.id = `textarea_${post_id}`
            textarea.innerText = current_content.trim();

            // replace post content with textarea
            const replace_text = document.querySelector(`#post-content_${post_id}_${username}`);
            replace_text.replaceWith(text_div);
            document.querySelector(`#textarea_${post_id}`).append(textarea);

            // fetch to update content
            
        }
    });
});