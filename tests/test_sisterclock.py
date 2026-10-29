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
