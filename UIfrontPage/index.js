var lottieContainer = document.getElementById('myLottie');
var player = document.querySelector('#myLottie > lottie-player');
var socket = new WebSocket("ws://127.0.0.1:8080");
var socket2 = new WebSocket("ws://127.0.0.1:8081");
var lastStatus = "waiting";
var currentStatus = "";

// 连接开启时的回调函数
socket.onopen = function(event) {
    console.log("Connection opened.");
};

// 连接关闭时的回调函数
socket.onclose = function(event) {
    console.log("Connection closed.");
};

// 连接出错时的回调函数
socket.onerror = function(event) {
    console.error("WebSocket error observed:", event);
};

socket.onmessage = function(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var data = reader.result;
        //只有当状态发生变化时才更新动画
        if(data == lastStatus){
            return;
        }

        console.log("Received data: " + data);
        lastStatus = data;
        player.stop();
        switch(data){
            case "waiting":
                lottieContainer.innerHTML = `<lottie-player id="player" src="https://assets9.lottiefiles.com/packages/lf20_8KprVpwPMy.json" background="transparent" speed="1" loop autoplay></lottie-player>`;
                document.getElementById("status").innerHTML = "等待唤醒";

                break;
            case "listening":
                lottieContainer.innerHTML = `<lottie-player id="player" src="https://assets1.lottiefiles.com/packages/lf20_rvSMJ15we8.json" background="transparent" speed="1" loop autoplay></lottie-player>`;
                document.getElementById("status").innerHTML = "听您说话";

                break;
            case "speaking":
                lottieContainer.innerHTML = `<lottie-player id="player" src="https://assets8.lottiefiles.com/packages/lf20_Xa4OfBisU2.json" background="transparent" speed="1" loop autoplay></lottie-player>`;
                document.getElementById("status").innerHTML = "我在回应";

                break;
        }
        // Update the player variable to point to the new animation
        player = document.querySelector('#myLottie > lottie-player');


    };
    reader.readAsText(event.data);
};

// 连接开启时的回调函数
socket2.onopen = function(event) {
    console.log("ws2 Connection opened.");
};

// 连接关闭时的回调函数
socket2.onclose = function(event) {
    console.log("ws2 Connection closed.");
};

// 连接出错时的回调函数
socket2.onerror = function(event) {
    console.error("WebSocket2 error observed:", event);
};


socket2.onmessage = function(event) {
    console.log(event)
    var reader = new FileReader();
    reader.onload = function() {
        var text = reader.result;
        //只有当状态发生变化时才更新动画

        console.log("收到字幕: " + text);
        document.getElementById("text").innerHTML = text;
    };
    reader.readAsText(event.data);
};

