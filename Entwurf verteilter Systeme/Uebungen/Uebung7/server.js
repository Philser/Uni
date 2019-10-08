// requires node.js
// http://codular.com/node-web-sockets

var http = require('http');
var server = http.createServer(function(request, response) {});

var PORT = 23023;

server.listen(PORT, function() {
    console.log((new Date()) + ' Server is listening on port ' + PORT);
});

var WebSocketServer = require('websocket').server;
wsServer = new WebSocketServer({
	httpServer: server
});

var clients = {};
var count = 0;
var id = 0;
var engine = null;
var controller = null;

wsServer.on('request', function(req){
    var newConnection = req.accept();
	clients[id] = newConnection;
	id = count + 1;
	console.log((new Date()) + ' Connection accepted [' + id + ']');
	
	// Receiving a message from the client
	newConnection.on('message', function(message) {
		var msgString = message.utf8Data;
		console.log("Received message");
		var jsonString = JSON.parse(msgString); //throws syntax error
		if(jsonString.messagetype == 'register') //check for undefined -- typeof != 'undefined'
		{			
			// maximum security!
			if(jsonString.data.type == 'engine'){
				engine = newConnection;
				console.log("Engine registered");
			}
			else if(jsonString.data.type == 'control'){
				controller = newConnection;
				console.log("Controller registered");
			}
		}
		else if(jsonString.messagetype == 'control')
		{
			console.log("Received control package");
			if(engine && typeof jsonString.data.speed != 'undefined')
			{
				console.log("Sending to engine");
				var speedVal = jsonString.data.speed; 
				var message = '{"data":{"speed":"' + speedVal + '"}}';
				engine.sendUTF(message);
			}
		}
		
	});

});
