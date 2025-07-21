document.addEventListener('DOMContentLoaded', function() {
  // Custom copy handler for terminal examples
  function setupCopyHandler() {
    // Listen for copy events on all sl-copy-button elements
    document.addEventListener('sl-copy', function(event) {
      const copyButton = event.target;
      
      // Get the target element that the copy button is copying from
      const fromAttr = copyButton.getAttribute('from');
      if (!fromAttr) return;
      
      const targetElement = document.getElementById(fromAttr);
      if (!targetElement) return;
      
      // Get the text content
      let textToCopy = targetElement.textContent || targetElement.innerText || '';
      
      // Check if this looks like a terminal/shell code block
      // Look for lines that start with $ followed by a space
      const lines = textToCopy.split('\n');
      const modifiedLines = lines.map(line => {
        // If line starts with $ followed by whitespace, strip it
        if (/^\$\s/.test(line)) {
          return line.replace(/^\$\s+/, '');
        }
        return line;
      });
      
      // Check if any lines were modified (meaning this was a terminal example)
      const wasModified = lines.some((line, index) => line !== modifiedLines[index]);
      
      if (wasModified) {
        // Prevent the default copy behavior
        event.preventDefault();
        
        // Copy the modified text to clipboard
        const modifiedText = modifiedLines.join('\n');
        
        if (navigator.clipboard && navigator.clipboard.writeText) {
          // Modern browsers
          navigator.clipboard.writeText(modifiedText).then(() => {
            // Trigger success feedback if available
            if (copyButton.success) {
              copyButton.success();
            }
          }).catch(err => {
            console.error('Failed to copy text: ', err);
            // Fallback to default behavior
            fallbackCopy(modifiedText);
          });
        } else {
          // Fallback for older browsers
          fallbackCopy(modifiedText);
        }
      }
    });
  }
  
  // Fallback copy method for older browsers
  function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-999999px';
    textarea.style.top = '-999999px';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    
    try {
      document.execCommand('copy');
    } catch (err) {
      console.error('Fallback copy failed: ', err);
    }
    
    document.body.removeChild(textarea);
  }
  
  // Initialize the copy handler
  setupCopyHandler();
}); 