// confirm js is active
console.log("JavaScript activated");

// declare global variables, to be changed by functions later
let button_method = "playlist/album";
let sorted_data = "";
let unsorted_data = "";

// monitor buttons for clicks
const spotify_login_button = document.getElementById("spotify_redirect");
const method_button_list = document.querySelectorAll(".method-button");
const submit_button = document.getElementById("data_submission");

// create variable for all output and overwriting function
const output_text = document.querySelectorAll(".output_text")
function overwrite_output_text(message){
    output_text.forEach(element => {
        element.textContent = ""
        element.style.display = "none"
    })
    const overwrite_message = document.getElementById("overwrite_text_placeholder")
    overwrite_message.style.display = "block"
    overwrite_message.textContent = message
}

// method selection, decides which algorithm to run in the backend
// also assigns elements to be dynamically edited to match comparison selection
const comparison_url_entry_message = document.getElementById("comparison_url_entry_message")
const comparison_output = document.getElementById("comparison_output")
method_button_list.forEach(button => {
    button.addEventListener("click", () => {
        method_button_list.forEach(button => {
            button.classList.remove("active")
        });
        button.classList.add("active")
        button_method = button.dataset.method;
        console.log(`Button method is ${button_method}`)
        comparison_url_entry_message.textContent = `Please paste the full URL of your ${button_method} below`
        comparison_output.textContent = `Your ${button_method} appears here`
    })
})

// generate sorted_switch, initially hidden but will be revealed and checked when the data is displayed
let distance_data = document.getElementById("distance_data")
let unsorted_data_table = ""
let sorted_data_table = ""
const sorted_switch = document.getElementById("sorted_switch")
sorted_switch.addEventListener("change", async function() {
    if (sorted_switch.checked) {
        distance_data.replaceChildren(sorted_data_table)
    }
    else {
        distance_data.replaceChildren(unsorted_data_table)
    }
})

function jsonToTable(data) {
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
    console.log("Header row complete")

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
        console.log("Row " + data_row + " complete")
    }

    table.appendChild(tbody)

    // const to_be_tabled = document.getElementById(ident)
    // // Clear any previous output to prevent buildup
    // to_be_tabled.textContent = ""
    // to_be_tabled.appendChild(table)
    return table
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
    overwrite_output_text("URLs submitted, please wait while data is retrieved and processed")
    // pull the str entered into the submission field
    const target_song_url = document.getElementById("target_song_url").value
    const comparison_url = document.getElementById("comparison_url").value

    // check the urls are valid and that the method chosen matches comparison url submitted
    if (!target_song_url.startsWith("https://open.spotify.com/")){
        console.log("Target URL error")
        overwrite_output_text("Error: the target song URL is empty or malformed. Please re-enter it.")
        return;
    }
    else if (!comparison_url.startsWith("https://open.spotify.com/")){
        console.log("Comparison URL error")
        overwrite_output_text("Error: the comparison object URL is empty or malformed. Please re-enter it.")
        return;
    }
    const object_type = new URL(comparison_url).pathname.split("/")[1]
    console.log(`Object type is ${object_type}`)
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
    console.log(`Method is ${method}`)

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
    console.log("Response below")
    console.log(response)

    // assign text to be rewritten, needs to be above check for error code 500
    const target_song_output = document.getElementById("target_song_output")
    const comparison_output = document.getElementById("comparison_output")

    if (response.status === 500){
        overwrite_output_text("Error: unable to access data. This may be due to " +
            "an incorrect playlist/album ID, or you may not have access to this data with your account. " +
            "Please try signing in if you have not already. If you have signed in, check your account " +
            "is the owner of the playlist. If you have done all of this, it may be a server issue")
        return;
    }

    // assign response
    const data = await response.json()

    if (data.message){
        window.location.href = "/login_to_cookie"
        return;
    }

    // final failsafe
    if (!data.target_song_name || !data.comparison_name || !data.distance_data || !data.sorted_data){
        overwrite_output_text("Error: data retrieval was unsuccessful. Please check your " +
            "URLs are correct and that you have access to this data. If so, it may be " +
            "an issue with the server.")
        return
    }

    // overwrite text on page
    console.log("Data below")
    console.log(data)
    target_song_output.textContent = data.target_song_name
    comparison_output.textContent = data.comparison_name
    sorted_data = JSON.parse(data.sorted_data)["Sorted data"]
    unsorted_data = JSON.parse(data.distance_data)["Unsorted data"]
    unsorted_data_table = jsonToTable(unsorted_data, "unsorted_table")
    sorted_data_table = jsonToTable(sorted_data, "sorted_table")
    sorted_switch.checked = true
    sorted_switch.style.display = "block"
    console.log("Process complete")
})