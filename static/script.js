// confirm js is active
console.log("Hello from JavaScript!");

// monitor buttons for clicks
const spotify_login_button = document.getElementById("spotify_redirect");
const method_button_list = document.querySelectorAll(".method-button");
const submit_button = document.getElementById("data_submission");

// create variable for all output and overwriting function
const output_text = document.querySelectorAll(".output_text")
function overwrite_output_text(message){
    output_text.forEach(element => {
        element.textContent = ""
    })
    const overwrite_message = document.getElementById("overwrite_text_placeholder")
    overwrite_message.textContent = message
}

// method selection, decides which algorithm to run in the backend
let button_method = "playlist/album";
method_button_list.forEach(button => {
    button.addEventListener("click", () => {
      method_button_list.forEach(button => {
          button.classList.remove("active")
      });
      button.classList.add("active")
      const button_method = button.dataset.method;
      console.log(button_method)
    })
})

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
    // Clear any previous output to prevent visual clogging
    to_be_tabled.textContent = ""
    to_be_tabled.appendChild(table)
}

// Spotify login
spotify_login_button.addEventListener("click", async function() {
    console.log("Spotify login activated")
    window.location.href = "/login_to_cookie"
});

// main event
submit_button.addEventListener("click", async function() {
    // Wait times can be long, so I output this to console to confirm it's active
    console.log("URLs submitted")
    // pull the str entered into the submission field
    const target_song_url = document.getElementById("target_song_url").value
    const comparison_url = document.getElementById("comparison_url").value

    // check the urls are valid and that the method chosen matches comparison url submitted
    if (!target_song_url.startsWith("https://open.spotify.com/")){
        console.log("target url error")
        overwrite_output_text("Error: the target song URL is malformed. Please re-enter it.")
        return;
    }
    else if (!comparison_url.startsWith("https://open.spotify.com/")){
        console.log("comparison url error")
        overwrite_output_text("Error: the comparison object URL is malformed. Please re-enter it.")
        return;
    }
    const object_type = new URL(comparison_url).pathname.split("/")[1]
    console.log("object type")
    console.log(object_type)
    if (button_method !== object_type){
        if (button_method === "playlist/album"){
            if (!(object_type === "playlist" || object_type === "album")){
                overwrite_output_text("Error: you may have selected the wrong comparison method. Please try again.")
                return;
            }
        }
        else {
            overwrite_output_text("Error: you may have selected the wrong comparison method. Please try again.")
            return;
        }
    }

    // convert var name for backend, just to make the var name recognisable at both ends
    const method = button_method
    console.log(method)

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

    // assign text to be rewritten, needs to be above check for error code 500
    const target_song_output = document.getElementById("target_song_output")
    const comparison_output = document.getElementById("comparison_output")

    if (response.status === 500 && method === "playlist/album"){
        overwrite_output_text("Error: unable to access data. This may be due to " +
            "an incorrect playlist/album ID, or you may not have access to this data with your account. " +
            "Please try signing in if you have not already. If you have signed in, check your account" +
            "is the owner of the playlist.")
    }

    // assign response
    const data = await response.json()

    if (data.message){
        window.location.href = "/login_to_cookie"
        return;
    }
    if (!data.target_song_name || !data.comparison_name || !data.distance_data || data.sorted_data){
        overwrite_output_text("Error: data retrieval was unsuccessful. Please check your " +
            "URLs are correct and that you have access to this data. If so, it may be " +
            "an issue with the server.")
        return
    }

    // overwrite text on page
    console.log(data)
    target_song_output.textContent = data.target_song_name
    comparison_output.textContent = data.comparison_name
    const distance_data = JSON.parse(data.distance_data)["Unsorted data"]
    const sorted_data = JSON.parse(data.sorted_data)["Sorted data"]
    jsonToTable(distance_data, "distance_table")
    jsonToTable(sorted_data, "sorted_table")
    console.log("complete")
})
