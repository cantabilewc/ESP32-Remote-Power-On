from machine import Pin
from servo import Servo
import network
import socket
import time

# 馬達設定
my_servo = Servo(Pin(22))

# Wi-Fi 連線
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('1hsiang', '123567890')
while not sta.isconnected():
    pass

ip = sta.ifconfig()[0]
print('✅ Wi-Fi 連線成功，IP:', ip)

# 開門動作
def unlock():
    print("🔓 開門中...")
    my_servo.write_angle(0)
    time.sleep(3)
    my_servo.write_angle(90)
    print("🔒 關門")
    
# HTTP server
s = socket.socket()
port = 8080
s.bind(('', port))
s.listen(1)
print('🌐 HTTP server ready at: http://%s:%d' % (ip, port))
print(sta.ifconfig())

while True:
    cl, addr = s.accept()
    request = cl.recv(1024).decode()
    print('📩 收到請求：\n', request)
    
    try:
        lines = request.split('\r\n')
        if len(lines) > 0 and ' ' in lines[0]:
            method, path, *_ = lines[0].split(' ')
            print("👉 method:", method, "| path:", path)

            # 這裡你可以加 if 判斷 method、path 是否符合需求
            unlock()
            response = 'HTTP/1.1 200 OK\r\n\r\n門已開啟'
        else:
            response = 'HTTP/1.1 400 Bad Request\r\n\r\n請求格式錯誤'
    except Exception as e:
        print("⚠️ 錯誤:", e)
        response = 'HTTP/1.1 500 Internal Server Error\r\n\r\n伺服器錯誤'

    # 🔧 缺的兩行在這裡！
    cl.send(response)
    cl.close()