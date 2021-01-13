var socket = io();
socket.on('connect', function() {
    console.log('Connected to websocket :)')
});

socket.on('data updated', data => {
    //FillMap();
    alert("Data was updated bitch!");
});