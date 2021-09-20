import websocket

def on_message(wsapp, message):
    print(message)

wsapp = websocket.WebSocketApp("wss://stream.meetup.com/2/rsvps",
        on_message=on_message)

wsapp.run_forever()
