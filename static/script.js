// confirm js is active
console.log("Hello from JavaScript!");

// monitor buttons for clicks
const submit_button = document.getElementById("data_submission");

function jsonToTable(data, elementId) {
    if (!data) return;

    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");
    const row = document.createElement("tr")

    // make header row
    const headers = ["Index", "Song", "Distance"]
    for (const header of headers) {
        const head = document.createElement("th")
        head.textContent = header
        row.appendChild(head)
        }
    thead.appendChild(row)
    table.appendChild(thead)
    console.log("header row complete")

    for (let data_row = 0; data_row < data.length; data_row++) {
        const row = document.createElement("tr")
        const index_num = document.createElement("td")
        const song_name = document.createElement("td")
        const song_data = document.createElement("td")
        const index_num_num = data_row + 1
        const song_name_name = data[data_row][0]
        const song_data_data = data[data_row][1]
        index_num.textContent = index_num_num
        song_name.textContent = song_name_name
        song_data.textContent = song_data_data
        row.appendChild(index_num)
        row.appendChild(song_name)
        row.appendChild(song_data)
        tbody.appendChild(row)
        console.log("row " + data_row + " complete")
    }

    table.appendChild(tbody)

    const to_be_tabled = document.getElementById(elementId)
    to_be_tabled.appendChild(table)
}

// main event
submit_button.addEventListener("click", async function() {
    // Wait times can be long, so I write this to console to confirm it's active
    console.log("URLs submitted")
    // pull the str entered into the submission field
    const target_song_url = document.getElementById("target_song_url").value
    const comparison_url = document.getElementById("comparison_url").value
    const method = document.getElementById("method").value
    // send off data to main.py through FastAPI
    const response = await fetch("/data_request", {
        method : "POST",
        body : JSON.stringify({
            target_song_url,
            comparison_url,
            method
        }),
        headers : {
            "Content-Type" : "application/json"
        }
    })
    console.log(response)
    // assign text to be rewritten
    const target_song_output = document.getElementById("target_song_output")
    const comparison_output = document.getElementById("comparison_output")
    // assign response
    const data = await response.json()

    // overwrite text on page
    target_song_output.textContent = data.target_song_url
    comparison_output.textContent = data.playlist_url
    const distance_data = JSON.parse(data.distance_data)["Unsorted data"]
    const sorted_data = JSON.parse(data.sorted_data)["Sorted data"]
    jsonToTable(distance_data, "distance_table")
    jsonToTable(sorted_data, "sorted_table")
    console.log("complete")
})
