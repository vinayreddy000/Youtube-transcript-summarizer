chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.message === "getURL") {
        getCurrentTabUrl(sendResponse);
        return true;
    }
});

function getCurrentTabUrl(callback) {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        var tabUrl = tabs[0].url;
        callback(tabUrl);
    });
}