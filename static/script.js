// confirm js is active
console.log("Hello from JavaScript!");

// monitor buttons for clicks
const submit_button = document.getElementById("data_submission");

const test = document.getElementById("test_text")

function jsonToTable(data) {
    if (!data) return;

    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");
    const row = document.createElement("tr")

    table.appendChild(tbody)
    const distance_table = document.getElementById("distance_table")
    distance_table.appendChild(table)

    const headers = Object.keys(data)
    console.log(headers)
    test.textContent = headers

    for (const header of headers){
        let header = headers[header]
        
    }
}

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
    const distance_table = data.distance_table
    const ranked_table = data.ranked_table
    console.log(distance_table)
    console.log(typeof distance_table)
    jsonToTable(distance_table)
    console.log("complete")
})
