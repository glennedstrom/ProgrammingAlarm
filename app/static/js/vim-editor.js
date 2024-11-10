// app/static/js/vim-editor.js

let vimEditor = null;

async function initVim() {
    try {
        const Module = await import('https://unpkg.com/@vimwasm/vim-wasm@0.0.8/vim-wasm.mjs');
        
        // Get the starter code
        const codeStorage = document.getElementById('code-storage');
        const initialContent = codeStorage.value;

        // Initialize Vim
        vimEditor = new Module.Vim('vim-editor', {
            clipboard: true,
            onQuit: () => {
                console.log('Vim quit requested');
            },
            onError: (error) => {
                console.error('Vim error:', error);
            },
            onWriteFile: (filename, contents) => {
                // Update hidden storage when file is saved
                document.getElementById('code-storage').value = contents;
            }
        });

        // Set initial content
        await vimEditor.loadContent(initialContent);
        
        // Focus the editor
        vimEditor.focus();

    } catch (error) {
        console.error('Error initializing Vim:', error);
        // Fallback to regular textarea if Vim fails to load
        const editorContainer = document.getElementById('editor-container');
        editorContainer.innerHTML = `
            <textarea id="fallback-editor" 
                      class="w-full h-full p-4 font-mono text-sm border rounded-md">${initialContent}</textarea>
        `;
    }
}

// Initialize Vim when the page loads
window.addEventListener('DOMContentLoaded', initVim);

// Update the submitSolution function to work with Vim
async function submitSolution() {
    let code;
    if (vimEditor) {
        // Get content from Vim
        code = await vimEditor.getContent();
    } else {
        // Fallback to regular textarea if Vim isn't available
        const fallbackEditor = document.getElementById('fallback-editor');
        code = fallbackEditor ? fallbackEditor.value : document.getElementById('code-storage').value;
    }
    
    const challengeId = window.location.pathname.split('/').pop();
    const resultsDiv = document.getElementById('test-results');
    
    resultsDiv.innerHTML = 'Running tests...';
    
    try {
        const response = await fetch('/api/verify-solution', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                challenge_id: challengeId,
                solution: code,
            }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            formatAndDisplayResults(data);
            if (data.all_passed) {
                stopAlarm();
                alert('Congratulations! All tests passed. Returning to main page...');
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            }
        } else {
            resultsDiv.innerHTML = `<div class="test-result-error">Error: ${data.error}</div>`;
        }
    } catch (error) {
        console.error('Error:', error);
        resultsDiv.innerHTML = '<div class="test-result-error">Error submitting solution</div>';
    }
}

// Update the resetCode function to work with Vim
async function resetCode() {
    if (!confirm('Are you sure you want to reset your code to the starter template?')) {
        return;
    }
    
    const starterCode = document.getElementById('code-storage').getAttribute('data-starter-code');
    
    if (vimEditor) {
        await vimEditor.loadContent(starterCode);
    } else {
        const fallbackEditor = document.getElementById('fallback-editor');
        if (fallbackEditor) {
            fallbackEditor.value = starterCode;
        }
    }
}
