// confirm js is working
console.log("Hello from JavaScript!");

// monitor buttons for clicks
const target_song_button = document.getElementById("target song submission");
const playlist_button = document.getElementById("playlist submission");

// main event 1
target_song_button.addEventListener("click", async function(){
    // pull the str entered into the submission field
    const target_song_url = document.getElementById("target song url").value
    // send off data to main.py through FastAPI
    const response = await fetch("/analysis", {
        method : "POST",
        body : JSON.stringify({target_song_url : target_song_url}),
        headers : {
            "Content-Type" : "application/json"
        }
    })
    // assign response
    const data = await response.json()
    // assign text to be rewritten
    const target_song_output = document.getElementById("target_song_output")
    // overwrite text on page
    target_song_output.textContent = data.target_song_url
    console.log("complete")
});


//
// HEY LISTEN UP I DIDN'T FIGURE OUT HOW TO PUT IN TWO FIELDS AND SUBMIT THE WHOLE THING AT ONCE
// SO MAIN EVENT 2 WHICH IS FOUND BELOW HAS BAD REFERENCES TO TARGET_SONG_URL AND THE LIKE
// NEED TO FIX THAT WHEN POSSIBLE
//

// main event 2
playlist_button.addEventListener("click", async function(){
    // pull the str entered into the submission field
    const target_song_url = document.getElementById("playlist url").value
    // send off data to main.py through FastAPI
    const response = await fetch("/analysis", {
        method : "POST",
        body : JSON.stringify({target_song_url : target_song_url}),
        headers : {
            "Content-Type" : "application/json"
        }
    })
    // assign response
    const data = await response.json()
    // assign text to be rewritten
    const playlist_output = document.getElementById("playlist_output")
    // overwrite text on page
    playlist_output.textContent = data.target_song_url
    console.log("complete")
});