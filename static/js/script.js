document.querySelector("html").classList.add("js");
var fileInput = document.querySelector(".input-file"), button = document.querySelector(".input-file-trigger"),
    the_return = document.querySelector(".file-return"), upload = document.querySelector(".upload-file");
button.addEventListener("keydown", function (e) {
    13 != e.keyCode && 32 != e.keyCode || fileInput.focus()
}), button.addEventListener("click", function (e) {
    return fileInput.focus(), !1
}), fileInput.addEventListener("change", function (e) {
    this.value.length > 0 ? the_return.innerHTML = fileInput.files[0].name : the_return.innerHTML = "None"
}), fileInput.addEventListener("change", function (e) {
    "None" != the_return.innerHTML && upload.removeAttribute("hidden")
});