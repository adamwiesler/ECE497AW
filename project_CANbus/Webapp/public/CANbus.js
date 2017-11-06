var plotColors = {pv: "#00CC00", out: "#0000CC", sp: "#222222", };

let urlHost = window.location.hostname;
urlHost = urlHost.toLowerCase().replace('localhost','127.0.0.1');
const websock = new WebSocket(`ws://${urlHost}:9091`);

Highcharts.setOptions({global: {useUTC: true, timezoneOffset: (new Date()).getTimezoneOffset()}});
var highChart;

//*************************************************
// angular controller
//*************************************************
var app = angular.module("myApp", []);

app.controller("AngularController", function($scope, $http) {
  //for debugging access to $scope:
  window.MYSCOPE = $scope;
  //create charts on startup
  highChart = createHighChart();

  $scope.CANData = { 9999: {id: 9999, ms: Date.now(), data: [0,1,2,3,4,5,6,7] } };
  $scope.indexCANData = 0;
  $scope.dataPeriod = 100;
  $scope.dataTimer;
  $scope.requestCANData = function() {
    const rq = JSON.stringify({ rq: 'CAN', payload: 9999 });
    websock.send(rq); // Request can message ID 1349 from the server
  }

  $scope.setRequestInterval = function(o) {
    clearInterval(o.dataTimer);
    o.dataTimer = setInterval(o.requestCANData, o.dataPeriod);
  }
  $scope.setRequestInterval($scope);

  websock.onmessage = function (event) {
    // console.log(event.data);
    const inData = JSON.parse(event.data);
    if (typeof inData === 'object' && typeof inData.rq === 'string' && inData.rq === 'CAN') {
      $scope.CANData[inData.payload.id] = inData.payload;
      $scope.$apply();
      highChart.get('CANData').addPoint([inData.payload.ms, inData.payload.data[1]], true, true);
    }
  }

});

//*************************************************
// Create the Highcharts chart
//*************************************************
function createHighChart() {
  var fakeData = dummyData(100, 100);
   $('#Chart1').highcharts({
      chart: {zoomType: 'xy', alignTicks: false, type: 'line', animation: false},
      credits: {enabled: false},
      exporting: {enabled: false},
      legend: {enabled: false},
      title: {text: null, style: {fontSize: "12px", color: "black"}},
      tooltip: {shared: true},
      plotOptions: {line: {animation: false}},
      xAxis: [{type: "datetime", crosshair: true, labels:{style: {fontSize: "8px"}}}],
      yAxis: [{endOnTick: false, startOnTick: false, lineWidth: 0.75, title: {text: null, style: {color: plotColors.pv}},
                labels:{format: "", style: {fontSize: "8px", color: plotColors.pv}}},
             ],
      series: [
         {data: fakeData, id: 'CANData', name: 'CAN Data', lineWidth: 0.75, color: plotColors.pv, marker: {enabled: false}, yAxis: 0},
              ]
   });
   return $('#Chart1').highcharts();
}

//*************************************************
// Dummy data
//*************************************************
function dummyData(count, interval) {
  var data = [];
  var now = Date.now();
  for (var i = 0; i < count; i++) {
    data.push([now - interval*(count-i), 0]);
  }
  return data;
}
