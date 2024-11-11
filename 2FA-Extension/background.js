
var intercepting = false;
var collecting = false;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "startIntercept") {
        isIntercepting = true;
        chrome.webRequest.onCompleted.addListener(
            captureRequest,
            { urls: ["<all_urls>"] },
            ["responseHeaders", "extraHeaders"]
        );
    } else if (message.action === "pauseIntercept") {
        intercepting = false;
        chrome.webRequest.onCompleted.removeListener(captureRequest);
    } else if (message.action === "setIntercept") {
        const { selector, tabId, reqNum } = message;
        // excute content.js script
        chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: [ "content.js" ]
        }, () => {
            chrome.tabs.sendMessage(tabId, { action: "addClickIntercept", selector, reqNum});
        });

    }
});

function captureRequest(details){
    const responseHeaders = details.responseHeaders;
    const setCookies = responseHeaders.filter(header => header.name === "set-cookie" || header.name === "Set-Cookie").map(header => header.value);

    if (setCookies.length) {
        const request = {
            url: details.url,
            method: details.method,
            setCookies: setCookies
        }; 

        chrome.runtime.sendMessage({ action: "captureRequest", data: request });
    }
}

// Allows users to open the side panel by clicking on the action toolbar icon
chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch((error) => console.error(error));

chrome.tabs.onUpdated.addListener(async (tabId, info, tab) => {
  // Enables the side panel on google.com
  await chrome.sidePanel.setOptions({
    tabId,
    path: '/popup/popup.html',
    enabled: true
  });
});