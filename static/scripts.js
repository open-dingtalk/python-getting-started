function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
			return decodeURIComponent(pair[1]);
		}
    }
    return(false);
}

function sendTextMessage() {
	$.ajax({
		type: "POST",
		url: "/api/sendText",
		data: JSON.stringify({
			txt: $("#textMessage").val(),
			openConversationId:getQueryVariable("openConversationId")
		}),
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		success: function(response) {
			//alert("success:" + JSON.stringify(response));
		},
		error: function(err) {
			// alert("error:" + JSON.stringify(err));
		}
	});
}


function sendCardMessage() {
	$.ajax({
		type: "POST",
		url: "/api/sendMessageCard",
		data: JSON.stringify({
			openConversationId:getQueryVariable("openConversationId")
		}),
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		success: function(response) {
			//alert("success:" + JSON.stringify(response));
		},
		error: function(err) {
			// alert("error:" + JSON.stringify(err));
		}
	});
}


function sendTopMessage() {
	$.ajax({
		type: "POST",
		url: "/api/sendTopCard",
		data: JSON.stringify({
			openConversationId:getQueryVariable("openConversationId")
		}),
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		success: function(response) {
			//alert("success:" + JSON.stringify(response));
		},
		error: function(err) {
			// alert("error:" + JSON.stringify(err));
		}
	});
}