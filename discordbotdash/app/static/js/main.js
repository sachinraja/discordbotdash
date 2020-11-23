function showCode(code){
    block = document.getElementById("commandCodeBlock")
    block.textContent = code;
    hljs.highlightBlock(block);
}

//insert placeholder command
onload = function(){
    showCode(`@bot.command()
    async def example(ctx):
        """Example Command in Command Code"""
        await ctx.send("This is an example!")`);
}