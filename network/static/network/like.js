document.addEventListener('DOMContentLoaded', () => {
    document.getElementsByName('like_btn').forEach(like_btn => {
        like_btn.onclick = () => {
            postId = like_btn.id;
            
            // Check if already liked the post
            fetch(`/like/${postId}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {

                if (data.status === 'liked') {
                    like_btn.style.background = red;
                } 
                else {
                    like_btn.style.background = black;
                }

            })
        }
    })
})