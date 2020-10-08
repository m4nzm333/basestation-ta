var host = window.location.hostname;

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


// Create a client instance
var client = new Paho.MQTT.Client(location.hostname, Number(9001), "clientId");

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({ onSuccess: onConnect });


// called when the client connects
async function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  var topic = await $.ajax({
    url: 'topic',
    success: (respond) => {
      console.log(respond);
    }
  })
  topic.forEach(topicRow => {
    client.subscribe(topicRow);
    $("#daftarParam").append(`<li>${topicRow}</li>`)
  });
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
      
      [idSensor, param] = message.topic.split('/')
      if (!$(`#${idSensor}`).length){
        $("#masterData").append(`
          <div id="${idSensor}">
            <h3>${idSensor}</h3>
            <div class="overflow-auto rowData" style="height: 250px; overflow-y: scroll;"></div>
          </div>
        `)
      }
      $(`#${idSensor} > .rowData`).append(param  + "," + message.payloadString + "<br>")
      $(`#${idSensor} > .rowData`).scrollTop(999999999);
}


// Buat Sigmoid Untuk Tampilan Node
// create an array with nodes
var nodes = new vis.DataSet([
  { id: 1, label: "Basestation" }
]);

// create an array with edges
var edges = new vis.DataSet([
]);

// create a network
var container = document.getElementById("mynetwork");
var data = {
  nodes: nodes,
  edges: edges
};
var options = {};
var network = new vis.Network(container, data, options);

var queue = []
var idNode = 2

function queueExist(idSensor){
  for(var i = 0; i < queue.length; i+=1){
    if(queue[i].idSensor == idSensor){
      return true
    }
  }
  return false
  
}
function queueRemove(idSensor){
  newQueue = []
  for(var i = 0; i < queue.length; i+=1){
    if(queue[i].idSensor != idSensor){
      newQueue.push(queue[i])
    }
  }
  queue.forEach(element => {
      
  });
  queue = newQueue
}

setInterval(async () => {
  var node = await $.ajax({
    url: 'queue',
    success: (respond) => {
      respond.forEach(element => {
        if(!queueExist(element.id)){
          queue.push({
            idNode: idNode,
            idSensor: element.id
          })
          nodes.add({id: idNode, label: element.id})
          edges.add({from: idNode, to: 1})
          idNode += 1
        }
      });
      
    }
  })
}, 5000)