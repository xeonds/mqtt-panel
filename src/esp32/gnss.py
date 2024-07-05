import machine
uart = machine.UART(1, tx=1, rx=2, baudrate=115200)
def send_at_command(command):
    print("Send->", command)
    uart.write(command + '\r\n')
    time.sleep(1)
    response = uart.read()
    if response:
        response_str = response.decode('utf-8')
        print("Rev:", response_str)
    else:
        print("No response")
    return response
def init_gps():
    send_at_command("AT+QGPSCFG=\"outport\",\"uartdebug\"")
    send_at_command("AT+QGPS=1")
    send_at_command("AT+QGPSLOC=0")