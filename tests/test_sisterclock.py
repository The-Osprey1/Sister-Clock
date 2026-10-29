import os
import re
import pytest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIRMWARE_DIR = os.path.join(BASE_DIR, "firmware")
DIST_DIR = os.path.join(BASE_DIR, "dist")
WEB_INSTALLER_DIR = os.path.join(BASE_DIR, "web_installer")
INO_FILE = os.path.join(FIRMWARE_DIR, "SisterClock.ino")
FONT_FILE = os.path.join(FIRMWARE_DIR, "mfactoryfont.h")
HTML_FILE = os.path.join(FIRMWARE_DIR, "index_html.h")
VERSION_FILE = os.path.join(FIRMWARE_DIR, "version.h")
BIN_FILE = os.path.join(DIST_DIR, "firmware.bin")
WEB_BIN_FILE = os.path.join(WEB_INSTALLER_DIR, "firmware.bin")
MANIFEST_FILE = os.path.join(WEB_INSTALLER_DIR, "manifest.json")
PLATFORMIO_INI = os.path.join(BASE_DIR, "platformio.ini")

def test_source_files_exist():
    assert os.path.isfile(INO_FILE), "SisterClock.ino must exist"
    assert os.path.isfile(FONT_FILE), "mfactoryfont.h must exist"
    assert os.path.isfile(HTML_FILE), "index_html.h must exist"
    assert os.path.isfile(VERSION_FILE), "version.h must exist"
    assert os.path.isfile(PLATFORMIO_INI), "platformio.ini must exist"
    assert os.path.isfile(MANIFEST_FILE), "web_installer/manifest.json must exist"

def test_firmware_binary_exists_and_size():
    assert os.path.isfile(BIN_FILE), "Precompiled firmware.bin must exist in dist/"
    assert os.path.isfile(WEB_BIN_FILE), "Self-contained firmware.bin must exist in web_installer/"
    size = os.path.getsize(BIN_FILE)
    web_size = os.path.getsize(WEB_BIN_FILE)
    assert size == web_size, "dist/firmware.bin and web_installer/firmware.bin must match exactly"
    # ESP8266 4MB flash image is usually ~700KB - 850KB
    assert 500_000 < size < 1_048_576, f"Firmware binary size {size} is outside expected range"

def test_hardware_defaults_for_makerworld_3009244():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # D1 Mini pin definitions
    assert re.search(r"#define\s+L_CLK\s+14", content), "CLK must be GPIO 14 (D5 on D1 Mini)"
    assert re.search(r"#define\s+L_CS\s+13", content), "CS must be GPIO 13 (D7 on D1 Mini)"
    assert re.search(r"#define\s+L_DATA\s+15", content), "DATA/DIN must be GPIO 15 (D8 on D1 Mini)"

    # Display configuration
    assert "MD_MAX72XX::FC16_HW" in content, "Display hardware must be FC16_HW for 4-in-1 modules"
    assert re.search(r"#define\s+MAX_DEVICES\s+4", content), "MAX_DEVICES must be 4 for 4-in-1 matrix"

def test_sister_branding_and_identity():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert 'DEFAULT_HOSTNAME = "sisterclock"' in content, "Default hostname must be sisterclock"
    assert 'DEFAULT_AP_SSID = "SisterClock-Setup"' in content, "Default AP SSID must be SisterClock-Setup"
    assert 'DEFAULT_AP_PASSWORD = "bestbrother"' in content, "Default AP password must be bestbrother"
    assert '(char)0x8F' in content, "AP mode must show actual heart glyph (0x8F), not WIFI icon"

def test_no_upstream_donation_nagware():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        ino_content = f.read()
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    assert "SUPPORTING ESPTIMECAST KEEPS THE PROJECT ALIVE" not in ino_content
    assert "buymeacoffee.com" not in html_content
    assert "Enjoying ESPTimeCast?" not in html_content
    assert "esptimecast.com/firmware.json" not in html_content

def test_sister_affirmations_present():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert "VIBE CHECK: PASSED" in content
    assert "MAIN CHARACTER ENERGY" in content
    assert "GIFTED BY THE BEST BROTHER" in content
    assert "SISTER_MESSAGE_COUNT = 10" in content
    assert "messageScrollTimes = 2" in content, "Sister affirmations should scroll twice"

def test_sister_affirmation_logic_and_endpoints():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert "bool sisterAffirmations = true;" in content, "Sister affirmations must default to true"
    assert 'server.on("/send_affirmation"' in content, "Must expose /send_affirmation endpoint"
    assert 'server.on("/set_sister_affirmations"' in content, "Must expose /set_sister_affirmations endpoint"
    assert "calcNextAffirmationTime(" in content, "Must implement wake-hour daytime affirmation scheduling"

