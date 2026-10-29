# SisterClock candidate hardware check

The candidate image is `dist/firmware-test.bin`. It is a test build, and the existing installer still uses the earlier firmware.

1. Connect the D1 Mini with a USB data cable. Identify its serial port; do not assume the first port belongs to the clock. Save any configuration you need before changing firmware.
2. From the repository folder, replace `COM3` with the clock’s port and run:

   ```powershell
   python -m esptool --chip esp8266 --port COM3 --baud 460800 write-flash --flash-size detect 0x0 dist\firmware-test.bin
   ```

   Do not erase the entire flash unless you intend to remove stored settings. Power-cycle and confirm the display starts.
3. On a fresh setup or after deliberately changing Wi-Fi credentials, join `SisterClock-Setup` and open `http://192.168.4.1`. Test a failed password, retry, and a successful connection. Check the selected time zone and displayed time.
4. On the same home Wi-Fi, open the clock page. Test brightness, weekday alarm selection, saving, and the test alarm. Verify sound only if the buzzer is connected and enabled. Check Stop and Snooze.
5. Disconnect and restore the router and clock power. Confirm reconnection and that settings and alarms survive. Check nighttime dimming and message display.
6. Only after the checks pass, copy the tested candidate to both `dist/firmware.bin` and `web_installer/firmware.bin`; verify their hashes match and rerun the test suite.
