// Recipe Transformer - Frontend Logic

// API endpoints
const API_BASE = '/api';
const TRANSFORM_ENDPOINT = `${API_BASE}/transform`;
const VALIDATE_ENDPOINT = `${API_BASE}/validate`;
const SCHEMA_ENDPOINT = `${API_BASE}/schema`;

// DOM elements
const inputSchema = document.getElementById('inputSchema');
const outputSchema = document.getElementById('outputSchema');
const transformBtn = document.getElementById('transformBtn');
const validateBtn = document.getElementById('validateBtn');
const loadSampleBtn = document.getElementById('loadSampleBtn');
const clearInputBtn = document.getElementById('clearInputBtn');
const copyOutputBtn = document.getElementById('copyOutputBtn');
const downloadBtn = document.getElementById('downloadBtn');
const fileUpload = document.getElementById('fileUpload');
const inputStatus = document.getElementById('inputStatus');
const outputStatus = document.getElementById('outputStatus');
const transformStatus = document.getElementById('transformStatus');
const btnText = transformBtn.querySelector('.btn-text');
const btnLoader = transformBtn.querySelector('.btn-loader');

// Sample recipe data
const sampleRecipe = {
    "output": {
        "recipe": {
            "connectors": [
                "salesforce",
                "slack",
                "jira"
            ]
        },
        "connectors_icons": [
            {
                "connector": "salesforce",
                "icon": "salesforce-icon"
            },
            {
                "connector": "slack",
                "icon": "slack-icon"
            },
            {
                "connector": "jira",
                "icon": "jira-icon"
            }
        ]
    }
};

// Utility functions
function showStatus(element, message, type = 'info') {
    element.textContent = message;
    element.className = `status-message show ${type}`;
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}

function hideStatus(element) {
    element.classList.remove('show');
}

