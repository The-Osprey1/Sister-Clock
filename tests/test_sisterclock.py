import os
import re
import pytest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIRMWARE_DIR = os.path.join(BASE_DIR, "firmware")
DIST_DIR = os.path.join(BASE_DIR, "dist")
INO_FILE = os.path.join(FIRMWARE_DIR, "SisterClock.ino")
HTML_FILE = os.path.join(FIRMWARE_DIR, "index_html.h")
VERSION_FILE = os.path.join(FIRMWARE_DIR, "version.h")
BIN_FILE = os.path.join(DIST_DIR, "firmware.bin")
PLATFORMIO_INI = os.path.join(BASE_DIR, "platformio.ini")

def test_source_files_exist():
    assert os.path.isfile(INO_FILE), "SisterClock.ino must exist"
    assert os.path.isfile(HTML_FILE), "index_html.h must exist"
    assert os.path.isfile(VERSION_FILE), "version.h must exist"
    assert os.path.isfile(PLATFORMIO_INI), "platformio.ini must exist"

def test_firmware_binary_exists_and_size():
    assert os.path.isfile(BIN_FILE), "Precompiled firmware.bin must exist in dist/"
    size = os.path.getsize(BIN_FILE)
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
    assert 'DEFAULT_AP_PASSWORD = "sisterclock"' in content, "Default AP password must be sisterclock"

def test_no_upstream_donation_nagware():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        ino_content = f.read()
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    assert "SUPPORTING ESPTIMECAST KEEPS THE PROJECT ALIVE" not in ino_content
    assert "buymeacoffee.com" not in html_content
    assert "Enjoying ESPTimeCast?" not in html_content

def test_sister_affirmations_present():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert "HAVE A WONDERFUL DAY, SIS!" in content
    assert "LOVE YOU TO THE MOON & BACK!" in content
    assert "SO PROUD TO BE YOUR BROTHER!" in content
    assert "SISTER_MESSAGE_COUNT = 8" in content
    assert "messageScrollTimes = 2" in content, "Sister affirmations should scroll twice"

def test_custom_token_aliases():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert '{ "<3", "\\x8F", 7 }' in content, "<3 must map to heart glyph"
    assert '{ "[LOVE]", "\\x8F", 7 }' in content, "[LOVE] must map to heart glyph"
    assert '{ "[STAR]", "\\x0F", 8 }' in content, "[STAR] must map to star glyph"
    assert '{ "[SMILE]", "\\x02", 8 }' in content, "[SMILE] must map to smile glyph"

def test_buffer_overflow_protections():
    with open(INO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # timeWithSeconds buffer must be 32, not 12
    assert "char timeWithSeconds[32];" in content
    assert "char timeWithSeconds[12];" not in content

    # snprintf alarm schedule buffer in alarm.h
    with open(os.path.join(FIRMWARE_DIR, "alarm.h"), "r", encoding="utf-8") as f:
        alarm_content = f.read()
    assert "char timeBuf[10];" in alarm_content

def test_web_ui_customization():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert "<title>SisterClock ✨ Settings</title>" in content
    assert "Sister Affirmations &amp; Cheerful Messages ❤️" in content
    assert "--accent-color: #f43f5e;" in content
    assert "SisterClock ✨ Handcrafted with Love" in content

def test_firmware_binary_strings():
    with open(BIN_FILE, "rb") as f:
        bin_data = f.read()

    assert b"SisterClock" in bin_data, "Binary must contain SisterClock string"
    assert b"sisterclock" in bin_data, "Binary must contain sisterclock string"
    assert b"SisterClock-Setup" in bin_data, "Binary must contain SisterClock-Setup SSID"
    assert b"SUPPORTING ESPTIMECAST KEEPS THE PROJECT ALIVE" not in bin_data
    assert b"buymeacoffee.com" not in bin_data
