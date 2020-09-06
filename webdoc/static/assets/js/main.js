const getStatusRaspi = () => {
    $.ajax({
        url: 'getStatus',
        success: (respond) => {
            $("#cpuLoad").text(respond.cpu.utilize + " %");
            $("#cpuTemp").text(respond.cpu.temp + "°C");
            $("#memoryLoad").text(respond.memory.percent + " %");
        }
    })
}
const getStatusData = () => {
    $.ajax({
        url: 'getCounter',
        success: (respond) => {
            $("#dataReceived").text(respond.received);
            $("#dataBlocked").text(respond.blocked);
            $("#dataSent").text(respond.sent);
            $("#dataNow").text(respond.time);
        }
    })
}

$('#data').scrollTop(1000000);

getStatusRaspi();
getStatusData();
setInterval(() => {
    getStatusRaspi();
    getStatusData();
}, 5000)

setInterval(() => {
    $("#data").append("")
}, 300000)


// Create a client instance: Broker, Port, Websocket Path, Client ID
client = new Paho.MQTT.Client("10.3.141.1", Number(9001), "/ws", "clientId");
// set callback handlers
client.onConnectionLost = function (responseObject) {
    console.log("Connection Lost: "+responseObject.errorMessage);
}
client.onMessageArrived = function (message) {
//   console.log("Message Arrived: "+message.payloadString);
  $("#data").append(message.payloadString + "<br>")
  $('#data').scrollTop(999999999);
}
// Called when the connection is made
function onConnect(){
    console.log("Client is connected!");
    client.subscribe("temperature")
    client.subscribe("hummidity")
    client.subscribe("pressure")
    client.subscribe("pm10")
    client.subscribe("co")
    client.subscribe("co2")
}
// Connect the client, providing an onConnect callback
client.connect({
	onSuccess: onConnect
});