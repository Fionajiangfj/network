 function handleEditClick(postId) {
    // Replace the post content with a textarea
    const postElement = document.getElementById(postId);
    const postContent = postElement.textContent;
    const textarea = document.createElement('textarea');
    textarea.className = "container";
    textarea.value = postContent;
    postElement.textContent = '';
    postElement.appendChild(textarea);

    // Create a "Save" button
    const saveButton = document.createElement('button');
    saveButton.textContent = 'Save';
    saveButton.className = "btn btn-primary"
    saveButton.addEventListener('click', () => {
        const editedContent = textarea.value;

        // Fetch CSRF token from cookies
        const getCookie = (name) => {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        };

        const csrftoken = getCookie('csrftoken');

        // Send the edited content to the server via AJAX
        fetch(`/edit/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ content: editedContent }) // send the edited content
        })
        .then(response => response.json()) // assuming the server response with json
        
        // Update the UI with the edited content
        .then(data => {
            postElement.textContent = data.updatedContent;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    postElement.appendChild(saveButton);
}


document.addEventListener('DOMContentLoaded', () => {
    document.getElementsByName('edit_btn').forEach(button => {
        button.onclick = () => {
            const postID = button.dataset.edit;
            handleEditClick(postID);
        };
    })
})