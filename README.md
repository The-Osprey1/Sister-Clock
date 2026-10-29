# SisterClock ✨

> A handcrafted, Wi-Fi connected LED dot matrix clock and weather station tailored with love for your sister. Built for the **ESP8266 Wemos D1 Mini** driving a **4-in-1 MAX7219 LED dot matrix display** in the [MakerWorld 3009244](https://makerworld.com/en/models/3009244-esp8266-clock-digital-clock-esp8266-d1-mini) enclosure.

---

## 💖 Why SisterClock?

While standard matrix clocks display time and weather, **SisterClock** is customized as a thoughtful, delightful gift:

- **Mobile Customizer Experience:** When connecting with a smartphone, an instant hero customizer card lets her personalize time format (12h vs 24h military), select between 3 clock display looks, choose between 3 animated alarm alerts, switch to a clock-only (no date) mode, and adjust display glow with touch-friendly presets.
- **Sister Affirmations & Heartbeat Cheer:** Periodically surprises her with uplifting messages throughout the day (e.g., *"HAVE A WONDERFUL DAY, SIS! ❤️"*, *"YOU MAKE THE WORLD BRIGHTER! ✨"*, *"REMEMBER TO DRINK WATER & SMILE :)"*, *"LOVE YOU TO THE MOON & BACK! ❤️"*).
- **Custom Love Notes & Messages:** Send real-time messages directly to her desk or nightstand from the Web UI or via simple HTTP requests.
- **Cute Matrix Glyphs:** Typing `<3` or `[LOVE]` automatically renders an animated glowing heart on the LED matrix! Also supports `[STAR]`, `[SMILE]`, `[MOON]`, and `[BELL]`.
- **Nighttime Auto-Dimming:** Dims to an ultra-soft glow after hours (or powers down completely) so it never disturbs her sleep.
- **Birthday & Event Countdowns:** Built-in countdown mode with cake/star icons for her birthday or special milestones.
- **100% Clean Gift Build:** All upstream donation popups, BuyMeACoffee nag screens, and telemetry have been completely removed.
- **Plug-and-Play Setup:** Self-contained captive portal hotspot (`SisterClock-Setup`) with friendly, zero-jargon configuration.

---

## 🖨️ 3D Enclosure (MakerWorld Model 3009244)

SisterClock is dimensioned and pin-mapped to fit the sleek 3D-printed case on MakerWorld:
👉 **[ESP8266 Clock / Digital Clock ESP8266 D1 Mini (Model 3009244)](https://makerworld.com/en/models/3009244-esp8266-clock-digital-clock-esp8266-d1-mini)**

See our complete [MakerWorld Build Guide](MAKERWORLD_BUILD_GUIDE.md) for slicer tips, diffuser layer techniques, and assembly tricks.

---

## 🔌 Hardware Wiring

Connect the **MAX7219 4-in-1 Module** (FC-16) to the **ESP8266 D1 Mini**:

| MAX7219 Pin | ESP8266 D1 Mini Pin | GPIO | Wire Color (Rec.) | Notes |
|:---|:---:|:---:|:---:|:---|
| **VCC** | **5V** | - | 🔴 Red | Connect to 5V (NOT 3.3V) |
| **GND** | **G (GND)** | - | ⚫ Black | Ground |
| **DIN** | **D8** | GPIO 15 | 🟡 Yellow | Hardware SPI MOSI |
| **CS** | **D7** | GPIO 13 | 🟢 Green | Chip Select |
| **CLK** | **D5** | GPIO 14 | 🔵 Blue | Hardware SPI Clock |

*For complete wiring diagrams and optional buzzer hookup, see [WIRING.md](WIRING.md).*

---

## ⚡ Flashing Options (Choose Any)

### Option 1: Browser-Based Flashing (Fastest & Easiest)
1. Open [`SisterClock/web_installer/index.html`](web_installer/index.html) in **Google Chrome** or **Microsoft Edge**.
2. Plug the D1 Mini into your computer using a USB data cable.
3. Click **"Connect & Flash SisterClock"**, select your COM port, and wait ~30 seconds!

### Option 2: One-Click PowerShell Script (Windows)
Open PowerShell in the `SisterClock` folder and run:
```powershell
.\flash.ps1
```
*The script automatically detects the USB COM port, verifies `esptool`, and flashes the precompiled `dist/firmware.bin`.*

### Option 3: PlatformIO CLI
Compile and flash with one command:
```bash
pio run -t upload
```

### Option 4: Arduino IDE
1. Open `firmware/SisterClock.ino` in Arduino IDE.
2. Select Board: **LOLIN(WEMOS) D1 R2 & mini**.
3. Flash Size: **4MB (FS:2MB OTA:~1019KB)**.
4. Install libraries: `ArduinoJson` (v7), `MD_Parola`, `MD_MAX72xx`, `ESPAsyncTCP`, `ESPAsyncWebServer`.
5. Click **Upload**.

---

## 📶 First-Time Wi-Fi Setup

1. **Power on SisterClock:** On first boot, the display shows a pulsing heart `<3` indicating setup mode.
2. **Connect to Hotspot:** On your smartphone or laptop, connect to the Wi-Fi network:
   - **SSID:** `SisterClock-Setup`
   - **Password:** `bestbrother`
3. **Open Portal:** Navigate to `http://192.168.4.1` (or `http://sisterclock.local`).
4. **Configure Settings:**
   - Select your home Wi-Fi and enter the password.
   - Enter your OpenWeatherMap API Key & City (optional, for live weather).
   - Choose 12-hour or 24-hour clock and temperature units (°F or °C).
   - Ensure **Sister Affirmations** is toggled ON.
5. Click **Save & Reboot**. SisterClock connects to Wi-Fi, syncs NTP time, and scrolls its assigned local IP address!

---

## 💌 Sending Live Messages & API Tokens

### Web UI
Open `http://sisterclock.local` in your browser anytime to change brightness, set timers, or send scrolling messages.

### Message Tokens
Special tokens inside custom messages automatically convert to graphics:
- `<3` or `[LOVE]` &rarr; Glowing Heart ❤️
- `[STAR]` &rarr; Sparkle Star ✨
- `[SMILE]` &rarr; Happy Face 😊
- `[MOON]` &rarr; Crescent Moon 🌙
- `[BELL]` &rarr; Chime Bell 🔔

### REST API (`/action`)
Send messages via curl, Python, or Home Assistant:
```bash
curl "http://sisterclock.local/action?message=Good%20morning%20sis!%20%3C3&scrolls=2"
```

---

## 📁 Repository Structure

```
SisterClock/
├── dist/
│   └── firmware.bin          # Precompiled ready-to-flash binary (759 KB)
├── firmware/
│   ├── SisterClock.ino       # Main firmware source code
│   ├── index_html.h          # Embedded responsive Web UI & styling
│   ├── version.h             # Firmware identity and version
│   ├── mfactoryfont.h        # 8x8 font and dot matrix glyph table
│   ├── alarm.h               # Alarm scheduler and logic
│   ├── buzzer.h              # Piezo sound synthesizer
│   ├── days_lookup.h         # Multilingual day of week strings
│   ├── months_lookup.h       # Multilingual month strings
│   └── tz_lookup.h           # IANA timezone database
├── tests/
│   └── test_sisterclock.py   # Automated pytest verification suite (10 tests)
├── web_installer/
│   ├── index.html            # WebSerial browser installer
│   └── manifest.json         # ESP Web Tools manifest
├── flash.ps1                 # Automated PowerShell flashing tool
├── flash.bat                 # Windows double-click flasher
├── platformio.ini            # PlatformIO build configuration
├── MAKERWORLD_BUILD_GUIDE.md # 3D printing & enclosure assembly guide
├── WIRING.md                 # Hardware pinout & wiring diagram
└── README.md                 # Master documentation
```

---

## ❤️ License
Personal non-commercial use. Handcrafted with love for your sister.
