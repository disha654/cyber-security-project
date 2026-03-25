document.addEventListener('DOMContentLoaded', () => {
  const navItems = document.querySelectorAll('nav li');
  const tabContents = document.querySelectorAll('.tab-content');
  const totalBlockedCount = document.getElementById('totalBlockedCount');
  const uniqueDomainsCount = document.getElementById('uniqueDomainsCount');
  const trackersTableBody = document.querySelector('#trackersTable tbody');
  const whitelistInput = document.getElementById('whitelistInput');
  const addWhitelistBtn = document.getElementById('addWhitelistBtn');
  const whitelistItems = document.getElementById('whitelistItems');
  const resetStatsBtn = document.getElementById('resetStatsBtn');

  // Tab switching logic
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const tabId = item.getAttribute('data-tab');
      
      navItems.forEach(nav => nav.classList.remove('active'));
      tabContents.forEach(content => content.classList.remove('active'));
      
      item.classList.add('active');
      document.getElementById(tabId).classList.add('active');
      document.querySelector('.main-header h1').textContent = item.textContent + ' Overview';
    });
  });

  // Load analytics data
  function loadStats() {
    chrome.storage.local.get(['totalBlocked', 'blockedDomains', 'whitelist'], (result) => {
      const total = result.totalBlocked || 0;
      const domains = result.blockedDomains || {};
      const whitelist = result.whitelist || [];

      totalBlockedCount.textContent = total;
      uniqueDomainsCount.textContent = Object.keys(domains).length;

      // Populate table
      trackersTableBody.innerHTML = '';
      const sortedDomains = Object.entries(domains).sort((a, b) => b[1] - a[1]);
      
      sortedDomains.forEach(([domain, count]) => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${domain}</td>
          <td>${count}</td>
        `;
        trackersTableBody.appendChild(row);
      });

      // Populate whitelist
      whitelistItems.innerHTML = '';
      whitelist.forEach(domain => {
        const li = document.createElement('li');
        li.className = 'list-item';
        li.innerHTML = `
          <span>${domain}</span>
          <button class="btn danger remove-whitelist" data-domain="${domain}">Remove</button>
        `;
        whitelistItems.appendChild(li);
      });
    });
  }

  // Add to whitelist
  addWhitelistBtn.addEventListener('click', () => {
    const domain = whitelistInput.value.trim().toLowerCase();
    if (domain) {
      chrome.storage.local.get(['whitelist'], (result) => {
        const whitelist = result.whitelist || [];
        if (!whitelist.includes(domain)) {
          whitelist.push(domain);
          chrome.storage.local.set({ whitelist }, () => {
            whitelistInput.value = '';
            loadStats();
            updateDynamicRules();
          });
        }
      });
    }
  });

  // Remove from whitelist
  whitelistItems.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-whitelist')) {
      const domain = e.target.getAttribute('data-domain');
      chrome.storage.local.get(['whitelist'], (result) => {
        const whitelist = (result.whitelist || []).filter(d => d !== domain);
        chrome.storage.local.set({ whitelist }, () => {
          loadStats();
          updateDynamicRules();
        });
      });
    }
  });

  // Reset stats
  resetStatsBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to reset all tracking data?')) {
      chrome.storage.local.set({ totalBlocked: 0, blockedDomains: {} }, () => {
        loadStats();
      });
    }
  });

  // Function to sync dynamic rules with whitelist
  async function updateDynamicRules() {
    chrome.storage.local.get(['whitelist'], async (result) => {
      const whitelist = result.whitelist || [];
      
      // Get existing dynamic rules
      const oldRules = await chrome.declarativeNetRequest.getDynamicRules();
      const oldRuleIds = oldRules.map(rule => rule.id);

      // Create allow rules for whitelist (ID range 1000+)
      const newRules = whitelist.map((domain, index) => ({
        id: 1000 + index,
        priority: 2, // Higher than block rules
        action: { type: 'allow' },
        condition: { urlFilter: domain, resourceTypes: ['script', 'xmlhttprequest', 'image'] }
      }));

      await chrome.declarativeNetRequest.updateDynamicRules({
        removeRuleIds: oldRuleIds,
        addRules: newRules
      });
    });
  }

  loadStats();
});
