const TIMEOUT = 100; // ms
var connected = false;
var disconnectTimer = null;

function getWidth(points) {
    var previous_x = null;
    var width = 0;
    let ps = points.split(" ");
    ps.forEach(function (p, _, _) {
        var x = Number(p.split(",")[0])
        if (previous_x === null) {
            previous_x = x
        } else {
            width = Math.max(width, Math.abs(previous_x - x))
        }
    });
    return width;
}

$("svg").ready(function () {
    // use panzoom
    var element = document.querySelector('svg');
    panzoom(element, {
        bounds: true,
        boundsPadding: 0.1
    });
});

function disconnected() {
    if (connected) {  // was connected, now disconnected
        console.log("disconnected");
        const d = new Date();
        document.getElementById("last_update").innerHTML = 'Disconnected since: ' + d.toLocaleTimeString();
        connected = false;
        clearInterval(disconnectTimer);
        setTimeout(connect, TIMEOUT);
    }
}

function connect() {
    console.log("connect");
    disconnectTimer = setTimeout(disconnected, TIMEOUT);
    if (!connected) {
        try {
            var client = new XMLHttpRequest();
            client.open('GET', 'msg');
            client.send();
            client.onprogress = function () {
                console.log("onprogress");
                clearInterval(disconnectTimer);
                disconnectTimer = setTimeout(disconnected, TIMEOUT);

                // use only last dict:
                let new_msg = this.responseText.slice(this.responseText.lastIndexOf("{"));
                console.log(new_msg);
                try {
                    data = JSON.parse(new_msg);

                    let nodes = $(".node").children("polygon");
                    nodes.each(function (n) {
                        var col = "#eeeeee";
                        if (this.parentElement.id in data) {
                            col = data[this.parentElement.id];
                        }
                        this.setAttribute("fill", col);
                    });

                    const d = new Date();
                    document.getElementById("last_update").innerHTML = 'Last update: ' + d.toLocaleTimeString();

                    connected = true;
                } catch (e) {
                    console.log(e);
                    disconnected();
                }
            }
        } catch (e) {
            console.log(e);
            disconnected();
        }
    }
}


$("svg").ready(function () {
    disconnectTimer = setTimeout(disconnected, TIMEOUT);
    connect();

    console.log("done");
    $(".node").children("image").hide();
    var width = getWidth($(".node:first").children("polygon").attr("points"));
});

// let myVar = setInterval(myTimer, 1000);
// function myTimer() {
//     const xhttp = new XMLHttpRequest();

//     // Define a callback function
//     xhttp.onload = function () {

//         data = JSON.parse(this.responseText)
//         document.getElementById("num").innerHTML = data[0];
//         let nodes = $(".node").children("polygon");
//         nodes.each(function (n) {
//             let id = this.parentElement.id;
//             let col = color_by_state(data[id]);
//             this.setAttribute("fill", col);
//         });
//     }

//     // Send a request
//     xhttp.open("GET", "data");
//     xhttp.send();
// }