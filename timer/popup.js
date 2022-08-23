//popup.js
/*
https://tinloof.com/blog/how-to-build-a-stopwatch-with-html-css-js-react-part-2


so most timers in code usually rely on datetime libraries 
date.getTime() -> 4/12/2022 - 14:29:00 
start = date.getTime()
end = date.getTime() 

actual_time = end - start
then modify actual time to be more presentable 

make 3rd button that saves to server (flask server)
make buttons bigger
modify timer/pop up to be bigger and have ample space around timer text 


expected logistic
	open website
	open popup/timer 
	start timer
	read website
	open popup/timer 
	stop timer 
	save time to server (passes in url link)
	
	
	in flask server 
		webcrawl url link
		save text as parsed dictionary 
		save time 
		save user 
		either
			save data as CSV (excel sheet)
			utilize software to visualize data for use (matplotlib for example)

*/


//add eventlisteners for each button
let startTimer = document.getElementById("start");
let stopTimer = document.getElementById("stop");
let resetTimer = document.getElementById("reset");
let enterusername = document.getElementById("entername");
let saveTime = document.getElementById("save");
let showTimes = document.getElementById("times");
let clearTime = document.getElementById("clear");
let wordcount = document.getElementById("wordcounts");

let avewordcnt = document.getElementById('avewordcnt'); 
let biggestword = document.getElementById('biggestword'); 
let commonword = document.getElementById('commonword'); 
let wordoccurence = document.getElementById('wordoccurence'); 

//variables to keep track of time
var startTime;
var elapsedTime = 0;
var timerInterval; 
var cont = false; 


var username; //modify html to include a text box for username 
var websiteURL = "N/A"; //modify html to indicate current website link 
//var websiteHTML = document.getElementById("websiteID");


//sync stuff here i think
chrome.storage.local.get('startTime', ({startTime}) =>{
	self.startTime = startTime;
	console.log('checking for past startTime');
});

chrome.storage.local.get('elapsedTime', ({elapsedTime}) =>{
	self.elapsedTime = elapsedTime;
	console.log('checking for past elapsedTime');
});

 chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {

    var activeTab = tabs[0];
    self.websiteURL = activeTab.url; 
	console.log('website set to' + self.websiteURL);
	document.getElementById("websiteID").innerHTML = "Website: " + self.websiteURL;
 });


chrome.storage.local.get('username', ({username}) =>{
	self.username = username;
	console.log('checking for past username');
	if (username != 'undefined'){
		document.getElementById("saveusername").value = username;
		showTime();
	}

});



chrome.storage.local.get('cont', ({cont}) =>{
	if (cont == true){
		self.timerInterval = setInterval(function printTime(){
			elapsedTime = Date.now() - startTime;
			chrome.storage.local.set({elapsedTime});
			setTime(timeToString(elapsedTime));

		}, 10);
		self.cont = true; 
		chrome.storage.local.set({cont});
		showButton("PAUSE"); 
		console.log("timer active");
	}else{
		self.cont = false; 
		chrome.storage.local.set({cont});
		clearInterval(self.timerInterval);
		setTime(timeToString(elapsedTime));
		showButton("PLAY"); 
		
	}
	
});

function testFlask(){
	// fetch json - 'http://127.0.0.1:5000/test'
	fetch('http://127.0.0.1:5000/test',{
		method: "GET",
		//mode: 'no-cors' //remove no-cors if app is successcully published 
      }).then((response) => {
        return response.json();
      }).then((text) => {
        console.log('GET response text:');
        console.log(text); // Print the greeting as text
        console.log(JSON.stringify(text));
        console.log('');
      }).catch(err => {
		console.log("error caught");
		console.log(err);
	  });
	
}
function showTime(){
	//send the username, the websiteurl, and the time to server to save 
	console.log('sending ' + username + ', ' + websiteURL);
	fetch('http://127.0.0.1:5000/showTime',{
		
		method: "POST",
			
		body: JSON.stringify({
			"username": self.username,
			"website": self.websiteURL
		}),
		headers: new Headers({
			"Content-Type": "application/json"
		})
		
	}).then((response) => {
        return response.json();
    }).then((text) => {
        console.log('GET response text:');
        console.log(text); // Print the greeting as text
		var tt = text["time"];
		var temp = [];
		showTimes.innerHTML = "";
		for(var i = 0; i < tt.length; i++){
			//timeToString(tt[i]);
			//create a list of times in html  
			var el = document.createElement('li');
			el.appendChild(document.createTextNode(timeToString(tt[i])));
			showTimes.appendChild(el);
			
		}
		
        console.log(JSON.stringify(temp));
        console.log('');
		
		var webstats = text["webstats"]; 
		console.log(webstats); 
		if(webstats[0].length >= 1){
			
			
			//<label id = "wordoccurence"></label>
			avewordcnt.innerHTML =  "Average Word Count: " + webstats[1];
			biggestword.innerHTML = "biggest word:       " + webstats[2];
			commonword.innerHTML =  "Most common word:   " + webstats[3];
			wordoccurence.innerHTML="with occurence:     " + webstats[4];
			wordcounts.innerHTML = ""; 
			for (var i = 0; i < 10; i++){
				var el = document.createElement('li');
				el.appendChild(document.createTextNode(webstats[0][i]));
				wordcounts.append(el); 
			}
		}
    }).catch(err => {
		console.log("error caught");
		console.log(err);
	});
}

