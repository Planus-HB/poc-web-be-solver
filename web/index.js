const express = require('express');
const WebSocket = require('ws');

const app = express();
const port = 3000;

let ws;

function createWebSocketClient() {
  ws = new WebSocket('ws://localhost:8765');

  ws.on('open', function open() {
    console.log('Connected to WebSocket server');
  });

  ws.on('error', function error(err) {
    console.error('WebSocket error:', err.message);
    setTimeout(createWebSocketClient, 2000);
  });
}

createWebSocketClient();

app.use(express.json());
app.post('/send-message', (req, res) => {
  const { message } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }

  if (ws.readyState !== WebSocket.OPEN) {
    return res.status(500).json({ error: 'WebSocket connection not open' });
  }

  ws.send(JSON.stringify({ message }));

  res.json({ success: true, message: 'Message sent successfully' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
