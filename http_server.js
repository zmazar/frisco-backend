var http = require('http');

// Define listening port
const PORT = 8080

// Define a function to handle HTTP requests
function handleHttpRequest(request, response) {
    switch(request.method) {
        case "GET":
            if(request.url === "/favicon.ico") {
                response.writeHead(404, {'Content-Type': 'text/html'});
                response.write('');
                response.end();
            }
            else if(request.url === "/columbia") {
                // Handle requests for Colubmia's beer list
                response.writeHead(200, {'Content-Type': 'application/json'});
                response.end('Requesting Columbia\'s beer list');
            }
            else if(request.url === "/crofton") {
                // Handle requests for Crofton's beer list
                response.writeHead(200, {'Content-Type': 'application/json'});
                response.end('Requesting Crofton\'s beer list');
            }
            else {
                // No idea what they're requesting, so lets just fail them
                response.writeHead(404, {'Content-Type': 'text/html'});
                response.end('What the hell are you trying to request?');
            }
            break;
        default:
            // We only handle GET requests, respond with failure
            response.writeHead(404, {'Content-Type': 'text/html'});
            response.end('We only handle GET requests dummy');
    }
}

// Create server
var server = http.createServer(handleHttpRequest);

// Lets start up the server
server.listen(PORT, function() {
    // Callback triggered when the server is succesfully listening
    console.log("Server listening on: http://localhost:%s", PORT);
});
