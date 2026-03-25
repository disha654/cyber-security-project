// background.js

let blockedCount = {}; // tabId -> count

// Initialize storage
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(['totalBlocked', 'blockedDomains', 'isExtensionEnabled'], (result) => {
    if (result.totalBlocked === undefined) {
      chrome.storage.local.set({ 
        totalBlocked: 0, 
        blockedDomains: {}, 
        isExtensionEnabled: true,
        whitelist: []
      });
    }
  });
});

// Listener for rule matches (Unpacked extension only)
chrome.declarativeNetRequest.onRuleMatchedDebug.addListener((info) => {
  updateStats(info.tabId, info.request.url);
});

function updateStats(tabId, url) {
  if (tabId === -1) return;

  const domain = new URL(url).hostname;
  
  // Update tab-specific count
  blockedCount[tabId] = (blockedCount[tabId] || 0) + 1;
  chrome.action.setBadgeText({ tabId: tabId, text: blockedCount[tabId].toString() });
  chrome.action.setBadgeBackgroundColor({ tabId: tabId, color: '#FF4444' });

  // Update persistent stats
  chrome.storage.local.get(['totalBlocked', 'blockedDomains'], (result) => {
    let total = (result.totalBlocked || 0) + 1;
    let domains = result.blockedDomains || {};
    domains[domain] = (domains[domain] || 0) + 1;
    
    chrome.storage.local.set({ totalBlocked: total, blockedDomains: domains });
  });
}

// Reset tab count on refresh
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'loading') {
    blockedCount[tabId] = 0;
    chrome.action.setBadgeText({ tabId: tabId, text: '' });
  }
});

// Handle messages from popup/dashboard
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getTabStats') {
    sendResponse({ count: blockedCount[request.tabId] || 0 });
  } else if (request.action === 'toggleExtension') {
    updateExtensionState(request.enabled);
  }
  return true;
});

async function updateExtensionState(enabled) {
  const rules = await chrome.declarativeNetRequest.getEnabledRulesets();
  if (enabled) {
    chrome.declarativeNetRequest.updateEnabledRulesets({ enableRulesetIds: ['ruleset_1'] });
  } else {
    chrome.declarativeNetRequest.updateEnabledRulesets({ disableRulesetIds: ['ruleset_1'] });
  }
  chrome.storage.local.set({ isExtensionEnabled: enabled });
}
