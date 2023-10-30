const TIMEOUT = 5000; // ms
var connected = false;
var ourTimer = null;
var nodes = null;
var history = {};
var FREQ = 1000000000; // ms

function newtimer(f) {
    clearInterval(ourTimer);
    ourTimer = setTimeout(f, TIMEOUT);
}

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

function disconnect() {
    // set state to disconnected
    if (connected) {  // was connected, now disconnected
        console.log("disconnected");
        const d = new Date();
        document.getElementById("last_update").innerHTML = 'Disconnected since: ' + d.toLocaleTimeString();
        connected = false;
        newtimer(connect);
    }
}

function connect() {
    // try to connect
    console.log("connect");
    if (!connected) {
        try {
            var client = new XMLHttpRequest();
            client.open('GET', 'msg');
            client.send();
            // document.getElementById("last_update").innerHTML = 'Connected';
            client.onprogress = function () {
                console.log("onprogress");
                newtimer(disconnect);

                // use only last dict:
                let new_msg = this.responseText.slice(this.responseText.lastIndexOf("{\"t"));
                console.log(new_msg);
                data = JSON.parse(new_msg);

                nodes.each(function (n) {
                    var col = "#eeeeee";
                    if (this.parentElement.id in data) {
                        col = data[this.parentElement.id]['current'];
                    }
                    this.setAttribute("fill", col);
                    history[this.parentElement.id][0].push(data['timestamp']);
                    history[this.parentElement.id][1].push(col);
                });
                draw();

                const d = new Date();
                document.getElementById("last_update").innerHTML = 'Last update: ' + d.toLocaleTimeString();

                connected = true;
            }
        } catch (e) {
            console.log(e);
            disconnect();
        }
    }
}

function draw() {
    nodes.each(function (n) {
        var col = "#eeeeee";
        this.setAttribute("fill", col);
        let timestamps = history[this.parentElement.id][0];
        let colors = history[this.parentElement.id][1];
        // add bars for history
        for (var i = timestamps.length - 1; i >= 0; i--) {
            var ts = timestamps[i];
            var color = colors[i];
            var height = this.getHeight();

            var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            rect.setAttribute("x", x);
            rect.setAttribute("y", y);
            rect.setAttribute("width", width);
            rect.setAttribute("height", height);
            rect.setAttribute("fill", color);
            this.parentElement.appendChild(rect);
        }
    });
}

$("svg").ready(function () {
    // use panzoom
    var element = document.querySelector('svg');
    panzoom(element, {
        bounds: true,
        boundsPadding: 0.1
    });
});

$("svg").ready(function () {
    connect();

    console.log("done");
    $(".node").children("image").hide();
    var width = getWidth($(".node:first").children("polygon").attr("points"));
    nodes = $(".node").children("polygon");
    nodes.each(function (n) {
        history[this.parentElement.id] = [[], []];
        // {
        //    "1": [[121], [122], ['#eeeeee', '#ff9999']]}
    });
});
