function showCode(code){
    block = document.getElementById("commandCodeBlock")
    block.textContent = code;
    hljs.highlightBlock(block);
}