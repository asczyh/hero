# 通过 Airtest 和 ADB 连接 MuMu 模拟器。
MUMU_DEVICE_UDID = '127.0.0.1:16384'
AIRTEST_DEVICE_URI = f'Android://127.0.0.1:5037/{MUMU_DEVICE_UDID}?cap_method=JAVACAP'

GAME_PACKAGE = 'com.tencent.tmgp.eden'
GAME_ACTIVITY = 'com.tencent.shell.MainShellActivity'
BILIBILI_PACKAGE = 'tv.danmaku.bili'
BILIBILI_ACTIVITY = '.MainActivityV2'

# 战报区域使用当前屏幕的相对比例表示。
# OCR 和滑动操作会避开固定顶部栏和底部导航栏。
REPORT_VIEWPORT = {
    'left': 0.08,
    'top': 0.22,
    'right': 0.98,
    'bottom': 0.89,
}
# OCR 仅识别战报面板，排除玩家信息栏和播放控制栏。
# 上方较高的 REPORT_VIEWPORT 仍用于滑动和重叠读取。
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
