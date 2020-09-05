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

$('#data').scrollTop(1000000);

getStatusRaspi();
setInterval(() => {
    getStatusRaspi();
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
    console.log("Connected!");
    client.subscribe("temperature")
}
// Connect the client, providing an onConnect callback
client.connect({
	onSuccess: onConnect
});