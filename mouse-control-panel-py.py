import tkinter as tk 
from threading import Thread, Event
import pyautogui
import time
import keyboard
import random
import json
import os
from tkinter import messagebox, scrolledtext
import pystray
from PIL import Image, ImageDraw
import sys
from datetime import datetime, timedelta
import queue

clicking = False
nudging = False
cycling = False
nudge_start_pos = (0, 0)
saved_positions = []
current_cycle_index = 0
save_file = "mouse_positions.json"
settings_file = "settings.json"
exit_event = Event()
action_queue = queue.Queue()

click_interval_range = (0, 3)
nudge_interval_range = (0, 4)
max_positions = 4

# Manual override detection
manual_override = False
last_manual_move = time.time()
mouse_check_interval = 1  # how often to check (in seconds)
pause_duration = 15  # seconds to pause after last manual movement
last_mouse_position = pyautogui.position()

# Scheduling
schedule_time = None

# Logging
log_messages = []
def log(msg):
    log_messages.append(msg)
    if len(log_messages) > 100:
        log_messages.pop(0)
    log_box.config(state='normal')
    log_box.delete(1.0, tk.END)
    log_box.insert(tk.END, '\n'.join(log_messages))
    log_box.config(state='disabled')
    log_box.yview(tk.END)
    print(msg)

def load_saved_positions():
    global saved_positions
    if os.path.exists(save_file):
        try:
            with open(save_file, 'r') as f:
                saved_positions = json.load(f)
                log(f"Loaded saved positions: {saved_positions}")
        except Exception as e:
            log(f"Error loading saved positions: {e}")

def save_positions_to_file():
    with open(save_file, 'w') as f:
        json.dump(saved_positions, f)
        log("Saved positions to file.")

def load_settings():
    global click_interval_range, nudge_interval_range, max_positions
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                data = json.load(f)
                click_interval_range = tuple(data.get("click_interval_range", (0, 3)))
                nudge_interval_range = tuple(data.get("nudge_interval_range", (0, 4)))
                max_positions = data.get("max_positions", 3)
                log("Settings loaded.")
        except Exception as e:
            log(f"Error loading settings: {e}")

def save_settings():
    data = {
        "click_interval_range": click_interval_range,
        "nudge_interval_range": nudge_interval_range,
        "max_positions": max_positions
    }
    with open(settings_file, 'w') as f:
        json.dump(data, f)
        log("Settings saved.")

def open_settings_window():
    def save_and_close():
        global click_interval_range, nudge_interval_range, max_positions
        try:
            click_interval_range = (float(click_min.get()), float(click_max.get()))
            nudge_interval_range = (float(nudge_min.get()), float(nudge_max.get()))
            max_positions = int(max_pos.get())
            save_settings()
            settings_win.destroy()
            update_ui()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("300x250")

    tk.Label(settings_win, text="Click Interval (min - max)").pack()
    click_min = tk.Entry(settings_win)
    click_min.insert(0, str(click_interval_range[0]))
    click_min.pack()
    click_max = tk.Entry(settings_win)
    click_max.insert(0, str(click_interval_range[1]))
    click_max.pack()

    tk.Label(settings_win, text="Nudge Interval (min - max)").pack()
    nudge_min = tk.Entry(settings_win)
    nudge_min.insert(0, str(nudge_interval_range[0]))
    nudge_min.pack()
    nudge_max = tk.Entry(settings_win)
    nudge_max.insert(0, str(nudge_interval_range[1]))
    nudge_max.pack()

    tk.Label(settings_win, text="Max Saved Positions").pack()
    max_pos = tk.Entry(settings_win)
    max_pos.insert(0, str(max_positions))
    max_pos.pack()

    tk.Button(settings_win, text="Save", command=save_and_close).pack(pady=10)

def click_loop():
    while not exit_event.is_set():
        if clicking and not manual_override:
            pyautogui.click(button='left')
            log("Click!")
        time.sleep(random.uniform(*click_interval_range))

