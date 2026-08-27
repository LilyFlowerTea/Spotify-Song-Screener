console.log("Hello from JavaScript!");

const output = document.getElementById("output");

output.textContent = "JavaScript changed this!";

const button = document.getElementById("submission");

button.addEventListener("click", function(){
   console.log("Button clicked")
});