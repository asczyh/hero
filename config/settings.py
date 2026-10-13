# MuMu emulator connection through Airtest and ADB.
MUMU_DEVICE_UDID = 'emulator-5554'
AIRTEST_DEVICE_URI = f'Android://127.0.0.1:5037/{MUMU_DEVICE_UDID}?cap_method=JAVACAP'

GAME_PACKAGE = 'com.tencent.tmgp.eden'
GAME_ACTIVITY = 'com.tencent.shell.MainShellActivity'
BILIBILI_PACKAGE = 'tv.danmaku.bili'
BILIBILI_ACTIVITY = '.MainActivityV2'

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
REPORT_SCROLL_PERCENT = 0.5
REPORT_NO_NEW_TEXT_LIMIT = 2
REPORT_MAX_SWIPES = 300
REPORT_OUTPUT_DIR = 'output'
