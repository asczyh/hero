APPIUM_SERVER_URL = 'http://localhost:4723'

# 设备与应用配置
PLATFORM_NAME = 'Android'
PLATFORM_VERSION = '12'
DEVICE_NAME = 'zyh'
APP_PACKAGE = 'tv.danmaku.bili'
APP_ACTIVITY = '.MainActivityV2'
AUTOMATION_NAME = 'UiAutomator2'

# 驱动配置
NO_RESET = True
NEW_COMMAND_TIMEOUT = 6000
IMPLICITLY_WAIT = 6

# MuMu emulator currently attached through ADB. This is separate from the
# Bilibili app settings above so the existing search example remains usable.
MUMU_DEVICE_UDID = 'emulator-5554'
GAME_PACKAGE = 'com.tencent.tmgp.eden'

# Battle report viewport as fractions of the active screen. The fixed header
# and bottom navigation are intentionally excluded from OCR and swipe gestures.
REPORT_VIEWPORT = {
    'left': 0.08,
    'top': 0.22,
    'right': 0.98,
    'bottom': 0.89,
}
# OCR only the battle-log panel, excluding the player HUD and playback controls.
# Keep the taller REPORT_VIEWPORT above for swipe gestures and overlap.
REPORT_OCR_VIEWPORT = {
    'left': 0.08,
    'top': 0.35,
    'right': 0.98,
    'bottom': 0.88,
}
REPORT_SCROLL_PERCENT = 0.65
REPORT_NO_NEW_TEXT_LIMIT = 2
REPORT_MAX_SWIPES = 300
REPORT_OUTPUT_DIR = 'output'
