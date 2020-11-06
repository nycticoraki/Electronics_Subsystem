const timeout = 1; // 1 ms
const callsPerSecond = 60;
const url = document.location.origin;
const data_div = document.getElementById('data');
const selector_div = document.getElementById('selector');
const test_selector_div = document.getElementById('test_selector');
const terminal_selector_div = document.getElementById('terminal_selector');
const imu_test_enums = {
    'Temperature': 0,
    'Accelerometer': 1,
    'Magnetometer': 2,
    'Gyroscope': 3,
    'EulerAngle': 4,
    'Quaternion': 5,
    'LinearAcceleration': 6,
    'Gravity': 7            
};
const alt_test_enums = {
    'Pressure': 0,
    'Altitude': 1,
    'Temperature': 2
};

let selection = null;
let data_x = 0;
let data_y = 0;
let last_data_x = 0;
let last_data_y = 0;
let data_buffer_x = [];
let data_buffer_y = [];
var socket = null;


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

    // set up tests for default selection
    populateTests();

    

    var interval = setInterval(()=> {
        updateGraph();
    }, 1000/callsPerSecond);

};

// handle socket conditions



// disconnect socket if a connection is open
function disconnect() {
    data_buffer_x = [];
    data_buffer_y = [];
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
    var test = test_selector_div.options[test_selector_div.selectedIndex].value;
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
        //var test = test_selector_div.options[test_selector_div.selectedIndex].value;
        var test_id = test_selector_div.selectedIndex;
        //console.log(msg);
        
        // update graph 
        data_x = msg.time;
        if(selection == "imusensor") {
            switch(test_id) {                       // everything except Temperature and Quaternion returns a 3 element array
                case imu_test_enums.Accelerometer:
                    data_y = msg.data.Accelerometer;
                    break;
                case imu_test_enums.EulerAngle:     
                    data_y = msg.data.EulerAngle;
                    break;
                case imu_test_enums.Gravity:
                    data_y = msg.data.Gravity;
                    break;
                case imu_test_enums.Gyroscope:      
                    data_y = msg.data.Gyroscope;
                    break;
                case imu_test_enums.LinearAcceleration:
                    data_y = msg.data.LinearAcceleration;
                    break;
                case imu_test_enums.Magnetometer:
                    data_y = msg.data.Magnetometer;
                    break;
                case imu_test_enums.Quaternion:     // returns a 4 element tuple - change way data is displayed (limit graphs)
                    data_y = msg.data.Quaternion;
                    break;
                case imu_test_enums.Temperature:
                    data_y = msg.data.Temperature;
                    break;
                default:
                    alert('illegal value used: ' + test);
                    disconnect();
                    break;
            };
        }
        else if(selection == "altsensor") {
            switch(test_id) {                   // all 3 sensor values are scalars
                case alt_test_enums.Altitude:
                    data_y = msg.data.Altitude;
                    break;
                case alt_test_enums.Pressure:
                    data_y = msg.data.Pressure;
                    break;
                case alt_test_enums.Temperature:
                    data_y = msg.data.Temperature;
                    break;
                default:
                    alert('illegal value used: ' + test);
                    disconnect();
                    break;
            };
        }

        let new_message = document.createElement('div');
        new_message.innerHTML = "time: " + data_x + " data_y: " + data_y;
        terminal_selector_div.appendChild(new_message);
        terminal_selector_div.scrollTop = terminal_selector_div.scrollHeight;

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

function populateTests() {
    disconnect();
    var selection = selector_div.options[selector_div.selectedIndex].value;
    while(test_selector_div.firstChild) {
        test_selector_div.removeChild(test_selector_div.firstChild);
    }
    // Uses enums for each sensor value
    if (selection == "imusensor") {
        Object.getOwnPropertyNames(imu_test_enums).forEach((value, id)=> {
            let element = document.createElement("option");
            element.text = value;
            element.value = id;      // match each enum name with its value
            console.log("value: " + value + " id: " + id);
            test_selector_div.appendChild(element);
        });
    }
    else if (selection == "altsensor") {
        Object.getOwnPropertyNames(alt_test_enums).forEach((value, id)=> {
            let element = document.createElement("option");
            element.text = value;
            element.value = id;      // match each enum name with its value
            console.log("value: " + value + " id: " + id);
            test_selector_div.appendChild(element);
        });
    }
}

function changeTest() {
    disconnect();
    var test = test_selector_div.options[test_selector_div.selectedIndex].value;
}