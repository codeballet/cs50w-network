document.addEventListener('DOMContentLoaded', function() {
    // listen to follow unfollow submits
    document.querySelector('#follow-form').onsubmit = e => {
        e.preventDefault();
        console.log(e);
    }
})