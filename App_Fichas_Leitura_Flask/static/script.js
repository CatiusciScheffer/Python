
function toggleCheckbox(checkedId, uncheckedId) {
    var checkedElement = document.getElementById(checkedId);
    var uncheckedElement = document.getElementById(uncheckedId);
    if (checkedElement.checked) {
        uncheckedElement.checked = false;
    }
}

function editBook(bookId) {
    window.location.href = '/edit/' + bookId;
}

function redirectToIndex() {
    window.location.href = "/";  // Redireciona para a página inicial (index)
}
