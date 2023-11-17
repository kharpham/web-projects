document.addEventListener("DOMContentLoaded", function() {
    // Allow users to edit their posts
    document.querySelectorAll('.edit').forEach(function(element) {
        element.addEventListener('click', modifyPost);
    });
    document.querySelectorAll('.like-btn').forEach(function(element) {
        element.addEventListener('click', interactPost);
    });
    document.querySelectorAll('.unlike-btn').forEach(function(element) {
        element.addEventListener('click', interactPost);
    });
    document.querySelectorAll('.like-btn2').forEach(function(element) {
        element.addEventListener('click', interactPost);
    });
    document.querySelectorAll('.like-number').forEach(handle_like);
});


function handle_like(element) {
    let id = element.parentNode.id;
    fetch(`/interact_post/${id}`)
    .then(response => response.json())
    .then(post => {
        element.innerText = post.number_likes;
    });
}

function modifyPost() {
    let textarea = this.parentNode.querySelector('textarea');
    let id = this.parentNode.id;
    // Allow edit
    if (this.className === 'edit') {
        this.innerText = 'Save';
        this.className = 'save';
        
        textarea.disabled = false;
        textarea.className = 'modify-textarea';
    }
    // Save editted post
    else if (this.className === 'save') {
        let content = textarea.value;
        //Trim the content to make sure that the user indeed types something
        let trimmed_content = content.trim();
        console.log(content);
        if (trimmed_content != "") {
            fetch(`/post/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: textarea.value,
                }),
            });
            textarea.classList.remove('modify-textarea')
            textarea.disabled = true;
            this.innerText = 'Edit';
            this.className = 'edit';
        }
        else {
            alert('Content could not be empty');
        }
    }   
}


// Handle like/unlike a post
function interactPost() {
    let button = this;
    let username = document.querySelector('#username').innerHTML;
    console.log(username);
    let id = button.parentNode.id;
    console.log(id);    
    fetch(`/interact_post/${id}`)
    .then(response => response.json())
    .then(post => {
        // console.log(post.likes);
        // console.log(post.likes.includes(username));
        likers_list = post.likes;
        likers_number = post.number_likes;
        // The user doens't like the post yet
        if (!post.likes.includes(username)) {
            likers_list.push(username);
            likers_number++;
            // console.log(likers_list);
            // console.log(likers_number);
            button.className = 'like-btn';
            fetch(`/interact_post/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    likes: likers_list,
                    number_likes : likers_number,
                })
            });
            handle_like(this.parentNode.querySelector('.like-number'));
        }
        // The user already likes the post
        else {
            let index = likers_list.indexOf(username);
            likers_list.splice(index, 1);
            console.log(likers_list);
            console.log(likers_number);
           
            likers_number--;
            // button.className = 'unlike-btn';
            button.className = 'unlike-btn';
            fetch(`/interact_post/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    likes: likers_list,
                    number_likes : likers_number,
                })
            });
            handle_like(this.parentNode.querySelector('.like-number'));
        }
    });
}