function setLoading(isLoading) {
    if (isLoading) {
        transformBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
    } else {
        transformBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

function formatJSON(jsonString) {
    try {
        const parsed = JSON.parse(jsonString);
        return JSON.stringify(parsed, null, 2);
    } catch (e) {
        return jsonString;
    }
}

function isValidJSON(str) {
    try {
        JSON.parse(str);
        return true;
    } catch (e) {
        return false;
    }
}

// API calls
async function transformRecipe() {
    const input = inputSchema.value.trim();
    
    if (!input) {
        showStatus(transformStatus, '⚠️ Please provide input schema', 'warning');
        return;
    }
    
    if (!isValidJSON(input)) {
        showStatus(transformStatus, '❌ Invalid JSON format in input', 'error');
        return;
    }
    
    setLoading(true);
    hideStatus(transformStatus);
    hideStatus(outputStatus);
    
    try {
        const response = await fetch(TRANSFORM_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                input: JSON.parse(input)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            outputSchema.value = JSON.stringify(data.output, null, 2);
            showStatus(transformStatus, `✅ ${data.message}`, 'success');
            showStatus(outputStatus, '✓ Transformation successful', 'success');
            
            // Enable output buttons
            copyOutputBtn.disabled = false;
            downloadBtn.disabled = false;
        } else {
            showStatus(transformStatus, `❌ ${data.error}`, 'error');
            outputSchema.value = '';
            copyOutputBtn.disabled = true;
            downloadBtn.disabled = true;
        }
    } catch (error) {
        showStatus(transformStatus, `❌ Network error: ${error.message}`, 'error');
        outputSchema.value = '';
        copyOutputBtn.disabled = true;
        downloadBtn.disabled = true;
    } finally {
        setLoading(false);
    }
}

async function validateSchema() {
    const input = inputSchema.value.trim();
    
    if (!input) {
        showStatus(inputStatus, '⚠️ Please provide input to validate', 'warning');
        return;
    }
    
    if (!isValidJSON(input)) {
        showStatus(inputStatus, '❌ Invalid JSON format', 'error');
        return;
    }
    
    validateBtn.disabled = true;
    hideStatus(inputStatus);
    
    try {
        const response = await fetch(VALIDATE_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                input: JSON.parse(input)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.valid) {
                showStatus(inputStatus, '✅ Input already conforms to recipe-schema-draft-01.json format', 'success');
            } else {
                showStatus(inputStatus, 'ℹ️ Input needs transformation to conform to schema', 'info');
            }
        } else {
            showStatus(inputStatus, `❌ ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(inputStatus, `❌ Network error: ${error.message}`, 'error');
    } finally {
        validateBtn.disabled = false;
    }
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    
    if (!file) {
        return;
    }
    
    // Check if file is JSON
    if (!file.name.endsWith('.json') && file.type !== 'application/json') {
        showStatus(inputStatus, '⚠️ Please upload a JSON file', 'warning');
        event.target.value = ''; // Reset file input
        return;
    }
    
    // Check file size (limit to 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    if (file.size > maxSize) {
        showStatus(inputStatus, '⚠️ File size exceeds 10MB limit', 'warning');
        event.target.value = ''; // Reset file input
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = function(e) {
        try {
            const content = e.target.result;
            
            // Validate JSON
            if (!isValidJSON(content)) {
                showStatus(inputStatus, '❌ Invalid JSON format in file', 'error');
                event.target.value = ''; // Reset file input
                return;
            }
            
            // Format and load the JSON
            inputSchema.value = formatJSON(content);
            showStatus(inputStatus, `✅ File "${file.name}" loaded successfully`, 'success');
            
            // Clear output
            outputSchema.value = '';
            copyOutputBtn.disabled = true;
            downloadBtn.disabled = true;
            hideStatus(outputStatus);
            hideStatus(transformStatus);
        } catch (error) {
            showStatus(inputStatus, `❌ Error reading file: ${error.message}`, 'error');
            event.target.value = ''; // Reset file input
        }
    };
    
    reader.onerror = function() {
        showStatus(inputStatus, '❌ Error reading file', 'error');
        event.target.value = ''; // Reset file input
    };
    
    reader.readAsText(file);
}

function loadSample() {
    inputSchema.value = JSON.stringify(sampleRecipe, null, 2);
    showStatus(inputStatus, '✓ Sample recipe loaded - Try transforming it!', 'success');
    outputSchema.value = '';
    copyOutputBtn.disabled = true;
    downloadBtn.disabled = true;
    hideStatus(outputStatus);
}

function clearInput() {
    inputSchema.value = '';
    outputSchema.value = '';
    hideStatus(inputStatus);
    hideStatus(outputStatus);
    hideStatus(transformStatus);
    copyOutputBtn.disabled = true;
    downloadBtn.disabled = true;
}

function copyOutput() {
    const output = outputSchema.value;
    
    if (!output) {
        showStatus(outputStatus, '⚠️ No output to copy', 'warning');
        return;
    }
    
    navigator.clipboard.writeText(output).then(() => {
        showStatus(outputStatus, '✅ Copied to clipboard!', 'success');
    }).catch(err => {
        showStatus(outputStatus, `❌ Failed to copy: ${err.message}`, 'error');
    });
}

function downloadOutput() {
    const output = outputSchema.value;
    
    if (!output) {
        showStatus(outputStatus, '⚠️ No output to download', 'warning');
        return;
    }
    
    try {
        const blob = new Blob([output], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `transformed_schema_${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showStatus(outputStatus, '✅ Downloaded successfully!', 'success');
    } catch (error) {
        showStatus(outputStatus, `❌ Download failed: ${error.message}`, 'error');
    }
}

// Event listeners
transformBtn.addEventListener('click', transformRecipe);
validateBtn.addEventListener('click', validateSchema);
loadSampleBtn.addEventListener('click', loadSample);
clearInputBtn.addEventListener('click', clearInput);
copyOutputBtn.addEventListener('click', copyOutput);
downloadBtn.addEventListener('click', downloadOutput);
fileUpload.addEventListener('change', handleFileUpload);

// Keyboard shortcuts
inputSchema.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to transform
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        transformRecipe();
    }
    
    // Tab key for indentation
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = e.target.selectionStart;
        const end = e.target.selectionEnd;
        e.target.value = e.target.value.substring(0, start) + '  ' + e.target.value.substring(end);
        e.target.selectionStart = e.target.selectionEnd = start + 2;
    }
});

// Auto-format JSON on paste
inputSchema.addEventListener('paste', (e) => {
    setTimeout(() => {
        const value = inputSchema.value;
        if (isValidJSON(value)) {
            inputSchema.value = formatJSON(value);
        }
    }, 10);
});

// Initialize
console.log('Recipe Transformer Web App initialized');
console.log('Keyboard shortcuts:');
console.log('  - Ctrl/Cmd + Enter: Transform');
console.log('  - Tab: Insert spaces');

// Made with Bob
