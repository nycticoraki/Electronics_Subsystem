const timeout = 1; // 1 ms
const callsPerSecond = 60;
const url = 'http://192.168.1.176:5000'
const data_div = document.getElementById('data');;
const selector_div = document.getElementById('selector');;
let data_x = 0
let data_y = 0
let last_data_x = 0;
let last_data_y = 0;
let data_buffer_x = [];
let data_buffer_y = [];
var socket;


window.onload = () => {
    // graphing
    let layout = {
        title: '-------- Sensor Not Selected --------'
    };
    
    let plotData = [{
        x: [],
        y: [],
        mode: 'lines',
        line: {color: '#80CAF6'}
    }];
    Plotly.newPlot(data_div, plotData, layout);

    

    

    var interval = setInterval(()=> {
        updateGraph();
    }, 1000/callsPerSecond);

};

// handle socket conditions



// disconnect socket if a connection is open
function disconnect() {
    if(socket) {
        socket.send('unsubscribe');   // we will subscribe to this sensor
        socket.disconnect();
        socket = null;

        let layout = {
            title: `-------- Disconnected --------`
        };
        Plotly.relayout(data_div, layout);

    }
}

// start a new connection
function connect() {
    // see what sensor client is requesting
    var selection = selector_div.options[selector_div.selectedIndex].value;
    disconnect();
    socket = io(url + `/${selection}`);
    socket.send('subscribe');   // we will subscribe to this sensor
    let layout = {
        title: `${selection} plot`
    };
    Plotly.relayout(data_div, layout);

    // connect to server
    socket.on('connect', ()=> {
        socket.send('User has connected!');
    });

    // send message
    socket.on('message', (msg)=> {
        console.log(msg);
        // update graph 
        data_x = msg.time;
        data_y = msg.data;

        data_buffer_x.push(data_x);
        data_buffer_y.push(data_y);
    });

}



function updateGraph() {
    var update = {x: [data_buffer_x], y: [data_buffer_y]}
    last_data_x = data_x;
    last_data_y = data_y;
    var slidingWindow = {
        xaxis: {
            type: 'number',
            range: [data_x - 10, data_x + 5]
        }
    };
    Plotly.relayout(data_div, slidingWindow);
    Plotly.extendTraces(data_div, update, [0]);
    while(data_buffer_x.pop());
    while(data_buffer_y.pop());
}