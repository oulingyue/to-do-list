const inputBox = document.getElementById("input-box");

const listContainer = document.getElementById("list-container");

function addTask(){
    if(inputBox.value === '') {
        alert("oops- you just entered an empty to-do... What do you want to do? nothing!? ");
    }
    else{
        let listElement = document.createElement("li");
        listElement.innerHTML = inputBox.value;
        listContainer.appendChild(listElement);

        let span = document.createElement("span");
        span.innerHTML = "\u00d7";
        listElement.appendChild(span);
    }
    inputBox.value = "";
    saveData();
}

listContainer.addEventListener("click", function(e){
    if(e.target.tagName === "LI"){
        e.target.classList.toggle("checked");
        saveData();
    }
    else if(e.target.tagName === "SPAN") {
        e.target.parentElement.remove();
        saveData();
    }
}, false);

function saveData(){
    localStorage.setItem("data", listContainer.innerHTML);
}

function showTask(){
    listContainer.innerHTML = localStorage.getItem("data");
}

showTask();