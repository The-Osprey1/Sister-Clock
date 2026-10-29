# MakerWorld Model 3009244 - 3D Printing & Assembly Guide

This guide is specifically tailored for building the **SisterClock** using the popular 3D printable case from MakerWorld:
👉 **MakerWorld Model 3009244**: [ESP8266 Clock / Digital Clock ESP8266 D1 Mini](https://makerworld.com/en/models/3009244-esp8266-clock-digital-clock-esp8266-d1-mini)

---

## 🖨️ Recommended 3D Print Settings

### 1. Main Housing / Body
- **Material:** PLA, PLA Matte, or PETG (Pink, Lavender, Mint, or warm White look fantastic for a sister's gift)
- **Layer Height:** `0.20 mm` Standard (or `0.16 mm` Optimal)
- **Walls / Perimeters:** `3` (ensures clean edges and eliminates light bleed)
- **Top / Bottom Layers:** `4` top / `4` bottom
- **Infill:** `15% - 20%` (Gyroid or Grid)
- **Supports:** Usually none needed if printed on the rear face down.

### 2. Front Light Diffuser / Grille
The MAX7219 matrix LEDs are very bright point-light sources. To give the numbers a soft, modern, high-end "digital glow":
- **Diffuser Material:** Semi-translucent White PLA or Natural Clear PETG.
- **Diffuser Thickness:** Print 1 or 2 layers (0.2 mm - 0.4 mm).
- **Pro Maker Tip:** You can also cut a small strip of translucent drafting paper or frosted plastic sheet (from a folder) and slide it between the LEDs and the front printed grille.

---

## 🧰 Required Bill of Materials (BOM)

| Item | Qty | Notes |
|:-----|:---:|:------|
| **ESP8266 Wemos D1 Mini** | 1 | USB-C or Micro-USB version |
| **MAX7219 4-in-1 Dot Matrix Display** | 1 | FC-16 module (32x8 dots, red, blue, green, or white LEDs) |
| **Hookup Wires** | 5 | 28-30 AWG flexible silicone wire or short female-female DuPont jumpers |
| **M2 or M3 Screws** (optional) | 2-4 | For mounting depending on print version |
| **5V USB Power Supply + Cable** | 1 | Standard 5V 1A or 2A phone charger |

---

## 🔧 Step-by-Step Assembly Instructions

### Step 1: Flash Firmware Before Assembly
Always flash the firmware onto the D1 Mini **before** mounting it inside the case:
- Serve `web_installer/` over HTTPS or localhost and open the page in Chrome/Edge, OR
- Run `.\flash.ps1` in PowerShell, OR
- Run `pio run -t upload` with PlatformIO.

Once flashed, plug in the 5 wires to test the display on your workbench:
- Verify that the pulsing heart animation `<3` appears when the clock turns on.

### Step 2: Prepare the MAX7219 Module
- Many MAX7219 modules come with right-angle or straight 5-pin headers on both ends.
- The **input** end is marked `VCC, GND, DIN, CS, CLK`. The **output** end is marked `VCC, GND, DOUT, CS, CLK`.
- Connect your wires **only to the input end** (`DIN`).
- If the header pins prevent the module from seating flush in the printed frame, bend the pins flat or desolder them and solder wires directly.

### Step 3: Insert Display into Front Bezel
1. Lay the front printed bezel on a soft cloth.
2. Insert your light diffuser strip (if using sheet diffuser).
3. Slide the MAX7219 module into the front retaining clips or screw standoffs.
4. Ensure the display orientation has `DIN` on the intended side (display flip can also be corrected in the Web UI if mounted upside-down).

### Step 4: Route Wires to the D1 Mini
1. Solder or connect the 5 wires to the D1 Mini per [WIRING.md](WIRING.md):
   - `VCC` &rarr; `5V`
   - `GND` &rarr; `G`
   - `DIN` &rarr; `D8` (GPIO 15)
   - `CS`  &rarr; `D7` (GPIO 13)
   - `CLK` &rarr; `D5` (GPIO 14)
2. Keep wire bundle tidy with a small piece of Kapton tape.

### Step 5: Mount D1 Mini & Snap Close
1. Align the D1 Mini's USB port with the rear cutout in the 3D-printed housing.
2. Gently tuck the slack wires into the void space.
3. Snap or fasten the back plate in place.
4. Plug in your USB cable — your SisterClock is ready for first-time Wi-Fi setup!
