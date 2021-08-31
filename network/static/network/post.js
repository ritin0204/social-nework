document.addEventListener('DOMContentLoaded', function() {
    Newpost();
});
function Newpost(){
 document.querySelector('#newpost').onsubmit = function() {
    const text = document.querySelector('#newpost-text').value;
    const options ={
        method:'POST',
        body: text,
        headers: {
            'Content-Type':'application/json'
        }
    }
    fetch('/newpost',options)
    .then(response => response.json())
    .then(result =>{
        if ("message" in result){
            console.log("posted");
            location.reload();
        }
    });
    return false
 }
document.querySelector('#newpost-text').value = '';
}

function editmypost(postid) {
    fetch(`/editpost/${postid}`)
    .then(response => response.json())
    .then(result =>{
        console.log(result);
        document.getElementById(`first${postid}`).innerHTML=`<form id=""edit-text">
          <div id=""edit-text">
            <textarea class="md-textarea form-control rounded-0" id="editpost-text" rows="3" >${result.text}</textarea>
            <input type="submit" value="Save Post" id = "save-post" class="btn btn-primary" onclick="savemypost(${postid})"/>
          </div>
          </form>`
    });
}

function savemypost(postid){
    const text = document.getElementById('editpost-text').value
    fetch(`/editpost/${postid}`,{
        method:'POST',
        body: text,
        headers: {
            'Content-Type':'application/json'
        }
    })
    .then(response => response.json())
    .then(result =>{
            console.log(result);
            document.getElementById(`first${postid}`).innerHTML=`<h4> ${result.text}<h4>`     
    })
}

function follow(){
    var userid = document.getElementById('follow').value
    fetch(`${userid}`,{
            method:'POST',
            body: JSON.stringify({
              Follow : 1
            })
      })
    .then(response => response.json())
    .then(result =>{
        console.log(result);
        location.reload() ;
      })
    }
function unfollow(){
    var userid = document.getElementById('unfollow').value
    fetch(`${userid}`,{
        method:'POST',
        body: JSON.stringify({
          Unfollow : 1
        })
    })
    .then(response => response.json())
    .then(result =>{
            console.log(result);
            location.reload();
    })
}

function like(postid){
    fetch(`/editpost/${postid}`,{
        method:'PUT',
            body: JSON.stringify({
              likes : 1
           })
    })
    .then(response => response.json())
    .then(result =>{
        console.log(result.likes);
        document.getElementById(`${postid}`).innerHTML=`<strong>Likes :</strong> <span>${result.likes}</span> <strong>Unlikes :</strong> <span>${result.unlikes}</span>`
    })
}
function unlike(postid){
    fetch(`/editpost/${postid}`,{
        method:'PUT',
        body: JSON.stringify({
            unlikes : 1
        })
    })
    .then(response => response.json())
    .then(result =>{
        console.log(result); 
        document.getElementById(`${postid}`).innerHTML=`<strong>Likes :</strong> <span>${result.likes}</span> <strong>Unlikes :</strong> <span>${result.unlikes}</span>`
    })
}
