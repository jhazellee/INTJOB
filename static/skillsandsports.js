// DOM References
const form = document.getElementById('sportsSkillsForm');
const countNote = document.getElementById('countNote');
const selectAllBtn = document.getElementById('selectAll');
const clearAllBtn = document.getElementById('clearAll');
const errorMsg = document.getElementById('errorMsg');
const confirmPanel = document.getElementById('confirmPanel');
const selectedTags = document.getElementById('selectedTags');
const continueBtn = document.getElementById('continueBtn');
const editBtn = document.getElementById('editBtn');
const otherInput = document.getElementById('c-other');

// --- SUB-CHOICE CONFIGURATION ---
// Add any new parent-to-child relationships here
const subMenuMap = [
    { parentId: 'c-webdev', childId: 'webdevDetails' },
    { parentId: 'c-dataAnalysis', childId: 'dataAnalysisDetails' } 
    // Ensure the parent checkbox for Data Analysis has id="c-data-analysis"
];

// Helper to get all current checkboxes
const getAllCheckboxes = () => Array.from(document.querySelectorAll("input[type='checkbox']"));

/**
 * Updates the UI count and manages the visibility of ALL sub-skill sections
 */
function updateUI() {
    const allCbs = getAllCheckboxes();
    const checkedCount = allCbs.filter(cb => cb.checked).length;
    
    if (countNote) countNote.textContent = `${checkedCount} selected`;

    // Loop through our map to toggle visibility for all sub-menus
    subMenuMap.forEach(item => {
        const parent = document.getElementById(item.parentId);
        const detailPanel = document.getElementById(item.childId);

        if (parent && detailPanel) {
            if (parent.checked) {
                detailPanel.style.display = 'block';
            } else {
                detailPanel.style.display = 'none';
                // Uncheck children if parent is unchecked
                detailPanel.querySelectorAll("input[type='checkbox']").forEach(cb => cb.checked = false);
            }
        }
    });
}

// --- Event Listeners ---

// 1. Universal Click Handler (for the "Cards")
document.addEventListener('click', (e) => {
    const card = e.target.closest('.subject');
    if (!card || card.classList.contains('other-input')) return;

    const cb = card.querySelector("input[type='checkbox']");
    
    // Toggle only if the user didn't click the checkbox/label directly
    if (cb && e.target !== cb && e.target.tagName !== 'LABEL') {
        cb.checked = !cb.checked;
    }
    updateUI();
});

// 2. Select All
selectAllBtn?.addEventListener('click', () => {
    getAllCheckboxes().forEach(cb => cb.checked = true);
    updateUI();
});

// 3. Clear All
clearAllBtn?.addEventListener('click', () => {
    getAllCheckboxes().forEach(cb => cb.checked = false);
    if (otherInput) otherInput.value = "";
    updateUI();
});

// 4. Form Submission
form.addEventListener('submit', async (e) => {
    e.preventDefault(); 

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.textContent;

    // 1. Collect values
    const selected = getAllCheckboxes()
        .filter(cb => cb.checked)
        .map(cb => cb.value);

    const otherVal = otherInput?.value.trim();
    if (otherVal) selected.push(otherVal);

    // 2. Validation
    if (selected.length === 0) {
        errorMsg.style.display = 'block';
        confirmPanel.style.display = 'none';
        return;
    }

    // 3. UI Feedback
    errorMsg.style.display = 'none';
    submitBtn.disabled = true;
    submitBtn.textContent = "Saving...";

    try {
        // --- UPDATED FETCH URL ---
        // This ensures it hits http://127.0.0.1:5000/save-skills
        const targetUrl = window.location.origin + '/save-skills';
        console.log("Attempting to save to:", targetUrl);

        const response = await fetch('/save-skills', { // Relative path is safest
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ skills: selected })
        });

        // Check if the server actually sent back a JSON response
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server reached but failed: ${response.status} - ${errorText}`);
        }

        const result = await response.json();

        if (result.success) {
            // 5. Success UI
            displayConfirmationTags(selected); 
            confirmPanel.style.display = 'block';
            confirmPanel.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            alert("Database Error: " + result.message);
        }
    } catch (err) {
        console.error("FULL ERROR DETAILS:", err);
        alert("Connection Error: " + err.message + "\n\nCheck if you are logged in and if Flask is running at " + window.location.origin);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
    }
});

function displayConfirmationTags(selected) {
    if (!selectedTags) return; // Safety check
    selectedTags.innerHTML = '';
    selected.forEach(skill => {
        const el = document.createElement('span');
        el.className = 'tag'; // Make sure you have .tag in your CSS!
        el.textContent = skill;
        selectedTags.appendChild(el);
    });
}

// 5. General Nav
continueBtn?.addEventListener('click', () => {
    // If they finished skills and you want them to go to the dashboard:
    window.location.href = '/applicant'; 
    
    // OR, if you want them to pick subjects next:
    // window.location.href = '/subjects'; 
});

editBtn?.addEventListener('click', () => {
    if (confirmPanel) confirmPanel.style.display = 'none';
});

// Run on load
updateUI();