function saveTimefunc(){
	//send the username, the websiteurl, and the time to server to save 
	console.log('sending ' + username + ', ' + websiteURL + ' ' + elapsedTime);	
	fetch('http://127.0.0.1:5000/saveTime',{
		
		method: "POST",
			
		body: JSON.stringify({
			"username": self.username,
			"time": self.elapsedTime,
			"website": self.websiteURL
		}),
		headers: new Headers({
			"Content-Type": "application/json"
		})
		
	}).catch(err => {
		console.log("error caught");
		console.log(err);
	});
	showTime();
		  
}
function delTimefunc(){
	//send the username, the websiteurl, and the time to server to save 
	console.log('sending ' + username + ', ' + websiteURL + ' ' + elapsedTime);	
	fetch('http://127.0.0.1:5000/delTime',{
		
		method: "POST",
			
		body: JSON.stringify({
			"username": self.username,
			"website": self.websiteURL
		}),
		headers: new Headers({
			"Content-Type": "application/json"
		})
		
	}).catch(err => {
		console.log("error caught");
		console.log(err);
	});
	showTime();
		  
}
function getUsername(){
	self.username = document.getElementById('saveusername').value;
	//save username locally 
	chrome.storage.local.set({username});
	document.getElementById("saveusername").placeholder = username;
	document.getElementById("test").innerHTML = "Saved as " + username;
	showTime();
	
}


function showButton(button){
	const currbutton = button === "PLAY" ? startTimer : stopTimer;
	const hidebutton = button === "PLAY" ? stopTimer : startTimer;
	
	currbutton.style.display = "block";
	hidebutton.style.display = "none"; 
}
	
	
function start(){
	startTime = Date.now() - elapsedTime; 
	chrome.storage.local.set({startTime});
	
	self.timerInterval = setInterval(function printTime(){
		elapsedTime = Date.now() - startTime;
		chrome.storage.local.set({elapsedTime});
		setTime(timeToString(elapsedTime));

	}, 10);
	self.cont = true; 
	chrome.storage.local.set({cont});
	
	showButton("PAUSE"); 
	
	testFlask();
	//saveTime();
}

function pause(){
	clearInterval(self.timerInterval);
	showButton("PLAY"); 
	
	self.cont = false;
	chrome.storage.local.set({cont});
}

function resetTime(){
	clearInterval(self.timerInterval); 
	setTime("00:00:00");
	elapsedTime = 0;
	chrome.storage.local.set({elapsedTime});
	showButton("PLAY");
	
	self.cont = false;
	chrome.storage.local.set({cont});
	
}

function setTime(txt){
	document.getElementById("timeDisplay").innerHTML = txt;
};




function timeToString(time) {
  let diffInHrs = time / 3600000;
  let hh = Math.floor(diffInHrs);

  let diffInMin = (diffInHrs - hh) * 60;
  let mm = Math.floor(diffInMin);

  let diffInSec = (diffInMin - mm) * 60;
  let ss = Math.floor(diffInSec);

  let diffInMs = (diffInSec - ss) * 100;
  let ms = Math.floor(diffInMs);

  let formattedMM = mm.toString().padStart(2, "0");
  let formattedSS = ss.toString().padStart(2, "0");
  let formattedMS = ms.toString().padStart(2, "0");

  return `${formattedMM}:${formattedSS}:${formattedMS}`;
}

startTimer.addEventListener("click", start);
stopTimer.addEventListener("click", pause);
resetTimer.addEventListener("click", resetTime);
enterusername.addEventListener("click", getUsername);
saveTime.addEventListener("click", saveTimefunc);
clearTime.addEventListener("click", delTimefunc);