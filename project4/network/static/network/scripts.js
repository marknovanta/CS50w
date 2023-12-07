document.addEventListener('DOMContentLoaded', () => {
    
    if (document.querySelector('#header').innerHTML === 'All Posts') {
        // By default, submit button disabled
        document.querySelector('#postingBtn').disabled = true;
    
        document.querySelector('#content').onkeyup = () => {
            if (document.querySelector('#content').value.length > 0) {
                document.querySelector('#postingBtn').disabled = false;
            }
            else {
                document.querySelector('#postingBtn').disabled = true;
            }
            
        }
    }
    
    
})


function showEdit(id) {
    document.querySelector(`#textArea${id}`).style.display = 'block';
    document.querySelector(`#saveBtn${id}`).style.display = 'block';
    document.querySelector(`#editBtn${id}`).style.display = 'none';
    
    document.querySelector(`#saveBtn${id}`).disabled = true;
    document.querySelector(`#textArea${id}`).onkeyup = () => {
        if (document.querySelector(`#textArea${id}`).value.length > 0) {
            document.querySelector(`#saveBtn${id}`).disabled = false;
        }
        else {
            document.querySelector(`#saveBtn${id}`).disabled = true;
        }
        
    }
}

function editPost(id) {
    const content = document.querySelector(`#textArea${id}`).value;
    console.log(content)
    console.log(id)
    document.querySelector(`#textArea${id}`).style.display = 'none';
    document.querySelector(`#saveBtn${id}`).style.display = 'none';
    document.querySelector(`#editBtn${id}`).style.display = 'block';

    fetch(`/post_edit/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: content,
        })
    }).then(() => {
        window.location.reload();
    })
}

function like(id) {
    fetch(`/like_dislike/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            action: 'like',
        })
    }).then(() => {
        window.location.reload();
    })
}

function dislike(id) {
    fetch(`/like_dislike/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            action: 'dislike',
        })
    }).then(() => {
        window.location.reload();
    })
}