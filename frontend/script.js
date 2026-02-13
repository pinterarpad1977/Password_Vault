const API_URL = "http://localhost:8000";

/* API helper object
This keeps code readable and avoids repeating fetch logic everywhere.*/

const api = {
    async getEntries() {
        const res = await fetch(`${API_URL}/entries?password=${encodeURIComponent(masterPassword)}`); 
        if (!res.ok) throw new Error("Failed to load entries");
        return res.json();    
    },

    async addEntry(entry) {
        const res = await fetch(`${API_URL}/entries?password=${encodeURIComponent(masterPassword)}`, {
            method: "POST",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify(entry)
        });
        if (!res.ok) throw new Error("Failed to add entry");
        return res.json();
    },

    async updateEntry(id, entry) {
        const res = await fetch(`${API_URL}/entries/${id}?password=${encodeURIComponent(masterPassword)}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(entry)
        });
        if (!res.ok) throw new Error("Failed to update entry.");
        return res.json();
    },

    async deleteEntry(id) {
        const res = await fetch(`${API_URL}/entries/${id}?password=${encodeURIComponent(masterPassword)}`, {
            method: "DELETE"
        });
        if (!res.ok) throw new Error("Failed to delete entry.");
    }
};


let masterPassword = null;
let editingId = null;
let entries = [];
let showPassword = false;
let darkMode = false;

const output = document.getElementById("output");
const button = document.getElementById("toggle");
const form = document.getElementById("addForm");
const serviceInput = document.getElementById("service");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const notesInput = document.getElementById("notes");
const unlockButton = document.getElementById("unlockButton");
const masterPasswordInput = document.getElementById("masterPasswordInput");


// toggle dark mode
const darkButton = document.getElementById("darkmode");

darkButton.addEventListener("click", () => {
    darkMode = !darkMode;  // Toggle the darkmode state
    applyDarkMode();
});

function applyDarkMode() {
    if (!darkButton) return; // in case the button is missing

    if (darkMode) {
        document.body.classList.add("dark-mode");
        darkButton.textContent = "Light mode";
    } else {
        document.body.classList.remove("dark-mode");
        darkButton.textContent = "Dark mode";
    }
}

unlockButton.addEventListener("click", async() => {
    masterPassword = masterPasswordInput.value.trim();

    if (!masterPassword) {
        alert("Please enter your master password.");
        return;
    } 

    try {
        await loadEntriesFromAPI(); // this will fail if the password is wrong

        // if correct
        document.getElementById("unlock-screen").style.display = "none";
        document.getElementById("vault-screen").style.display = "block";
    } catch (err) {
        alert("Incorrect master password");
        console.error(err);
    }

});

function escapeHTML(str) {
    if (typeof str !== "string") {
        return "";
    }
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

async function loadEntriesFromAPI() {
    entries = await api.getEntries();
    render();
}


function render() {
    let html = "";

    for (let e of entries) {
        html += `
        <div class="entry" data-id=${e.id}>
        
            <div class="entry-row">
                <span class="entry-label">Service:</span> ${escapeHTML(e.service)}
            </div>

            <div class="entry-row">
                <span class="entry-label">Username:</span> ${escapeHTML(e.username)}
            </div>

            <div class="entry-row">
                <span class="entry-label">Password:</span> 
                <span class="entry-value">${
                showPassword ? escapeHTML(e.password) : "*".repeat(e.password.length)
            }</span>
            </div>

            <div class="entry-row">
                <span class="entry-label">Notes:</span> ${escapeHTML(e.notes)}
            </div>

            <div class="entry-buttons">
                <button class="edit">Edit</button>
            </div>
            
            <div class="entry-buttons">
                <button class="delete">Delete</button>
            </div>
        </div>`;
    }

    output.innerHTML = html;

    applyDarkMode();

    //update button text
    button.textContent = showPassword
        ? "Mask passwords"
        : "Unmask passwords";
}



button.addEventListener("click", () => {
    showPassword = !showPassword;
    
    render();
});

// initial render
render();



submitButton.addEventListener("click", handleSubmit);

function handleSubmit(event) {
    event.preventDefault(); // prevents page reload

    if (editingId === null) {
        addNewEntry();
    } else {
        saveEditedEntry();
    }
}


async function addNewEntry() {
    const service = serviceInput.value.trim();
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    const notes = notesInput.value.trim();

    if (!service || !username || !password) {
        alert("Please fill in all required fields.");
        return;
    }

    const newEntry = {service, username, password, notes};

    try {
        const created = await api.addEntry(newEntry);

        // Add the backend created entry to our local list
        entries.push(created);

        render();
        form.reset();
    } catch (err) {
        console.error("Failed to add entry:", err);
    }
}

// Unified click handler for DELETE and EDIT buttons
output.addEventListener("click", async (event) => {

    // --- DELETE BUTTON ---
    const deleteBtn = event.target.closest(".delete");
    if (deleteBtn) {
        if (!confirm("Are you sure you want to delete this entry?")) return;

        const entryDiv = deleteBtn.closest(".entry");
        const id = entryDiv.dataset.id;

        try {
            await api.deleteEntry(id);
            entries = entries.filter(e => e.id !== id);
            render();
        } catch (err) {
            console.error(err);
            alert("Failed to delete entry.");
        }

        return; // stop here so edit doesn't also trigger
    }

    // --- EDIT BUTTON ---
    const editBtn = event.target.closest(".edit");
    if (editBtn) {
        const entryDiv = editBtn.closest(".entry");
        const id = entryDiv.dataset.id;
        startEditMode(id);
        return;
    }
});

console.log("Delete/Edit listener attached");


function startEditMode(id) {
    // find the entry we want to edit
    const entry = entries.find(e => e.id === id);
    if (!entry) return; // safety check

    // fill the form with the values
    serviceInput.value = entry.service;
    usernameInput.value = entry.username;
    passwordInput.value = entry.password;
    notesInput.value = entry.notes;

    // store the ID globally, so Save knows what to update
    editingId = id;

    // switch the UI to editing mode
    enterEditUIState();
}

function enterEditUIState() {
    // change the main button text
    submitButton.textContent = "Save Changes";
    // show the Cancel button 
    cancelButton.style.display = "inline-block";
    // hide the success message (just to make sure)
    successMessage.style.display = "none";
    // scroll to the form
    form.scrollIntoView({behavior: "smooth"});
}

function cancelEditMode () {
    form.reset();
    cancelButton.style.display = "none";
    successMessage.style.display = "none";
    submitButton.textContent = "Add Entry";
    form.scrollIntoView({behavior: "smooth"});
}

const successMessage = document.getElementById("successMessage");

function saveEditedEntry() {
    // read values from the form
    const service = serviceInput.value.trim();
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    const notes = notesInput.value.trim();

    // validate (same as for Add mode)
    if (!service || !username || !password) {
        alert("Please fill in all required fields.");
        return;
    }

    // find the entry we are editing
    const entry = entries.find(e => e.id === editingId);
    if (!entry) return;

    // update the values
    entry.service = service;
    entry.username = username;
    entry.password = password;
    entry.notes = notes;

    render();

    // show success pill
    successMessage.textContent = "Changes saved";
    successMessage.style.display = "inline-block";

    // Hide cancel button immediately
    cancelButton.style.display = "none";

    // Reset the form after a short delay
    setTimeout(() => {
        form.reset();
        successMessage.style.display = "none";
        submitButton.textContent = "Add Entry";
        editingId = null;
        },
    1500);
}


