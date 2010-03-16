function processGetPost()
	{
	var myajax=ajaxpack.ajaxobj
	var myfiletype=ajaxpack.filetype
	if (myajax.readyState == 4)
		{ //if request of file completed
		if (myajax.status==200 || window.location.href.indexOf("http")==-1)
			{ //if request was successful or running script locally
			if (myfiletype=="txt")
			alert(myajax.responseText)
			else
			alert(myajax.responseXML)
			}
		}
	}


function connect()
{
  var nick = document.getElementById('nickname').value;
  Orbited.connect(chat_event, nick, "/chat", "0");
  ajaxpack.getAjaxRequest("/chat/join/" + nick + "/", "", processGetPost, "txt");
}


chat_event = function(data) {
  var chat_box = document.getElementById('box');
  var div = window.parent.document.createElement('div');
  div.className = "event";
  div.innerHTML = data;
  chat_box.appendChild(div);
  chat_box.scrollTop = chat_box.scrollHeight;
}

function send_msg() {
  var msg = document.getElementById('chat').value;
  var nick = document.getElementById('nickname').value;
  ajaxpack.getAjaxRequest("/chat/send/" + nick + "/" + msg + "/", "", processGetPost, "txt");
}
