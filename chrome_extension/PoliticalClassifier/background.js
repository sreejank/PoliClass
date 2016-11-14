chrome.extension.onMessage.addListener(onRequest);
var pressed = false;
chrome.browserAction.onClicked.addListener(function (tab) {
    console.log("Icon pressed");
    if(pressed == false){
        chrome.tabs.executeScript(tab.id, {file:'functions.js'});
        chrome.tabs.executeScript(tab.id, {file:'check.js'}, function () {
            chrome.tabs.sendMessage(tab.id, {options:getOptions(), action:"initial"});
        });
        pressed = true;
    }
    else{chrome.tabs.reload();}
    
});

chrome.runtime.onInstalled.addListener(function(details){
    if(details.reason == "install"){
        chrome.tabs.create({url: "options.html?newinstall=yes"});
    }
    else if(details.reason == "update"){
        var thisVersion = chrome.runtime.getManifest().version;
        console.log("Updated from " + details.previousVersion + " to " + thisVersion + "!");
    }
});