var link;
var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
var eventer = window[eventMethod];
var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";
// Listen to message from child IFrame window
eventer(messageEvent, function (e) {
   var string = JSON.stringify(e.data);
   // check to see if the string contains the session id 
   if (string.match(/[0-9]{3}[-][0-9]{3}[-][0-9]{3}/g)) {
      link = string.substring(1, string.length - 1);
      document.getElementById("inviteLink").value = link;
   }
}, false);

var copyText = document.getElementById('copyLink');
copyText.addEventListener('click', function () {
   var copiedLink = document.getElementById('inviteLink');
   // select the contents
   inviteLink.select();
	   
   document.execCommand('copy');
}, false);

