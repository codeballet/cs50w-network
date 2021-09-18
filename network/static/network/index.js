// document.addEventListener('DOMContentLoaded', function() {
//     // listen for submission of new post
//     document.querySelector('#create-form').addEventListener('submit', e => {
//         create_post();
//     });

//     // load posts by default
//     load_posts();
// });


// function create_post() {
//     // acquire csrf token
//     const csrftoken = getCookie('csrftoken');

//     // send POST request to API route create
//     fetch('/posts/create', {
//         method: 'POST',
//         mode: 'same-origin',
//         headers: {
//             'X-CSRFToken': csrftoken
//         },
//         body: JSON.stringify({
//             content: document.querySelector('#create-content').value
//         })
//     })
//     .then(response => response.json())
//     .then(result => {
//         console.log(result);
//     })
//     .catch(error => {
//         console.log('Error:', error);
//     })
// }


// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }


// function load_posts() {
//     fetch(`/posts`)
//     .then(response => response.json())
//     .then(posts => {
//         console.log(posts);
        
//         // loop over the posts object
//         posts.forEach(post => {
//             // create HTML elements
//             const post_div = document.createElement('div');
//             post_div.id = `post_${post.id}`;
//             post_div.className = 'border p-3 mt-2';

//             const username_div = document.createElement('div');
//             username_div.className = 'h4';

//             const content_div = document.createElement('div');

//             const timestamp_div = document.createElement('div');
//             timestamp_div.className = 'text-muted';

//             const likes_div = document.createElement('div');

//             // set the innerHTML of elements
//             username_div.innerHTML = post.creator;
//             content_div.innerHTML = post.content;
//             timestamp_div.innerHTML = post.timestamp;
//             likes_div.innerHTML = `Likes: ${post.likes}`;

//             // append elements to DOM
//             document.querySelector('#posts').append(post_div);
//             document.querySelector(`#post_${post.id}`).append(username_div);
//             document.querySelector(`#post_${post.id}`).append(content_div);
//             document.querySelector(`#post_${post.id}`).append(timestamp_div);
//             document.querySelector(`#post_${post.id}`).append(likes_div);
//         })
//     })
//     .catch(error => {
//         console.log('Error:', error);
//     })
// }