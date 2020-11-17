function hideAllCategories(){
    for (category of document.getElementsByClassName("category")){
        category.style.display = "none";
    }
}

function showCategoryById(id){
    let category = document.getElementById(id);

    if (category == null){
        console.error(`No category with the id ${id} found.`);
    }
    
    else{
        category.style.display = "block";
    }
}

function showCode(code){
    block = document.getElementById("commandCodeBlock")
    block.textContent = code;
    hljs.highlightBlock(block);
}