def test_custom_token_aliases():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert '{ "<3", "\\x8F", 7 }' in content, "<3 must map to heart glyph (0x8F)"
    assert '{ "[LOVE]", "\\x8F", 7 }' in content, "[LOVE] must map to heart glyph (0x8F)"
    assert '{ "[STAR]", "\\xD1", 7 }' in content, "[STAR] must map to real 5-point star glyph (0xD1)"
    assert '{ "[SPARKLE]", "\\xD2", 5 }' in content, "[SPARKLE] must map to sparkle glyph (0xD2)"
    assert '{ "[SMILE]", "\\xD0", 7 }' in content, "[SMILE] must map to smile glyph (0xD0)"
    assert '{ ":)", "\\xD0", 7 }' in content, ":) must map to smile glyph (0xD0)"
    assert '{ ":-)", "\\xD0", 7 }' in content, ":-) must map to smile glyph (0xD0)"

def test_font_custom_glyphs():
    with open(FONT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert "7, 16, 32, 70, 64, 70, 32, 16" in content, "Smiley face glyph must be defined at 208 (0xD0)"
    assert "7, 68, 44, 30, 63, 30, 44, 68" in content, "5-point star glyph must be defined at 209 (0xD1)"
    assert "5, 4, 14, 31, 14, 4" in content, "Sparkle glyph must be defined at 210 (0xD2)"

def test_buffer_overflow_protections():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # timeWithSeconds buffer must be 32, not 12
    assert "char timeWithSeconds[32];" in content
    assert "char timeWithSeconds[12];" not in content

    # timeSpacedStr buffer must be 64 to avoid stack overflow when timeWithSeconds is spaced
    assert "char timeSpacedStr[64];" in content
    assert "char timeSpacedStr[24];" not in content

    # snprintf alarm schedule buffer in alarm.h
    with open(os.path.join(FIRMWARE_DIR, "alarm.h"), "r", encoding="utf-8") as f:
        alarm_content = f.read()
    assert "char timeBuf[10];" in alarm_content

def test_utf8_emoji_conversion():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # UTF-8 parser must decode multi-byte emoji sequences
    assert "utf8ToLatin1(" in content
    assert "0x8F" in content, "Must map heart emojis to 0x8F"
    assert "0xD1" in content, "Must map star emojis to 0xD1"
    assert "0xD2" in content, "Must map sparkle emojis to 0xD2"
    assert "0xD0" in content, "Must map smileys to 0xD0"

def test_web_ui_customization():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert "<title>SisterClock ✨ Settings</title>" in content
    assert "Daily Vibe Check &amp; Messages ✨" in content
    assert "--accent-color: #f43f5e;" in content
    assert "SisterClock ✨ Best Brother Edition" in content
    assert "uploadOtaFile()" in content, "UI must support local .bin firmware uploading"
    assert "sendAffirmationNow()" in content, "UI must support instant surprise affirmation button"
    assert "insertToken(" in content, "UI must support quick token insertion buttons"
    assert "TUNES_STORAGE_KEY = \"sisterclock_tunes\"" in content

def test_web_installer_portability():
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert '"path": "firmware.bin"' in content, "Manifest must refer to local portable firmware.bin"

def test_firmware_binary_strings():
    with open(BIN_FILE, "rb") as f:
        bin_data = f.read()

    assert b"SisterClock" in bin_data, "Binary must contain SisterClock string"
    assert b"sisterclock" in bin_data, "Binary must contain sisterclock string"
    assert b"SisterClock-Setup" in bin_data, "Binary must contain SisterClock-Setup SSID"
    assert b"SUPPORTING ESPTIMECAST KEEPS THE PROJECT ALIVE" not in bin_data
    assert b"buymeacoffee.com" not in bin_data


def test_clock_and_alarm_styles_backend():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify global variables and defaults
    assert "int clockStyle = 1;" in content
    assert "int alarmStyle = 0;" in content

    # Verify endpoints registered
    assert 'server.on("/set_clock_style", HTTP_POST, setHandler);' in content
    assert 'server.on("/set_alarm_style", HTTP_POST, setHandler);' in content
    assert 'server.on("/test_alarm", HTTP_POST,' in content

    # Verify action handling
    assert 'action == "clock_style"' in content
    assert 'action == "alarm_style"' in content

    # Verify config serialization and saving
    assert 'doc["clockStyle"] = clockStyle;' in content
    assert 'doc["alarmStyle"] = alarmStyle;' in content
    assert 'clockStyle = doc["clockStyle"]' in content
    assert 'alarmStyle = doc["alarmStyle"]' in content

def test_mobile_customizer_ui_elements():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Hero card header
    assert 'id="sister-customizer"' in content
    assert "Make your clock yours" in content
    assert "mobile-hero-card" in content

    # 12h vs 24h controls
    assert 'id="btn-12h"' in content
    assert 'id="btn-24h"' in content
    assert "12-Hour (AM/PM)" in content
    assert "24-Hour" in content

    # 3 Clock face looks
    assert 'id="clock-style-0"' in content
    assert 'id="clock-style-1"' in content
    assert 'id="clock-style-2"' in content
    assert "Minimal" in content
    assert "Day Tag" in content
    assert "Time + Seconds" in content

    # Show date toggle
    assert 'id="btn-showdate-yes"' in content
    assert 'id="btn-showdate-no"' in content
    assert "Hide Date" in content

    # Touch brightness slider & presets
    assert 'id="mobile-bright-slider"' in content
    assert 'id="mobile-bright-val"' in content
    assert "Night (1)" in content
    assert "Cozy (5)" in content
    assert "Day (10)" in content
    assert "Max (15)" in content

    # 3 Alarm alert styles & test alarm
    assert 'id="alarm-style-0"' in content
    assert 'id="alarm-style-1"' in content
    assert 'id="alarm-style-2"' in content
    assert "Strobe Flash" in content
    assert "Bell & Heart" in content
    assert "Wake-Up" in content
    assert "testAlarmNow()" in content

def test_mobile_customizer_js_handlers():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert "function setTwelveHourMode(" in content
    assert "function chooseClockStyle(" in content
    assert "function chooseAlarmStyle(" in content
    assert "function setShowDateMode(" in content
    assert "function updateMobileBrightness(" in content
    assert "function setBrightnessPreset(" in content
    assert "function testAlarmNow(" in content

    # Verify config.json initialization
    assert "b12.classList.toggle(\"active\", is12hMode);" in content
    assert "clock-style-" in content
    assert "alarm-style-" in content

def test_alarm_style_render_modes():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Style 0: Inverted Strobe
    assert "P.setInvert(alarmInvert);" in content
    # Style 1: Bouncing Bell & Heart
    assert "\\xBF" in content
    assert "\\x8F" in content
    # Style 2: Wake-Up text banner
    assert "WAKE UP!" in content


def test_reset_wifi_endpoint():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert 'server.on("/reset_wifi", HTTP_POST,' in content
    assert 'doc["ssid"] = "";' in content
    assert 'doc["password"] = "";' in content
    assert 'writeConfigSafely(doc);' in content
    assert 'ESP.restart();' in content

def test_ap_setup_banner_display():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify friendly scrolling setup banner in AP mode
    assert 'CONNECT PHONE TO: SisterClock-Setup' in content
    assert '192.168.4.1' in content
    assert '\\x8F SETUP \\x8F' in content
    assert 'dnsServer.processNextRequest();' in content

def test_mobile_pwa_and_setup_button():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # PWA mobile app meta tags
    assert 'name="apple-mobile-web-app-capable" content="yes"' in content
    assert 'name="apple-mobile-web-app-title" content="SisterClock"' in content
    assert 'name="theme-color" content="#18102a"' in content

    # One-tap switch Wi-Fi / setup mode button and handler
    assert "resetWifiAndSetup()" in content
    assert "Connect to New Wi-Fi (Setup Mode)" in content
    assert 'fetch("/reset_wifi"' in content

def test_printable_qr_card():
    qr_card_path = os.path.join(WEB_INSTALLER_DIR, "qr_setup_card.html")
    assert os.path.exists(qr_card_path), "qr_setup_card.html must exist"
    with open(qr_card_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "WIFI:S:SisterClock-Setup;T:WPA;P:bestbrother;;" in content
    assert "http://192.168.4.1" in content
    assert "Print Setup Card" in content
    assert "SisterClock ✨ Quick Start" in content


def test_captive_portal_and_ap_mode_robustness():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        ino = f.read()

    # /index.html must be explicitly registered alongside /
    assert 'server.on("/index.html", HTTP_GET, sendIndexHtml);' in ino

    # /scan must switch to WIFI_AP_STA if in WIFI_AP mode
    assert 'WiFi.mode(WIFI_AP_STA);' in ino

    # handleCaptivePortal must send immediate 404 for missing static assets to prevent socket hangs
    assert 'uri.endsWith(".png")' in ino
    assert 'request->send(404, "text/plain", "Not found");' in ino

    # AP loop helper banner must be reachable in isAPMode block
    assert 'CONNECT PHONE TO: SisterClock-Setup' in ino
    assert 'P.displayScroll' in ino

def test_index_html_js_syntax_integrity():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Verify no unmatched braces in the main script block
    import re
    scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL)
    assert len(scripts) >= 1, "Must contain at least one script block"

    main_script = scripts[0]
    # Simple brace balance check
    # Filter out braces inside strings and regexes
    clean_js = re.sub(r'([\'"`])(?:\\.|(?!\1).)*\1', '', main_script)
    clean_js = re.sub(r'//.*', '', clean_js)
    clean_js = re.sub(r'/\*.*?\*/', '', clean_js, flags=re.DOTALL)

    open_braces = clean_js.count('{')
    close_braces = clean_js.count('}')
    assert open_braces == close_braces, f"Mismatched braces in JS: {open_braces} open vs {close_braces} close"
