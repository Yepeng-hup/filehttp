const input = document.getElementById("text_input"), input2 = document.getElementById("text_input2"),
    btn = document.getElementById("btn"), btn2 = document.getElementById("btn2");

function copyText() {
    input.select(), document.execCommand("copy"), btn.innerHTML = "Copied!", setTimeout(() => {
        btn.innerHTML = '<img style="height: 20px; width: 20px" src="/static/img/clipboard-outline.svg">'
    }, 2e3)
}

function copyText2() {
    input2.select(), document.execCommand("copy"), btn2.innerHTML = "Copied!", setTimeout(() => {
        btn2.innerHTML = '<img style="height: 20px; width: 20px" src="/static/img/clipboard-outline.svg">'
    }, 2e3)
}

btn.addEventListener("click", copyText), btn2.addEventListener("click", copyText2);