import pyautogui
import time
import tkinter as tk
from threading import Thread

def get_color_state(color):
    states = {
        "赤金": [231, 255, 42, 255, 0, 251],
        "亮蓝": [64, 231, 121, 255, 167, 255],
        "暗青": [24, 63, 51, 120, 78, 166],
    }
    r, g, b = color
    for state, (r1, r2, g1, g2, b1, b2) in states.items():
        if r1 <= r <= r2 and g1 <= g <= g2 and b1 <= b <= b2:
            return state
    return "未知状态"

def check_side_states(positions, screenshot):
    states_count = {"赤金": 0, "亮蓝": 0}
    for x, y in positions:
        color = screenshot.getpixel((x, y))
        state = get_color_state(color)
        if state in states_count:
            states_count[state] += 1
    return states_count

def check_color_states():
    positions_left = [(245, 200), (285, 200), (325, 200), (365, 200)]
    positions_right = [(2070, 200), (2110, 200), (2150, 200), (2190, 200)]
    screenshot = pyautogui.screenshot()
    left_states = check_side_states(positions_left, screenshot)
    right_states = check_side_states(positions_right, screenshot)

    left_result = left_states["亮蓝"] if left_states["赤金"] == 0 else 4
    right_result = right_states["亮蓝"] if right_states["赤金"] == 0 else 4

    return left_result, right_result

def start_gui():
    root = tk.Tk()
    root.title("\u8ba1\u65f6\u4e0e\u72b6\u6001\u663e\u793a")
    root.attributes("-topmost", True)

    top_frame = tk.Frame(root)
    top_frame.pack()

    left_label = tk.Label(top_frame, text="\u5de6\u4fa7\u5012\u8ba1\u65f6: 0.0", font=("Arial", 10))
    left_label.pack(side=tk.LEFT, padx=10)
    right_label = tk.Label(top_frame, text="\u53f3\u4fa7\u5012\u8ba1\u65f6: 0.0", font=("Arial", 10))
    right_label.pack(side=tk.RIGHT, padx=10)

    count_frame = tk.Frame(root)
    count_frame.pack()

    left_count_label = tk.Label(count_frame, text="\u5de6\u4fa7\u8ba1\u6570: 0", font=("Arial", 10))
    left_count_label.pack(side=tk.LEFT, padx=10)
    right_count_label = tk.Label(count_frame, text="\u53f3\u4fa7\u8ba1\u6570: 0", font=("Arial", 10))
    right_count_label.pack(side=tk.RIGHT, padx=10)

    button_frame = tk.Frame(root)
    button_frame.pack()

    left_timer = [0]
    right_timer = [0]
    is_running = [False]
    monitor_left = [True]
    monitor_right = [True]

    def update_gui():
        while True:
            if is_running[0]:
                if left_timer[0] > 0:
                    left_timer[0] -= 0.1
                if right_timer[0] > 0:
                    right_timer[0] -= 0.1

                left_label.config(text=f"\u5de6\u4fa7\u5012\u8ba1\u65f6: {max(0, left_timer[0]):.1f}")
                right_label.config(text=f"\u53f3\u4fa7\u5012\u8ba1\u65f6: {max(0, right_timer[0]):.1f}")
            time.sleep(0.1)

    def monitor():
        previous_left_result = None
        previous_right_result = None

        while True:
            if is_running[0]:
                if left_timer[0] <= 0 and monitor_left[0]:
                    left_result, _ = check_color_states()
                    left_count_label.config(text=f"\u5de6\u4fa7\u8ba1\u6570: {left_result}")
                    if previous_left_result is not None and left_result < previous_left_result:
                        left_timer[0] = 14.5
                    previous_left_result = left_result

                if right_timer[0] <= 0 and monitor_right[0]:
                    _, right_result = check_color_states()
                    right_count_label.config(text=f"\u53f3\u4fa7\u8ba1\u6570: {right_result}")
                    if previous_right_result is not None and right_result < previous_right_result:
                        right_timer[0] = 14.5
                    previous_right_result = right_result
            time.sleep(0.05)

    def toggle_start_stop():
        is_running[0] = not is_running[0]
        start_button.config(text="\u505c\u6b62" if is_running[0] else "\u5f00\u59cb")

    def toggle_left_monitor():
        monitor_left[0] = not monitor_left[0]
        left_button.config(text="\u5de6\u4fa7: \u5f00\u542f" if monitor_left[0] else "\u5de6\u4fa7: \u5173\u95ed")

    def toggle_right_monitor():
        monitor_right[0] = not monitor_right[0]
        right_button.config(text="\u53f3\u4fa7: \u5f00\u542f" if monitor_right[0] else "\u53f3\u4fa7: \u5173\u95ed")

    start_button = tk.Button(button_frame, text="\u5f00\u59cb", font=("Arial", 10), command=toggle_start_stop)
    start_button.pack(side=tk.LEFT, padx=10)
    left_button = tk.Button(button_frame, text="\u5de6\u4fa7: \u5f00\u542f", font=("Arial", 10), command=toggle_left_monitor)
    left_button.pack(side=tk.LEFT, padx=10)
    right_button = tk.Button(button_frame, text="\u53f3\u4fa7: \u5f00\u542f", font=("Arial", 10), command=toggle_right_monitor)
    right_button.pack(side=tk.RIGHT, padx=10)

    Thread(target=update_gui, daemon=True).start()
    Thread(target=monitor, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    start_gui()
