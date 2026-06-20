import customtkinter as ctk
import time
import threading
import queue


class AppUI(ctk.CTk):
    def __init__(self, start_callback, stop_callback):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.title("Kick Live Archiver")
        self.geometry("560x500")
        self.resizable(False, False)

        self.start_callback = start_callback
        self.stop_callback = stop_callback

        self.monitoring_start = None
        self.recording_start = None
        self.running = True
        self._main_thread_id = threading.get_ident()
        self._ui_queue = queue.Queue()

        # ===== INPUT =====
        self.url_entry = ctk.CTkEntry(
            self,
            placeholder_text="https://kick.com/username",
            width=480,
        )
        self.url_entry.pack(pady=20)

        # ===== STATUS =====
        self.status_label = ctk.CTkLabel(
            self,
            text="OFFLINE",
            text_color="gray",
            font=("Segoe UI", 16, "bold"),
        )
        self.status_label.pack()

        # ===== TIMERS =====
        self.monitor_label = ctk.CTkLabel(self, text="Monitoring: 00:00:00")
        self.monitor_label.pack(pady=2)

        self.record_label = ctk.CTkLabel(self, text="Recording: --:--:--")
        self.record_label.pack(pady=2)

        # ===== PROGRESS BAR =====
        self.progress = ctk.CTkProgressBar(self, width=480)
        self.progress.set(0)
        self.progress.pack(pady=15)

        # ===== BUTTONS =====
        self.start_btn = ctk.CTkButton(self, text="Start Monitoring", command=self.start)
        self.start_btn.pack(pady=5)

        self.stop_btn = ctk.CTkButton(self, text="Stop", command=self.stop)
        self.stop_btn.pack(pady=5)
        self.stop_btn.configure(state="disabled")

        # ===== LOG =====
        self.log_box = ctk.CTkTextbox(self, width=520, height=170)
        self.log_box.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._ui_loop()

    # ===== UI CONTROL =====
    def start(self):
        try:
            started = bool(self.start_callback(self.url_entry.get()))
        except Exception as e:
            self.add_log(f"Start failed: {e}")
            started = False

        if not started:
            self.monitoring_start = None
            self.recording_start = None
            self.set_status("OFFLINE")
            return

        self.monitoring_start = time.time()
        self.recording_start = None
        self.set_status("MONITORING")

    def stop(self):
        self.monitoring_start = None
        self.recording_start = None
        try:
            self.stop_callback()
        except Exception as e:
            self.add_log(f"Stop failed: {e}")
        self.set_status("OFFLINE")

    def set_status(self, status):
        if threading.get_ident() != self._main_thread_id:
            self._ui_queue.put(("status", status))
            return
        self._apply_status(status)

    def _apply_status(self, status):
        if status == "OFFLINE":
            self.status_label.configure(text="OFFLINE", text_color="gray")
            self.record_label.configure(text="Recording: --:--:--")
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
        elif status == "MONITORING":
            self.status_label.configure(text="MONITORING", text_color="gray")
            self.record_label.configure(text="Recording: --:--:--")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
        elif status == "LIVE":
            self.status_label.configure(text="LIVE", text_color="red")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
        elif status == "RECORDING":
            self.status_label.configure(text="RECORDING", text_color="green")
            self.recording_start = time.time()
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")

    # ===== LOG =====
    def add_log(self, text):
        if threading.get_ident() != self._main_thread_id:
            self._ui_queue.put(("log", text))
            return
        self._apply_log(text)

    def _apply_log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    # ===== TIMER LOOP =====
    def _ui_loop(self):
        if not self.running:
            return

        while True:
            try:
                event, value = self._ui_queue.get_nowait()
            except queue.Empty:
                break

            if event == "status":
                self._apply_status(value)
            elif event == "log":
                self._apply_log(value)

        now = time.time()

        if self.monitoring_start:
            elapsed = int(now - self.monitoring_start)
            self.monitor_label.configure(text=f"Monitoring: {self._fmt(elapsed)}")
            self.progress.set((elapsed % 10) / 10)

        if self.recording_start:
            elapsed = int(now - self.recording_start)
            self.record_label.configure(text=f"Recording: {self._fmt(elapsed)}")

        self.after(1000, self._ui_loop)

    def _on_close(self):
        self.running = False
        try:
            self.stop_callback()
        except Exception:
            pass
        self.destroy()

    def _fmt(self, sec):
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        return f"{h:02}:{m:02}:{s:02}"
