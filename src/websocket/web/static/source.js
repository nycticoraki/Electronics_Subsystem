const timeout = 1; // 1 ms
const callsPerSecond = 60;
const url = 'http://192.168.1.176:5000'
let data_x = 0
let data_y = 0
let last_data_x = 0;
let last_data_y = 0;
let data_buffer_x = [];
let data_buffer_y = [];


window.onload = () => {
    data_vis = document.getElementById('data');
    var socket = io(url)

    // graphing
    let layout = {
        title: 'Range Finder Time versus Distance'
    };
    
    let plotData = [{
        x: [],
        y: [],
        mode: 'lines',
        line: {color: '#80CAF6'}
    }];
    Plotly.newPlot(data_vis, plotData, layout);

    socket.on('connect', ()=> {
        socket.send('User has connected!');
    });

    socket.on('message', (msg)=> {
        console.log(msg);
        // update graph 
        data_x = msg.time;
        data_y = msg.data;

        data_buffer_x.push(data_x);
        data_buffer_y.push(data_y);
    });

    socket.send("feed me!");

    var interval = setInterval(()=> {
        updateGraph();
    }, 1000/callsPerSecond);

};


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
    Plotly.relayout(data_vis, slidingWindow);
    Plotly.extendTraces(data_vis, update, [0]);
    while(data_buffer_x.pop());
    while(data_buffer_y.pop());
}