def toggle_clicking():
    global clicking, cycling
    clicking = not clicking
    if clicking:
        log("Clicking started.")
        if len(saved_positions) == max_positions:
            if not cycling:
                cycling = True
                log("Cycle loop also started.")
                Thread(target=cycle_positions, daemon=True).start()
        else:
            log("Not enough saved positions to start cycling.")
    else:
        log("Clicking stopped.")
        cycling = False
    update_ui()

def toggle_nudging():
    global nudging, nudge_start_pos
    nudging = not nudging
    if nudging:
        nudge_start_pos = pyautogui.position()
        log("Nudging started.")
        Thread(target=nudge_loop, daemon=True).start()
    else:
        pyautogui.moveTo(nudge_start_pos)
        log("Nudging stopped. Resetting mouse position.")
    update_ui()

def nudge_loop():
    while nudging and not exit_event.is_set():
        if not manual_override:
            x_offset = random.randint(-20, 20)
            y_offset = random.randint(-20, 20)
            cur_x, cur_y = pyautogui.position()
            pyautogui.moveTo(cur_x + x_offset, cur_y + y_offset)
            log(f"Nudged by ({x_offset}, {y_offset})")
        time.sleep(random.uniform(*nudge_interval_range))

def save_position():
    global saved_positions
    pos = pyautogui.position()
    if len(saved_positions) >= max_positions:
        saved_positions = []
        log("Resetting saved positions.")
    saved_positions.append(pos)
    log(f"Position {len(saved_positions)} saved: {pos}")
    save_positions_to_file()
    update_ui()
    messagebox.showinfo("Position Saved", f"Position {len(saved_positions)} saved: {pos}")

def start_cycling():
    global cycling
    if len(saved_positions) != max_positions:
        log("You must save all positions before cycling.")
        return
    if cycling:
        log("Already cycling.")
        return
    cycling = True
    log("Starting cycle through saved positions...")
    Thread(target=cycle_positions, daemon=True).start()
    update_ui()

def stop_cycling():
    global cycling
    cycling = False
    log("Stopped cycling.")
    update_ui()

def cycle_positions():
    global current_cycle_index
    while cycling and not exit_event.is_set():
        if not manual_override:
            pos = saved_positions[current_cycle_index]
            log(f"Moving to position {current_cycle_index + 1}: {pos}")
            pyautogui.moveTo(pos)
        for _ in range(30):
            if not cycling or exit_event.is_set():
                return
            time.sleep(1)
        current_cycle_index = (current_cycle_index + 1) % max_positions

def monitor_manual_mouse_movement():
    global manual_override, last_manual_move, last_mouse_position
    while not exit_event.is_set():
        current_pos = pyautogui.position()
        if current_pos != last_mouse_position:
            last_manual_move = time.time()
            if not manual_override:
                log("Manual mouse movement detected. Pausing automation.")
                manual_override = True
        elif manual_override and (time.time() - last_manual_move > pause_duration):
            log("Resuming automation after manual activity pause.")
            manual_override = False
        last_mouse_position = current_pos
        time.sleep(mouse_check_interval)

def listen_hotkeys():
    keyboard.add_hotkey('F8', lambda: action_queue.put(toggle_clicking))
    keyboard.add_hotkey('F9', lambda: action_queue.put(toggle_nudging))
    keyboard.add_hotkey('F7', lambda: action_queue.put(save_position))
    keyboard.add_hotkey('esc', lambda: action_queue.put(stop_all))
    keyboard.wait()

def update_ui():
    status_label.config(text=f"Clicking: {'ON' if clicking else 'OFF'}")
    toggle_btn.config(text="Stop" if clicking else "Start")
    nudge_status_label.config(text=f"Nudging: {'ON' if nudging else 'OFF'}")
    nudge_btn.config(text="Stop Nudging" if nudging else "Start Nudging")
    save_status_label.config(text=f"Saved Positions: {len(saved_positions)} / {max_positions}")
    cycle_status_label.config(text=f"Cycling: {'ON' if cycling else 'OFF'}")
    scheduler_label.config(text=f"Scheduled Start: {schedule_time.strftime('%H:%M:%S')}" if schedule_time else "No Schedule Set")
    version_label.config(text="Version: 1.0.0")

