const timeout = 1; // 1 ms
const callsPerSecond = 60;
const url = 'http://192.168.1.176:5000'




window.onload = () => {
    data_vis = document.getElementById('data');
    var socket = io(url)

    socket.on('connect', ()=> {
        socket.send('User has connected!');
    });

    socket.on('message', (msg)=> {
        console.log(msg);
        // update graph 
    });

    socket.send("feed me!");

    

};
