"use strict";

let socket;

function sendMessage() {
    const userInput = document.getElementById("usertext");
    const message = userInput.value.trim();

    if (message !== "") {
        socket.send(message);
        userInput.value = ""; // Clear input field after sending message
    }
}

function displayMessage(message) {
    const chatbox = document.getElementById("chatbox");
    chatbox.value += message + "\n";
}

function initializeWebSocket() {
    socket = new WebSocket("ws://" + document.location.host + "/sock");

    socket.addEventListener("open", () => {
        console.log("WebSocket connection opened");
        document.getElementById("sendbutton").disabled = false; // Enable send button
    });

    socket.addEventListener("message", (event) => {
        const message = event.data;
        displayMessage(message);
    });

    socket.addEventListener("close", () => {
        console.log("WebSocket connection closed");
    });

    socket.addEventListener("error", (error) => {
        console.error("WebSocket error:", error);
    });
}

function keyWasPressed(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function main() {
    initializeWebSocket();
}

main();
