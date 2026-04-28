import os
import sys
import time
import subprocess
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    print("Pandas is required. Please run: pip install pandas")
    sys.exit(1)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_locustfile(paths_list, min_wait, max_wait):
    """Generates the locustfile dynamically based on inputs."""
    tasks_code = ""
    for idx, path in enumerate(paths_list):
        tasks_code += f"    @task\n    def task_{idx}(self):\n        self.client.get('{path}', name='{path}')\n"
        
    if not tasks_code:
        tasks_code = "    @task\n    def task_0(self):\n        self.client.get('/', name='/')\n"

    content = f"""from locust import HttpUser, task, between

class DynamicLoadTester(HttpUser):
    # Think time: Simulate 'slow & low' behavior
    wait_time = between({min_wait}, {max_wait})

{tasks_code}
"""
    with open("locustfile.py", "w") as f:
        f.write(content)

def run_cli_dashboard():
    clear_screen()
    print("======================================================")
    print("       🎯 RED TEAM CLI LOAD TESTING DASHBOARD         ")
    print("======================================================")
    
    # Prompt for configuration
    target_url = input("Target URL [http://localhost:8000]: ").strip() or "http://localhost:8000"
    users = input("Concurrent Users [50]: ").strip() or "50"
    spawn_rate = input("Spawn Rate (users/sec) [5]: ").strip() or "5"
    duration = input("Duration in seconds [60]: ").strip() or "60"
    min_w = input("Min wait time (s) [1.0]: ").strip() or "1.0"
    max_w = input("Max wait time (s) [5.0]: ").strip() or "5.0"
    paths = input("Paths (comma separated) [/]: ").strip() or "/"

    paths_list = [p.strip() for p in paths.split(",") if p.strip()]
    
    # Generate locustfile locally
    generate_locustfile(paths_list, float(min_w), float(max_w))
    
    # Prepare results directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = os.path.join(RESULTS_DIR, f"run_{timestamp}")
    
    # Check if locust is installed before running
    try:
        import locust
    except ImportError:
        print("\n❌ Error: Locust is not installed in this Python environment.")
        print("Please install it by running: sys.executable -m pip install locust")
        sys.exit(1)
        
    # Build subprocess command
    cmd = [
        sys.executable, "-m", "locust",
        "-f", "locustfile.py",
        "--headless",
        "-u", users,
        "-r", spawn_rate,
        "--run-time", f"{duration}s",
        "--host", target_url,
        "--csv", prefix
    ]
    
    print("\n🚀 Starting Background Load Test...")
    time.sleep(1)
    
    # Hide locust standard output to render our own UI
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    history_csv = f"{prefix}_stats_history.csv"
    start_time = time.time()
    
    try:
        while process.poll() is None:
            time.sleep(2)
            if not os.path.exists(history_csv):
                continue
                
            try:
                # Read live stats
                df = pd.read_csv(history_csv)
                if df.empty: 
                    continue
                    
                if 'Name' in df.columns and 'Aggregated' in df['Name'].values:
                    df = df[df['Name'] == 'Aggregated']
                
                if df.empty: 
                    continue
                
                latest = df.iloc[-1]
                
                # Render UI
                clear_screen()
                elapsed = int(time.time() - start_time)
                print("======================================================")
                print(f" 🎯 LIVE METRICS - Target: {target_url}")
                print(f" ⏳ Time Elapsed: {elapsed}s / {duration}s")
                print("======================================================")
                print(f" 👥 Active Users  : {latest.get('User Count', 0)}")
                print(f" 🚀 Requests / s  : {latest.get('Requests/s', 0):.2f}")
                print(f" ❌ Failures / s  : {latest.get('Failures/s', 0):.2f}")
                print("------------------------------------------------------")
                print(" ⏱️  Latency Percentiles (ms)")
                print(f"    p50 (Median)  : {latest.get('50%', 0)}")
                print(f"    p95           : {latest.get('95%', 0)}")
                print(f"    p99           : {latest.get('99%', 0)}")
                print("======================================================")
                print("Press Ctrl+C to stop early.")
            except Exception:
                pass
                
        # Final output
        clear_screen()
        print("======================================================")
        print(" ✅ TEST COMPLETED SUCCESSFULLY!")
        print("======================================================")
        print(f" 📁 Results saved in : {prefix}_stats.csv")
        print("======================================================")
        
    except KeyboardInterrupt:
        clear_screen()
        print("\n🛑 Test Stopped Manually by User.")
        if os.name == 'nt':
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            process.terminate()

if __name__ == "__main__":
    run_cli_dashboard()
