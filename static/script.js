// confirm js is working
console.log("Hello from JavaScript!");
output.textContent = "JavaScript is active! :)";

// monitor button for clicks
const button = document.getElementById("submission");

// main event
button.addEventListener("click", async function(){
    // pull the str entered into the submission field
    const input = document.getElementById("name").value
    // print out input on page just to check
    output.textContent = input
    // send off data to main.py through FastAPI
    const response = await fetch("/hello", {
        method : "POST",
        body : JSON.stringify({name : input}),
        headers : {
            "Content-Type" : "application/json"
        }
    })
    // assign response
    const data = await response.json()
    // assign text to be rewritten
    const greeting = document.getElementById("greeting")
    // overwrite text on page
    greeting.textContent = data.message
    console.log("complete")
});