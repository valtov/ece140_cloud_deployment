document.addEventListener("DOMContentLoaded", (event) => {

    var guestBook = document.getElementById("guestbookSubmitButton");

    guestBook.addEventListener("click", function() {
        console.log(guestBook);
        // window.location = ('http://localhost:5000/new_post');
    });
});