const timeout = 1; // 1 ms
const callsPerSecond = 100;
const url_getDistance = document.location.origin + "/getDistance";
const url_getID = document.location.origin + "/getID";
var data_vis;
var obj_data;
var ID = null;
var STARTING_TIME;
var plotData;
var data_x;
var data_y;
var layout;
var last_data_x;
var last_data_y;

class DataBundle {
    constructor(time, distance) {
        this.time = time;
        this.distance = distance;
    }
}

window.onload = () => {
    data_vis = document.getElementById('data');
    //let cnt = 0;
    layout = {
        title: 'Range Finder Time versus Distance'
    };
    data_x = 0
    data_y = 0
    last_data_x = 0;
    last_data_y = 0;
    plotData = [{
        x: [],
        y: [],
        mode: 'lines',
        line: {color: '#80CAF6'}
    }];
    Plotly.newPlot(data_vis, plotData, layout);

    // request an id from the server
    requestID();

    if(ID == null)
        console.log("An Error Has Occurred While Getting an ID...");

    var interval = setInterval(()=> {
        requestSensorData();
        updateGraph();
    }, 1000/callsPerSecond);

};

async function requestID() {
    fetch(url_getID)
        .then(res => res.json())
        .then(data => {
            ID = data.ID;
            START_TIME = data.START_TIME;
            console.log(`ID: ${ID}, TIME: ${START_TIME}`);
        })
        .catch(err => {
            console.log(`Error: ${err}`);
        });
}

async function requestSensorData() {
    if(ID == null) {
        console.log("An Error Has Occurred While Getting an ID...");
        return;
    }
    pollForDistance();
}


async function pollForDistance() {
    fetch(url_getDistance)
        .then(res => res.json())
        .then(data => {
            //data_vis.textContent = "(" + (data.time) + ", "+ data.distance + ")";
            data_x = data.time;
            data_y = data.distance
        })
        .catch(err => {
            console.log(`Error: ${err}`);
        });
}

function updateGraph() {
    var update = {x: [[data_x]], y: [[(data_y - last_data_y) / (data_x - last_data_x)]]}
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
}

