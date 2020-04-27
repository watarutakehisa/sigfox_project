let date = [],
    temperature = [],
    humidity = [],
    pressure = [],
    waterlevel = [],//add
    compressed, tmp;

function drawChart(){
    setData(obj).then(function(){
        plotCharts();
    });
};

async function setData(obj){
    for(let i=0; i<obj.length; i++){
        // date.push(new Date(obj.data[i].time*1000));  // set as Date object
        date.push(new Date(obj[i][1]));  // if use API v2
        //compressed = obj.data[i].data;

        // TEMPERATURE
        //tmp = "0x" + compressed.substring(0, 8);
        temperature.push({
            t: date[i],  // either x: or t:
            y: obj[i][2]
        });
        // HUMIDITY
        //tmp = "0x" + compressed.substring(8, 16);
        humidity.push({
            t: date[i],
            y: obj[i][3]
        });
        // PRESSURE
        pressure.push({
            t: date[i],
            y: obj[i][4]
        });
        //add
        // WATERLEVEL
        waterlevel.push({
            t: date[i],
            y: obj[i][5]
        });
    }
    return 0;
}

function plotCharts(){
    var tct = document.getElementById("tChart");
    window.tChart = new Chart(tct, tconfig);
    var hct = document.getElementById("hChart");
    window.hChart = new Chart(hct, hconfig);
    var pct = document.getElementById("pChart");
    window.pChart = new Chart(pct, pconfig);
    //add
    var wct = document.getElementById("wChart");
    window.wChart = new Chart(wct, wconfig);
}

const now = new Date();
const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
let showLength = new Date(now.getFullYear(), now.getMonth(), now.getDate() -1);

// options applied for all 4 charts
let options = {
    legend: {
        labels: {
            fontSize: 18,
        },
    },
    layout: {
        padding: {
            left: 100,
            right: 100
        }
    },
    scales: {
        xAxes: [{
            distribution: 'linear',  // either 'linear' or 'series'
            ticks: {
                source: 'auto',  // either 'auto' or 'data'
                fontSize: 18
            },
            time: {
                min: showLength,
                unit: 'day',
                displayFormats: {
                    day: 'MM-DD',
                },
                tooltipFormat: 'HH:mm YYYY-MM-DD',
            },
            type: 'time',
        }],
        yAxes: [{
            ticks: {
                fontSize: 18
            },
        }]
    },
    tooltips: {
        titleFontSize: 16,
        titleFontStyle: 'normal',
        bodyFontSize: 18,
        bodyFontStyle: 'bold',
        callbacks: {
            label: function(tooltipItem, data) {
                var label = data.datasets[tooltipItem.datasetIndex].label || '';
                if(label){
                    label += ': ';
                }
                label += Math.round(tooltipItem.yLabel * 100) / 100;
                return label;
            }
        }
    }
};

// config for Temperature chart
var tconfig = {
    type: 'line',
    data: {
        labels: date,
        datasets: [{
            label: '気温 [*C]',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: temperature,
            fill: false,
            lineTension: 0,
        }]
    },
    options: options
};

// config for Humidity Chart
var hconfig = {
    type: 'line',
    data: {
        labels: date,
        datasets: [{
            label: '湿度 [%]',
            backgroundColor: 'rgb(99, 132, 255)',
            borderColor: 'rgb(99, 132, 255)',
            data: humidity,
            fill: false,
            lineTension: 0,
        }]
    },
    options: options
};

// config for Pressure Chart
var pconfig = {
    type: 'line',
    data: {
        labels: date,
        datasets: [{
            label: '気圧 [hPa]',
            backgroundColor: 'rgb(132, 99, 255)',
            borderColor: 'rgb(132, 99, 255)',
            data: pressure,
            fill: false,
            lineTension: 0,
        }]
    },
    options: options
};

//add
// config for waterlevel Chart
var wconfig = {
    type: 'line',
    data: {
        labels: date,
        datasets: [{
            label: '水位 [m]',
            backgroundColor: 'rgb(255, 132, 99)',
            borderColor: 'rgb(255, 132, 99)',
            data: waterlevel,
            fill: false,
            lineTension: 0,
        }]
    },
    options: options
};

// Executed after scope change
function updateCharts(){
    tChart.update();
    hChart.update();
    pChart.update();
    //add
    wChart.update();
}

// Add data scope
document.getElementById('addData').addEventListener('click', function(){
    showLength.setDate(showLength.getDate()-1);
    updateCharts();
})

// Reduce data scope
document.getElementById('reduceData').addEventListener('click', function(){
    if(showLength.getTime() < today.getTime()){
        showLength.setDate(showLength.getDate()+1);
        updateCharts();
    }
})

// Draw graphs of recent 7 days
document.getElementById('recent').addEventListener('click', function(){
    showLength.setDate(today.getDate()-7);
    updateCharts();
})

window.onload = function(){
    // document.write("hoge");
    drawChart();
};
