import os
import sys
import subprocess
import time
import threading
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# --- Styling Constants ---
BG_COLOR = "#0f172a"  # Dark Slate Blue
CARD_COLOR = "#1e293b"
ACCENT_COLOR = "#38bdf8" # Sky Blue
TEXT_COLOR = "#f8fafc"
SUCCESS_COLOR = "#4ade80"
ERROR_COLOR = "#f87171"

class RedTeamDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("RED TEAM - DDoS Stealth Testing Dashboard")
        self.root.geometry("1100x750")
        self.root.configure(bg=BG_COLOR)
        
        self.test_running = False
        self.process = None
        self.current_prefix = None
        self.start_time = 0
        
        # Paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.results_dir = os.path.join(self.base_dir, "results")
        os.makedirs(self.results_dir, exist_ok=True)
        self.locustfile_path = os.path.join(self.base_dir, "temp_locustfile.py")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG_COLOR, height=60)
        header.pack(fill="x", padx=20, pady=10)
        
        title_label = tk.Label(header, text="🎯 RED TEAM PRO: DDOS EMULATION", 
                             font=("Segoe UI", 20, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR)
        title_label.pack(side="left")
        
        self.status_indicator = tk.Label(header, text="● IDLE", font=("Segoe UI", 12, "bold"), 
                                       bg=BG_COLOR, fg="#64748b")
        self.status_indicator.pack(side="right", pady=10)
        
        # Main Layout: Left Config | Right Metrics
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # --- LEFT: Config Panel ---
        left_panel = tk.Frame(main_frame, bg=CARD_COLOR, width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 10), pady=10)
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="CONFIGURATION", font=("Segoe UI", 12, "bold"), 
                 bg=CARD_COLOR, fg=TEXT_COLOR).pack(pady=15)
        
        # Helper for input fields
        def create_input(label_text, default_val):
            frame = tk.Frame(left_panel, bg=CARD_COLOR)
            frame.pack(fill="x", padx=15, pady=5)
            tk.Label(frame, text=label_text, font=("Segoe UI", 9), bg=CARD_COLOR, fg="#94a3b8").pack(anchor="w")
            entry = tk.Entry(frame, font=("Segoe UI", 10), bg="#0f172a", fg="white", 
                            insertbackground="white", borderwidth=0)
            entry.insert(0, default_val)
            entry.pack(fill="x", pady=2)
            return entry

        self.ent_target = create_input("Target URL", "http://localhost:8000")
        self.ent_users = create_input("Concurrent Users", "50")
        self.ent_spawn = create_input("Spawn Rate", "5")
        self.ent_duration = create_input("Duration (seconds)", "60")
        
        tk.Label(left_panel, text="Think Time (Slow & Low)", font=("Segoe UI", 9, "bold"), 
                 bg=CARD_COLOR, fg=ACCENT_COLOR).pack(pady=(15, 5))
        
        wait_frame = tk.Frame(left_panel, bg=CARD_COLOR)
        wait_frame.pack(fill="x", padx=15)
        
        self.ent_min_wait = tk.Entry(wait_frame, width=10, bg="#0f172a", fg="white", borderwidth=0)
        self.ent_min_wait.insert(0, "1.0")
        self.ent_min_wait.pack(side="left", padx=2)
        tk.Label(wait_frame, text="to", bg=CARD_COLOR, fg="white").pack(side="left")
        self.ent_max_wait = tk.Entry(wait_frame, width=10, bg="#0f172a", fg="white", borderwidth=0)
        self.ent_max_wait.insert(0, "5.0")
        self.ent_max_wait.pack(side="left", padx=2)
        
        # Buttons
        self.btn_run = tk.Button(left_panel, text="🚀 START ATTACK", command=self.start_attack,
                               bg=ACCENT_COLOR, fg=BG_COLOR, font=("Segoe UI", 11, "bold"),
                               borderwidth=0, cursor="hand2", activebackground="#7dd3fc")
        self.btn_run.pack(fill="x", padx=15, pady=30)
        
        self.btn_stop = tk.Button(left_panel, text="🛑 STOP", command=self.stop_attack,
                                bg="#ef4444", fg="white", font=("Segoe UI", 11, "bold"),
                                borderwidth=0, cursor="hand2", state="disabled")
        self.btn_stop.pack(fill="x", padx=15, pady=0)
        
        # --- RIGHT: Dashboard ---
        right_panel = tk.Frame(main_frame, bg=BG_COLOR)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Top Metrics Cards
        metrics_frame = tk.Frame(right_panel, bg=BG_COLOR)
        metrics_frame.pack(fill="x", pady=10)
        
        def create_metric_card(parent, label):
            card = tk.Frame(parent, bg=CARD_COLOR, padx=20, pady=15)
            card.pack(side="left", fill="both", expand=True, padx=5)
            tk.Label(card, text=label, font=("Segoe UI", 9), bg=CARD_COLOR, fg="#94a3b8").pack()
            val_label = tk.Label(card, text="0", font=("Segoe UI", 20, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR)
            val_label.pack()
            return val_label

        self.lbl_rps = create_metric_card(metrics_frame, "REQUESTS / SEC")
        self.lbl_failures = create_metric_card(metrics_frame, "FAILURES / SEC")
        self.lbl_latency = create_metric_card(metrics_frame, "P95 LATENCY (ms)")
        self.lbl_time = create_metric_card(metrics_frame, "ELAPSED TIME")
        
        # Graph Area
        self.graph_frame = tk.Frame(right_panel, bg=CARD_COLOR)
        self.graph_frame.pack(fill="both", expand=True, padx=5, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 3), facecolor=CARD_COLOR)
        self.ax.set_facecolor(CARD_COLOR)
        self.ax.tick_params(colors=TEXT_COLOR)
        for spine in self.ax.spines.values():
            spine.set_color('#475569')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Log Area
        self.log_text = tk.Text(right_panel, height=6, bg="#020617", fg="#94a3b8", 
                              font=("Consolas", 9), borderwidth=0, padx=10, pady=10)
        self.log_text.pack(fill="x", padx=5, pady=5)
        self.log("System ready. Configure targets and press START.")

    def log(self, message):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{ts}] {message}\n")
        self.log_text.see(tk.END)

    def generate_locustfile(self):
        content = f"""from locust import HttpUser, task, between
class DynamicLoadTester(HttpUser):
    wait_time = between({self.ent_min_wait.get()}, {self.ent_max_wait.get()})
    @task
    def test_target(self):
        self.client.get("/", name="root")
"""
        with open(self.locustfile_path, "w") as f:
            f.write(content)

    def start_attack(self):
        if self.test_running: return
        
        try:
            self.generate_locustfile()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_prefix = os.path.join(self.results_dir, f"run_{timestamp}")
            
            cmd = [
                sys.executable, "-m", "locust",
                "-f", self.locustfile_path,
                "--headless",
                "-u", self.ent_users.get(),
                "-r", self.ent_spawn.get(),
                "--run-time", f"{self.ent_duration.get()}s",
                "--host", self.ent_target.get(),
                "--csv", self.current_prefix
            ]
            
            self.log(f"Launching attack on {self.ent_target.get()}...")
            self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            self.test_running = True
            self.start_time = time.time()
            self.btn_run.config(state="disabled")
            self.btn_stop.config(state="normal")
            self.status_indicator.config(text="● ATTACKING", fg=ERROR_COLOR)
            
            # Start monitor thread
            threading.Thread(target=self.monitor_process, daemon=True).start()
            self.update_ui_loop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start: {e}")
            self.log(f"ERROR: {e}")

    def stop_attack(self):
        if not self.test_running: return
        self.log("Stopping attack...")
        if self.process:
            if os.name == 'nt':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                self.process.terminate()
        self.test_running = False
        self.btn_run.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.status_indicator.config(text="● STOPPED", fg="#94a3b8")

    def monitor_process(self):
        while self.process and self.process.poll() is None:
            time.sleep(1)
        if self.test_running:
            self.root.after(0, self.finish_test)

    def finish_test(self):
        self.test_running = False
        self.log("Test completed successfully.")
        self.btn_run.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.status_indicator.config(text="● COMPLETED", fg=SUCCESS_COLOR)

    def update_ui_loop(self):
        if not self.test_running: return
        
        history_csv = f"{self.current_prefix}_stats_history.csv"
        if os.path.exists(history_csv):
            try:
                df = pd.read_csv(history_csv)
                if not df.empty:
                    if 'Name' in df.columns:
                        df = df[df['Name'] == 'Aggregated']
                    
                    if not df.empty:
                        latest = df.iloc[-1]
                        self.lbl_rps.config(text=f"{latest.get('Requests/s', 0):.2f}")
                        self.lbl_failures.config(text=f"{latest.get('Failures/s', 0):.2f}")
                        self.lbl_latency.config(text=f"{latest.get('95%', 0)}")
                        
                        elapsed = int(time.time() - self.start_time)
                        self.lbl_time.config(text=f"{elapsed}s")
                        
                        # Update Graph
                        self.ax.clear()
                        self.ax.set_facecolor(CARD_COLOR)
                        self.ax.plot(df.index, df['Requests/s'], color=ACCENT_COLOR, linewidth=2)
                        self.ax.set_title("Live Requests per Second", color=TEXT_COLOR, fontsize=10)
                        self.ax.grid(True, alpha=0.1)
                        self.canvas.draw()
            except Exception:
                pass
        
        self.root.after(2000, self.update_ui_loop)

if __name__ == "__main__":
    # Check for dependencies
    missing = []
    try: import pandas as pd
    except ImportError: missing.append("pandas")
    try: import matplotlib
    except ImportError: missing.append("matplotlib")
    try: import locust
    except ImportError: missing.append("locust")
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Please run: pip install pandas matplotlib locust")
        sys.exit(1)

    root = tk.Tk()
    app = RedTeamDashboard(root)
    root.mainloop()
