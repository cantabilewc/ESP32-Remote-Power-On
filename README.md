# ESP32-Remote-Power-On
Control ESP32 to remotely power on the PC

# ✅ 專案實作架構說明與問題解決總結

**主題：用手機透過 MAKE.com 遠端開門（控制 ESP32）**

---

## 📌 架構總覽：

```
手機（Shortcuts / LINE / Webhook）
      ↓
  MAKE.com 發 HTTP GET 請求
      ↓
  ngrok（跑在筆電上）
      ↓
  轉發請求到 ESP32 的 HTTP Server（在家中區域網）
      ↓
  ESP32 接收到 GET 請求後 → 控制 Servo 馬達開門
```

---

## ✅ 技術元件與角色

| 元件          | 角色 / 功能                        |
| ----------- | ------------------------------ |
| ESP32       | 負責執行開門動作（內建 HTTP Server）       |
| MicroPython | 寫 ESP32 的控制邏輯（馬達 + 網路）         |
| ngrok       | 在筆電建立「外網 ➝ 內網」通道               |
| 筆電          | 負責執行 ngrok，轉送流量給 ESP32         |
| MAKE.com    | 發出 HTTP 請求（手機觸發）               |
| 手機          | 透過 LINE bot / Shortcuts 發出開門請求 |

---

## 🧨 遇到的關鍵問題與解決方案

| 問題編號 | 問題描述                     | 原因分析                                      | 解決方法                                          |
| ---- | ------------------------ | ----------------------------------------- | --------------------------------------------- |
| 1️⃣  | ESP32 `accept()` 沒有反應    | 筆電和 ESP32 不在同一網段（桌電是有線 LAN，ESP32 是 Wi-Fi） | 改用筆電透過 Wi-Fi 連上與 ESP32 相同的 SSID（`ASUS_50_2G`） |
| 2️⃣  | ngrok 顯示 502 Bad Gateway | 筆電無法打通 ESP32 IP，因此無法將 ngrok request 轉發成功  | 確認 ngrok 執行指向 `192.168.50.119:8080`，且筆電與其在同網域 |
| 3️⃣  | ping 不通 ESP32            | ESP32 不支援 ICMP（ping），但實際 HTTP 可通          | 改用瀏覽器 / curl 直接打 ESP32 URL 進行測試               |
| 4️⃣  | 打網址會開門兩次                 | 瀏覽器自動請求 `/favicon.ico` 導致第二次觸發            | 程式中加入判斷：只在 `path == "/"` 時執行開門                |
| 5️⃣  | 用 iPhone 熱點打不進 ESP32     | iPhone 熱點封鎖 LAN-to-LAN（裝置彼此無法互打）          | 改用家用 Wi-Fi 分享器環境或 Android 熱點                  |

---

* ✅ 成功建立 ESP32 HTTP Server，監聽並回應開門指令
* ✅ 成功從筆電 ngrok 轉送流量，讓 MAKE.com 能控制內網的 ESP32
* ✅ 成功用手機按下觸發，經過 MAKE ➝ ngrok ➝ ESP32 開啟 Servo 馬達

---

## 🎯 架構亮點

* 📦 **使用 ngrok 搭橋，讓內網裝置接受外部控制**
* 🔧 **MicroPython 驅動 Servo 並架設 socket server**
* 🔒 **ESP32 行為可擴充驗證邏輯（如 key 驗證）**
* 📱 **手機前端透過 MAKE.com 實現無 App 控制硬體**

