# SisterClock - Hardware Wiring Guide

Target Hardware: **ESP8266 Wemos D1 Mini** + **MAX7219 4-in-1 LED Matrix Module (FC-16)**
Enclosure: **MakerWorld Model 3009244**

---

## 📌 Pin Connection Table

| MAX7219 Module Pin | ESP8266 D1 Mini Pin | GPIO Number | Function / Description | Wire Color (Rec.) |
|:-------------------|:--------------------|:------------|:-----------------------|:------------------|
| **VCC**            | **5V**              | -           | 5V Power Supply        | 🔴 Red            |
| **GND**            | **G (GND)**         | -           | Ground                 | ⚫ Black          |
| **DIN** (Data In)  | **D8**              | **GPIO 15** | Software SPI data      | 🟡 Yellow         |
| **CS** (Chip Sel)  | **D7**              | **GPIO 13** | Software SPI select        | 🟢 Green          |
| **CLK** (Clock)    | **D5**              | **GPIO 14** | Software SPI clock       | 🔵 Blue           |

> **Important Power Note:** Connect MAX7219 **VCC to the 5V pin** on the D1 Mini (NOT 3.3V). A genuine MAX7219 specifies a 3.5 V minimum logic-high input at its stated 5 V supply conditions, so 3.3 V ESP8266 signals are not guaranteed to meet its specification. For reliable logic levels use a 5 V powered 74HCT125 or equivalent buffer on DIN, CS, and CLK, and connect all grounds together. Test the actual module and power supply in the finished enclosure.

---

## 🧩 Visual Wiring Diagram

```
       +-------------------------------------------------------+
       |             MAX7219 4-in-1 LED Matrix                 |
       |                   (32x8 Pixels)                       |
       +-----+-------+-------+-------+-------------------------+
         VCC    GND     DIN     CS     CLK
          |      |       |       |      |
          |      |       |       |      |
          |      |       |       |      |
         5V     GND     D8      D7     D5
       +-------------------------------------------------------+
       |             ESP8266 Wemos D1 Mini                     |
       |                (Micro-USB / USB-C)                    |
       +-------------------------------------------------------+
```

---

## ⚡ Optional Piezo Buzzer (Alarms & Timers)

If you wish to add an audible alarm or timer chime:

| Passive Buzzer Pin | ESP8266 D1 Mini Pin | GPIO Number | Description |
|:-------------------|:--------------------|:------------|:------------|
| **Positive (+)**   | **D6**              | **GPIO 12** | PWM Buzzer  |
| **Negative (-)**   | **G (GND)**         | -           | Ground      |

---

## 🛠 Assembly Tips for MakerWorld Model 3009244

1. **Header Pins Orientation:** If your MAX7219 module came with straight header pins that stick out too far for the case, desolder them or gently bend them 90 degrees flat against the PCB back. Alternatively, solder silicone hookup wires directly to the pads for the lowest profile fit.
2. **Wire Length:** Keep jumper wires between 6 cm and 10 cm. This allows easy folding into the rear cavity of the 3D-printed enclosure without pinching.
3. **USB Port Alignment:** Seat the D1 Mini so the USB-C or Micro-USB port aligns perfectly with the cutout on the rear shell before securing the backplate.
