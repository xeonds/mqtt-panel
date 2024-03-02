import time,ujson,network
import dht
import machine
from umqtt.simple import MQTTClient
from machine import ADC, Pin

# 定义颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

# 传感器引脚设置
EC_RST = Pin(16, Pin.OUT)
dht_pin = Pin(9, Pin.IN, Pin.PULL_UP)          # 温湿度传感器初始化
d = dht.DHT11(dht_pin)
beep = Pin(45, Pin.OUT)                         # 蜂鸣器初始化
LED1 = Pin(17, Pin.OUT)                         # LED灯初始化
LED2 = Pin(18, Pin.OUT)
LED3 = Pin(21, Pin.OUT)
button1 = Pin(46, Pin.IN, Pin.PULL_UP)          # 初始化按键，设置为输入模式
button2 = Pin(11, Pin.IN, Pin.PULL_UP)
button3 = Pin(12, Pin.IN, Pin.PULL_UP)
adc1 = ADC(Pin(5))                              # 两路ADC引脚初始化
adc1.atten(ADC.ATTN_11DB)
adc2 = ADC(Pin(7))
adc2.atten(ADC.ATTN_11DB)

topic_publish       = '$sys/${username}/${clientId}/thing/property/post'
topic_subscribe     = '$sys/${username}/${clientId}/thing/property/set'

keepalive   = 60
#######################下面就是需要修改的地方##########################################
# 修改为自己手机热点的名称和密码，尽量不要出现中文
wifi_ssid   = 'Vintage'
wifi_passwd = ''


clientId    = "EC800"                                                 # 设备ID
username    = "0KuShP5G6J"                                          # 产品ID
passwd      = "version=2018-10-31&res=products%2FtG1T8EU4T9%2Fdevices%2F0KuShP5G6J&et=1709385180&method=md5&sign=DlFfoUg%2B6vx3xmWOLrBXqQ%3D%3D"  # token
######################################################################################
mqttHostUrl = "mqtts.heclouds.com"                                  # 服务器地址,不用改
port        = 1883                                                  # 服务器端口,不用改

topic_publish       = topic_publish.replace('${username}', username)
topic_publish       = topic_publish.replace('${clientId}', clientId)
topic_subscribe       = topic_subscribe.replace('${username}', username)
topic_subscribe       = topic_subscribe.replace('${clientId}', clientId)

# 初始化串口
uart = machine.UART(1, tx=1, rx=2, baudrate=115200)

def send_at_command(command):
    print("Send->", command)
    uart.write(command + '\r\n')
    time.sleep(1)
    response = uart.read()
    if response: print("Rev:", response.decode('utf-8'))
    else: print("No response")
    return response.decode("utf-8")

# ADC数据读取函数
def get_adc_value():
    Value1 = adc1.read()
    Value2 = adc2.read()
    Value1 = int((Value1 / 4095) * 100)
    Value2 = int((Value2 / 4095) * 100)
    return Value1,Value2

# 传感器初始化函数
def init_sensor():
    beep.value(0)                               # 关闭蜂鸣器        
    EC_RST.value(1)                             # 重置EC传感器
    time.sleep(1)
    EC_RST.value(0)

    # 初始化GNSS模块
    send_at_command("AT+QGPS=1")
    
    LED1.value(0)                               #跑马灯
    LED2.value(0)
    LED3.value(0)
    LED1.value(1)   
    time.sleep(0.5)
    LED2.value(1)
    time.sleep(0.5)
    LED3.value(1)
    time.sleep(0.5)
    
# 按键读取函数
def read_buttons():
    button1_state = button1.value()
    button2_state = button2.value()
    button3_state = button3.value()
    # 检查哪个按键被按下，并打印出来
    if button1_state == 0:
        time.sleep_ms(10)  # 消抖延时
        if button1.value() == 0:  # 再次检测按键状态
            LED1.value(not LED1.value())  # 取反LED1的电平
            print("Button 1 is pressed")
    if button2_state == 0:
        time.sleep_ms(10)  # 消抖延时
        if button2.value() == 0:  # 再次检测按键状态
            LED2.value(not LED2.value())  # 取反LED2的电平
            print("Button 2 is pressed")
    if button3_state == 0:
        time.sleep_ms(10)  # 消抖延时
        if button3.value() == 0:  # 再次检测按键状态
            LED3.value(not LED3.value())  # 取反LED3的电平
            print("Button 3 is pressed")

# 云平台订阅消息接收函数
def receiveMessage(topic_subscribe, msg):
    message = ujson.loads(msg)
    data = message["params"]

def main():
    init_sensor()
    # 开始连接WIFI
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(wifi_ssid, wifi_passwd)
    
    while not wlan.isconnected():
        time.sleep(1)
        print('WIFI connecting!')

    # 等待连接
    time.sleep(1)
    # 连接成功提示
    print('WIFI connection succeeded!')

    # 连接OneNet
    client = MQTTClient(clientId, mqttHostUrl, port, username, passwd, keepalive)
    try: client.connect()
    except(e): 
        print("[OneNet Init] Initialization failed: " + e)
        return
    client.set_callback(receiveMessage)
    time.sleep(1)
    print('MQTT connection succeeded!')
    
    def get_gps_info():
        return send_at_command("AT+QGPSLOC=0")

    while True:
        try:
            time.sleep(0.1)
            read_buttons()
            d.measure()                             # 测量温湿度
            temperature = d.temperature()           # 获取温度值
            humidity = d.humidity()                 # 获取湿度值
            Value1,Value2 = get_adc_value()         # 读取两路ADC的值
            gps_data = get_gps_info()               # 读取GPS信息

            byte_msg = ujson.dumps({
                "id":"1697011901539",
                "version":"1.0",
                "params": {
                "ADC_value1":{"value":Value1},
                "ADC_value2":{"value":Value2},
                "temperature":{"value":temperature},
                "humidity":{"value":humidity},
                "location":{"value":gps_data}
            }}).encode('ascii')

            print(byte_msg)
            # 发布消息到云平台
            client.publish(topic_publish, msg=byte_msg)
            client.check_msg()
        except OSError as e:
            print('OSError:', e)

if __name__ == '__main__':
    main()