def stop_all():
    global clicking, nudging, cycling
    clicking = nudging = cycling = False
    exit_event.set()
    log("All actions stopped by panic key (ESC).")
    root.quit()

def minimize_to_tray():
    root.withdraw()
    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill='white')
    icon = pystray.Icon("MouseControl", image, "Mouse Control", menu=pystray.Menu(
        pystray.MenuItem("Restore", lambda: restore_window()),
        pystray.MenuItem("Quit", lambda: stop_all())
    ))
    Thread(target=icon.run, daemon=True).start()

def restore_window():
    root.deiconify()

def schedule_start():
    global schedule_time
    minutes = schedule_entry.get()
    try:
        delay = int(minutes)
        schedule_time = datetime.now() + timedelta(minutes=delay)
        Thread(target=scheduler_loop, daemon=True).start()
        log(f"Scheduled to start in {delay} minutes at {schedule_time.strftime('%H:%M:%S')}.")
        update_ui()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a number of minutes.")

def scheduler_loop():
    global schedule_time
    while schedule_time and datetime.now() < schedule_time and not exit_event.is_set():
        time.sleep(1)
    if not exit_event.is_set():
        action_queue.put(toggle_clicking)
    schedule_time = None
    update_ui()

def process_queue():
    try:
        while True:
            func = action_queue.get_nowait()
            func()
    except queue.Empty:
        pass
    root.after(100, process_queue)

# GUI Setup
root = tk.Tk()
root.title("Mouse Control Panel")
root.geometry("300x560")

# Buttons
toggle_btn = tk.Button(root, text="Start", width=25, command=lambda: action_queue.put(toggle_clicking))
toggle_btn.pack(pady=5)

nudge_btn = tk.Button(root, text="Start Nudging", width=25, command=lambda: action_queue.put(toggle_nudging))
nudge_btn.pack(pady=5)

save_btn = tk.Button(root, text="Save Position (F7)", width=25, command=lambda: action_queue.put(save_position))
save_btn.pack(pady=5)

cycle_btn = tk.Button(root, text="Start Cycling (Auto w/F8)", width=25, command=start_cycling)
cycle_btn.pack(pady=5)

stop_cycle_btn = tk.Button(root, text="Stop Cycling", width=25, command=stop_cycling)
stop_cycle_btn.pack(pady=5)

settings_btn = tk.Button(root, text="Settings", width=25, command=open_settings_window)
settings_btn.pack(pady=5)

# Scheduler
tk.Label(root, text="Schedule Start (minutes from now):").pack(pady=2)
schedule_entry = tk.Entry(root, width=10)
schedule_entry.pack(pady=2)
tk.Button(root, text="Set Schedule", command=schedule_start).pack(pady=2)

# Labels
status_label = tk.Label(root, text="Clicking: OFF")
status_label.pack(pady=3)

nudge_status_label = tk.Label(root, text="Nudging: OFF")
nudge_status_label.pack(pady=3)

save_status_label = tk.Label(root, text="Saved Positions: 0 / 3")
save_status_label.pack(pady=3)

cycle_status_label = tk.Label(root, text="Cycling: OFF")
cycle_status_label.pack(pady=3)

scheduler_label = tk.Label(root, text="No Schedule Set")
scheduler_label.pack(pady=3)

version_label = tk.Label(root, text="Version: 1.0.0")
version_label.pack(pady=3)

info_label = tk.Label(root, text="F8 = Click | F9 = Nudge | F7 = Save Pos | ESC = Panic", font=("Arial", 8))
info_label.pack(pady=5)

# Log output
log_box = scrolledtext.ScrolledText(root, height=6, width=35, state='disabled')
log_box.pack(pady=5)

# Load data
load_settings()
load_saved_positions()
update_ui()

# Threads
Thread(target=click_loop, daemon=True).start()
Thread(target=listen_hotkeys, daemon=True).start()
Thread(target=monitor_manual_mouse_movement, daemon=True).start()
root.after(100, process_queue)

# Minimize to tray on close
root.protocol("WM_DELETE_WINDOW", minimize_to_tray)

root.mainloop()
