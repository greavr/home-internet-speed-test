// Results array
var stats = [['Time','Ping']];
var count = 1;
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function GetLatest() {
    var ping_div = document.getElementById("LatestPing");
    $.ajax({
        type: 'GET',
        url: '/latest',
        contentType: "application/json",
        dataType: 'json',
        cache: false,
        success: function(response) {
            // Data
            var data = response.ping;
            console.log(response);
            ping_div.innerHTML = "<b>" + data + "ms</b> | (" + count + ")";
            // Add Data to Diagram
            // Check that date/time is new
            var this_result = [response.time_stamp,data]
            if (stats[stats.length -1 ][0] != response.time_stamp) {
                stats.push(this_result)
                drawChart()
                count +=1;
            }
        },
        complete:function(data){
            setTimeout(GetLatest,2000);
        }
    })  
}

function drawChart() {
    var data = google.visualization.arrayToDataTable(stats)

    var options = {
        title: {position: 'none'},
        curveType: 'function',
        backgroundColor: '#e4e4e4',
        legend: {position: 'none'}
      };

      var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

      chart.draw(data, options);
}


$( document ).ready(function() {
    console.log( "ready!" );
    setTimeout(GetLatest,2000);
})