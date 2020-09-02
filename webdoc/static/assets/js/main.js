const getStatusRaspi = () => {
    $.ajax({
        url: 'getStatus',
        success: (respond) => {
            console.log(respond);
            $("#valueCPUTemp").text(respond.cpuTemp);
            $("#valueMemoryLoad").text(respond.memoryLoad);
        }
    })
}

getStatusRaspi();
setInterval(() => {
    getStatusRaspi();
}, 5000)

var chartTemp = am4core.create("chartTemp", am4charts.XYChart);


function initDateChart(chart, data) {
    console.log(data)
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    // Create chart instance
    // Add data
    chart.data = data;
    // Set input format for the dates
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss.SSSSSS";
    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.title.text = "Temperature"

    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.tooltipText = "{value}°C - {date}"
    series.strokeWidth = 2;
    series.minBulletDistance = 15;
    series.stroke = am4core.color("#FF0000")
    // Drop-shaped tooltips
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.strokeOpacity = 0;
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.label.minWidth = 40;
    series.tooltip.label.minHeight = 40;
    series.tooltip.label.textAlign = "middle";
    series.tooltip.label.textValign = "middle";
    // Make bullets grow on hover
    var bullet = series.bullets.push(new am4charts.CircleBullet());
    bullet.circle.strokeWidth = 2;
    bullet.circle.radius = 4;
    bullet.circle.fill = am4core.color("#fff");
    var bullethover = bullet.states.create("hover");
    bullethover.properties.scale = 1.3;
    // Make a panning cursor
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "panXY";
    chart.cursor.xAxis = dateAxis;
    chart.cursor.snapToSeries = series;
    // Create vertical scrollbar and place it before the value axis
    chart.scrollbarY = new am4core.Scrollbar();
    chart.scrollbarY.parent = chart.leftAxesContainer;
    chart.scrollbarY.toBack();
    // Create a horizontal scrollbar with previe and place it underneath the date axis
    chart.scrollbarX = new am4charts.XYChartScrollbar();
    chart.scrollbarX.series.push(series);
    chart.scrollbarX.parent = chart.bottomAxesContainer;

    // console.log(chart);
}

$.ajax({
    method: 'GET',
    data: {
        sensor: 'temperature',
        id: 'cd14'
    },
    url: '/getLast100rows?sensor=temperature&id=cd14',
    success: (respond) => {
        respond = respond.map((element) => {
            return {
                date: element.time,
                value: element.value
            }
        })
        initDateChart(chartTemp, respond)
    }
})

// setInterval(() => {
//     now = Date()
//     stringNow = moment(now).format('YYYY-MM-DD HH:mm:ss.SSS');
//     chartTemp.addData({
//         date : stringNow,
//         value : 50
//     })


// }, 2000)
