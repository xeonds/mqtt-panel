package main

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

func handleWebSocket(srcConns, dstConns map[*websocket.Conn]bool) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		srcConn, err := (&websocket.Upgrader{
			CheckOrigin: func(r *http.Request) bool {
				return true
			},
		}).Upgrade(w, r, nil)
		if err != nil {
			return
		}
		defer srcConn.Close()
		srcConns[srcConn] = true
		for {
			messageType, p, err := srcConn.ReadMessage()
			if err != nil {
				delete(srcConns, srcConn)
				return
			} else if messageType == websocket.TextMessage {
				for dstConn := range dstConns {
					if err := dstConn.WriteMessage(websocket.TextMessage, p); err != nil {
						delete(dstConns, dstConn)
					}
				}
				log.Println("Forwarding message: " + string(p))
			}
		}
	}
}

func main() {
	// 简单的服务端：将来自某个客户端的信息广播出去
	var conns = make(map[*websocket.Conn]bool)
	http.HandleFunc("/ws", handleWebSocket(conns, conns))
	http.Handle("/", http.FileServer(http.Dir("dist")))
	panic(http.ListenAndServe(":8765", nil))
}
