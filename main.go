package main

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type Client struct {
	conn *websocket.Conn
}

var clients = make(map[*Client]bool)

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}
	defer conn.Close()

	client := &Client{conn: conn}
	clients[client] = true

	for {
		messageType, p, err := conn.ReadMessage()
		if err != nil {
			delete(clients, client)
			return
		}
		if messageType == websocket.TextMessage {
			broadcastMessage(p)
			log.Println("forwarding message: " + string(p))
		}
	}
}

func broadcastMessage(message []byte) {
	for client := range clients {
		err := client.conn.WriteMessage(websocket.TextMessage, message)
		if err != nil {
			delete(clients, client)
		}
	}
}

func main() {
	http.HandleFunc("/ws", handleWebSocket)
	http.Handle("/", http.FileServer(http.Dir("dist")))
	http.ListenAndServe(":80", nil)
}
