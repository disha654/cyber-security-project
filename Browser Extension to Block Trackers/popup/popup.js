document.addEventListener('DOMContentLoaded', async () => {
  const extensionToggle = document.getElementById('extensionToggle');
  const currentTabCount = document.getElementById('currentTabCount');
  const totalCount = document.getElementById('totalCount');
  const openDashboard = document.getElementById('openDashboard');

  // Get current tab ID
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Update popup UI from storage
  chrome.storage.local.get(['totalBlocked', 'isExtensionEnabled'], (result) => {
    totalCount.textContent = result.totalBlocked || 0;
    extensionToggle.checked = result.isExtensionEnabled !== false;
  });

  // Get current tab stats from background
  chrome.runtime.sendMessage({ action: 'getTabStats', tabId: tab.id }, (response) => {
    if (response && response.count !== undefined) {
      currentTabCount.textContent = response.count;
    }
  });

  // Handle toggle change
  extensionToggle.addEventListener('change', () => {
    const enabled = extensionToggle.checked;
    chrome.runtime.sendMessage({ action: 'toggleExtension', enabled: enabled });
  });

  // Open Dashboard
  openDashboard.addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });
});
