#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include "ADS1X15.h"
#define SAMPLE_RATE 125

ADS1115 ADS(0x48);

float editValue = 0;

// WiFi Configuration
const char* ssid = "你的WiFi名称";
const char* password = "你的WiFi密码";

String message = "你好，这是一个测试消息";
String target_ip = "192.168.1.100";
int target_port = 80;

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED: // 连接断开时触发
      Serial.println("WebSocket连接断开");
      break;
    case WStype_CONNECTED: // 连接成功时触发
      Serial.println("WebSocket连接成功");
      // 发送字符串到服务器
      webSocket.sendTXT(message);
      break;
    case WStype_TEXT: // 收到文本消息时触发
      Serial.println("收到文本消息：");
      // 打印收到的消息内容
      Serial.println(String((char *)payload));
      break;
    case WStype_BIN: // 收到二进制消息时触发
      Serial.println("收到二进制消息，长度：");
      // 打印收到的消息长度
      Serial.println(length);
      break;
  }
}

void setup() {
    Serial.begin(115200);
    // Wire.begin();
    ADS.begin();
    // adc.setVoltageRange_mV(ADS1115_RANGE_6144);
    // adc.setConvRate(ADS1115_860_SPS);
    // adc.setMeasureMode(ADS1115_CONTINUOUS);
    // adc.setCompareChannels(ADS1115_COMP_0_GND);
    WiFi.begin(ssid, password);
    Serial.print("正在连接WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.print("已连接WiFi，本机IP地址为：");
    Serial.println(WiFi.localIP());
    webSocket.onEvent(webSocketEvent);
    webSocket.begin(target_ip, target_port, "/");
}


void loop() {   
    ADS.setGain(0);
    int16_t val_0 = ADS.readADC(0);
    float f = ADS.toVoltage(1);
    float volts0 = val_0 *f;
    float volts1;
    static unsigned long past = 0;
    unsigned long present = micros();
    unsigned long interval = present - past;
    past = present;

    // Run timer
    static long timer = 0;
    timer -= interval;

    // WebSocket Loop
    webSocket.loop();

    // Sample
    if(timer < 0){
        timer += 1000000 / SAMPLE_RATE;
        float sensor_value = volts0;
        float signal = ECGFilter(sensor_value);
        Serial.println(signal);
        volts1=signal;
        char buffer[32];
        sprintf(buffer, "%.2f,", value);
        sprintf(buffer + strlen(buffer) , "%lu,", millis());
        WebSocket.sendTXT(buffer);
        /* float voltage = 0.0;
           float voltage1 = 0.0;
           voltage = readChannel(ADS1115_COMP_0_GND);

           static unsigned long past = 0;
           unsigned long present = micros();
           unsigned long interval = present - past;
           past = present;

        // Run timer
        static long timer = 0;
        timer -= interval;
        if(timer < 0){
        timer += 1000000 / SAMPLE_RATE;
        float voltage1 = ECGFilter(voltage);*/
    }
}

float ECGFilter(float input)
{
    float output = input;
    {
        static float z1, z2; // filter section state
        float x = output - 0.70682283*z1 - 0.15621030*z2;
        output = 0.28064917*x + 0.56129834*z1 + 0.28064917*z2;
        z2 = z1;
        z1 = x;
    }
    {
        static float z1, z2; // filter section state
        float x = output - 0.95028224*z1 - 0.54073140*z2;
        output = 1.00000000*x + 2.00000000*z1 + 1.00000000*z2;
        z2 = z1;
        z1 = x;
    }
    {
        static float z1, z2; // filter section state
        float x = output - -1.95360385*z1 - 0.95423412*z2;
        output = 1.00000000*x + -2.00000000*z1 + 1.00000000*z2;
        z2 = z1;
        z1 = x;
    }
    {
        static float z1, z2; // filter section state
        float x = output - -1.98048558*z1 - 0.98111344*z2;
        output = 1.00000000*x + -2.00000000*z1 + 1.00000000*z2;
        z2 = z1;
        z1 = x;
    }
    return output;
}
