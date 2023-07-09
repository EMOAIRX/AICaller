const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });
const wss2 = new WebSocket.Server({ port: 8081 });

//数据转发服务器

console.log('server is running on port 8080 and 8081');

wss.on('connection', ws => {
  ws.on('message', message => {
    console.log(`Received message => ${message}`);
    
    wss.clients.forEach(client => {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(message);
        console.log('message had been sent to all clients')
      }
    });
  });
});

wss2.on('connection', ws => {
  ws.on('message', message => {
    console.log(`Received message => ${message}`);
    
    wss2.clients.forEach(client => {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(message);
        console.log('message had been sent to all clients')
      }
    });
  });
});
