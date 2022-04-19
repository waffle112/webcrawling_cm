//popup.js
/*
https://tinloof.com/blog/how-to-build-a-stopwatch-with-html-css-js-react-part-2


so most timers in code usually rely on datetime libraries 
date.getTime() -> 4/12/2022 - 14:29:00 
start = date.getTime()
end = date.getTime() 

actual_time = end - start
then modify actual time to be more presentable 

*/


//add eventlisteners for each button
let startTimer = document.getElementById("start");
let stopTimer = document.getElementById("stop");
let resetTimer = document.getElementById("reset");

//variables to keep track of time
var startTime;
var elapsedTime = 0;
var timerInterval; 

//sync stuff here i think
chrome.storage.local.get(['start'], function(result) {
  console.log('Value currently is ' + result.key);
  if(result.key == null){
	console.log('start of program'); 
	
  }else{
	console.log('resuming program');  
	startTime = result.key;

	chrome.storage.local.get(['elasped'], function(result) {
		elapsedTime = result.key; 
		
	});		
  }
});




function showButton(button){
	const currbutton = button === "PLAY" ? startTimer : stopTimer;
	const hidebutton = button === "PLAY" ? stopTimer : startTimer;
	
	currbutton.style.display = "block";
	hidebutton.style.display = "none"; 
}
	
	
function start(){
	startTime = Date.now() - elapsedTime; 
	timerInterval = setInterval(function printTime(){
		elapsedTime = Date.now() - startTime;
		setTime(timeToString(elapsedTime));

	}, 10);
	
	showButton("PAUSE"); 
	
	
}

function pause(){
	clearInterval(timerInterval);
	showButton("PLAY"); 
}

function resetTime(){
	clearInterval(timerInterval); 
	setTime("00:00:00");
	elapsedTime = 0;
	showButton("PLAY");

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
