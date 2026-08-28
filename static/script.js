// confirm js is active
console.log("Hello from JavaScript!");

// monitor buttons for clicks
const submit_button = document.getElementById("data_submission");

// main event 1
submit_button.addEventListener("click", async function(){
    // pull the str entered into the submission field
    const target_song_url = document.getElementById("target_song_url").value
    const playlist_url = document.getElementById("playlist_url").value
    // send off data to main.py through FastAPI
    const response = await fetch("/analysis", {
        method : "POST",
        body : JSON.stringify({
            target_song_url,
            playlist_url
        }),
        headers : {
            "Content-Type" : "application/json"
        }
    })
    console.log(response)
    // assign response
    const data = await response.json()
    // assign text to be rewritten
    const target_song_output = document.getElementById("target_song_output")
    const playlist_output = document.getElementById("playlist_output")
    // overwrite text on page
    target_song_output.textContent = data.target_song_url
    playlist_output.textContent = data.playlist_url
    console.log("complete")
})