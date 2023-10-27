const TIMEOUT = 5000; // ms
var connected = false;
var ourTimer = null;

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
                let new_msg = this.responseText.slice(this.responseText.lastIndexOf("{"));
                console.log(new_msg);
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
            }
        } catch (e) {
            console.log(e);
            disconnect();
        }
    }
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
});
