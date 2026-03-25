# Tracker Blocker & Privacy Shield

A modern, privacy-focused browser extension to block known tracking scripts and provide detailed analytics.

## Features
- **Block Known Trackers**: Pre-configured list of common tracking domains (Google Analytics, Facebook, DoubleClick, etc.).
- **Real-time Badge Counter**: Shows the number of trackers blocked on the current page.
- **Analytics Dashboard**: View total blocked requests and a breakdown by domain.
- **Whitelist Support**: Easily allow trackers for specific domains if needed.
- **Privacy First**: All data is stored locally in your browser.

## How to Install (Local/Developer Mode)

### For Chrome/Edge/Brave:
1. Open Chrome and go to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in the top right corner).
3. Click on **Load unpacked**.
4. Select the project folder: `D:\Disha\Cyber Security Projects\p1\Browser Extension to Block Trackers`.
5. The extension icon should appear in your toolbar.

### For Firefox:
1. Open Firefox and go to `about:debugging#/runtime/this-firefox`.
2. Click on **Load Temporary Add-on...**.
3. Select the `manifest.json` file in the project folder.

## How to Use
- **Popup**: Click the extension icon to see stats for the current page and toggle the blocker on/off.
- **Dashboard**: Click "View Dashboard" in the popup or right-click the extension and select "Options" to see your full blocking history and manage your whitelist.

## File Structure
- `manifest.json`: Extension configuration (Manifest V3).
- `background.js`: Service worker for tracking and communication.
- `rules.json`: Static blocking rules.
- `popup/`: UI for the extension's popup.
- `dashboard/`: Analytics and Whitelist management page.
- `icons/`: (Place your icons here: `icon16.png`, `icon48.png`, `icon128.png`).

## Commands to Run
Since this is a browser extension, there is no "build" command required if you are loading it as an unpacked extension. 
Just follow the "How to Install" steps above!
