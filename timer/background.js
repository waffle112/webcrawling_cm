// background.js
/*
var startTime;
var elapsedTime;
var timerInterval; 

chrome.runtime.onInstalled.addListener(() => {
	chrome.storage.sync.set({ startTime });
	chrome.storage.sync.set({ elapsedTime });
	chrome.storage.sync.set({ timerInterval });
});

*/
/*
var website = "N/A";


chrome.tabs.onActivated.addListener(function(activeInfo) {
    chrome.tabs.get(activeInfo.tabId, function (tab) {
        mySuperCallback(tab.url);
    });
});

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, updatedTab) {
    chrome.tabs.query({'active': true}, function (activeTabs) {
        var activeTab = activeTabs[0];

        if (activeTab == updatedTab) {
            mySuperCallback(activeTab.url);
        }
    });
});

function mySuperCallback(newUrl) {
    website = newUrl;
	console.log("website set to " + website);
	chrome.storage.local.set({website});
}
	*/
 
 
 
/*
chrome.storage.onChanged.addListener(function (changes, namespace) {
  for (let [key, { oldValue, newValue }] of Object.entries(changes)) {
    
	console.log(
      `Storage key "${key}" in namespace "${namespace}" changed.`,
      `Old value was "${oldValue}", new value is "${newValue}".`
    );

  }
  
});
*/

