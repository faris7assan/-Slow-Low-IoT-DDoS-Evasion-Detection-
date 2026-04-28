import streamlit as st
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from datetime import datetime
import glob
import signal
import sys

# Page setup
st.set_page_config(page_title="Red Team Load Test Dashboard", layout="wide", page_icon="🎯")

# Constants & Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)
LOCUST_FILE_PATH = os.path.join(BASE_DIR, "locustfile.py")

# Session state initialization
if 'test_running' not in st.session_state:
    st.session_state.test_running = False
if 'process_pid' not in st.session_state:
    st.session_state.process_pid = None
if 'current_prefix' not in st.session_state:
    st.session_state.current_prefix = None

def generate_locustfile(paths, min_wait, max_wait):
    """Generates a dynamic locustfile based on UI configurations."""
    paths_list = [p.strip() for p in paths.split(",") if p.strip()]
    tasks_code = ""
    for idx, path in enumerate(paths_list):
        # Using the actual path as the name helps group stats in Locust
        tasks_code += f"    @task\n    def task_{idx}(self):\n        self.client.get('{path}', name='{path}')\n"
        
    if not tasks_code:
        tasks_code = "    @task\n    def task_0(self):\n        self.client.get('/', name='/')\n"

    content = f"""# Automatically generated locustfile for Load Testing Dashboard
from locust import HttpUser, task, between

class DynamicLoadTester(HttpUser):
    # Think time: Simulate 'slow & low' behavior with randomized wait times
    wait_time = between({min_wait}, {max_wait})

{tasks_code}
"""
    with open(LOCUST_FILE_PATH, "w") as f:
        f.write(content)

def check_process_running(pid):
    """Check if a process is still running."""
    if pid is None:
        return False
    if os.name == 'nt':
        try:
            # Look for the exact PID in Windows tasklist
            output = subprocess.check_output(f'tasklist /FI "PID eq {pid}"', shell=True).decode()
            return str(pid) in output
        except Exception:
            return False
    else:
        try:
            # Sending signal 0 checks for process existence on Unix
            os.kill(pid, 0)
            return True
        except OSError:
            return False

def stop_process(pid):
    """Terminate the locust process safely across OS."""
    if not pid:
        return
    try:
        if os.name == 'nt':
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(pid)])
        else:
            os.kill(pid, signal.SIGTERM)
    except Exception as e:
        st.error(f"Error stopping process: {e}")

# -----------------
# Sidebar UI
# -----------------
st.sidebar.header("🎯 Load Test Config")
st.sidebar.markdown("Configure parameters for the headless Locust run.")

target_url = st.sidebar.text_input("Target URL", value="http://localhost:8000")
concurrent_users = st.sidebar.slider("Concurrent Users", min_value=1, max_value=200, value=50)
spawn_rate = st.sidebar.number_input("Spawn Rate (users/sec)", min_value=1, value=5)
duration = st.sidebar.number_input("Duration (seconds)", min_value=10, value=60)

st.sidebar.subheader("Think Time ('Slow & Low')")
col1, col2 = st.sidebar.columns(2)
with col1:
    min_wait = st.number_input("Min Wait (s)", min_value=0.0, value=1.0, step=0.1)
with col2:
    max_wait = st.number_input("Max Wait (s)", min_value=0.0, value=5.0, step=0.1)

paths_input = st.sidebar.text_area("Request Paths (comma-separated)", value="/,\n/api/data,\n/health")

# Controls
st.sidebar.markdown("---")
run_col, stop_col = st.sidebar.columns(2)
with run_col:
    start_btn = st.button("🚀 Run Test", disabled=st.session_state.test_running, use_container_width=True)
with stop_col:
    stop_btn = st.button("🛑 Stop Test", disabled=not st.session_state.test_running, use_container_width=True)

# -----------------
# Main UI
# -----------------
st.title("Red Team Authorized Load Testing Dashboard")
st.markdown("⚠️ **Disclaimer:** This tool is strictly for authorized testing on infrastructure you own or control. Do not use for malicious DDoS attacks.")

# Start Test Action
if start_btn:
    # 1. Prepare configuration
    generate_locustfile(paths_input, min_wait, max_wait)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = f"run_{timestamp}"
    full_prefix = os.path.join(RESULTS_DIR, prefix)
    
    # 2. Build CLI command
    cmd = [
        sys.executable, "-m", "locust",
        "-f", LOCUST_FILE_PATH,
        "--headless",
        "-u", str(concurrent_users),
        "-r", str(spawn_rate),
        "--run-time", f"{duration}s",
        "--host", target_url,
        "--csv", full_prefix
    ]
    
    # 3. Launch Subprocess
    try:
        if os.name == 'nt':
            # Create a new process group on Windows so we can kill the tree cleanly
            process = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            process = subprocess.Popen(cmd, preexec_fn=os.setsid)
            
        st.session_state.process_pid = process.pid
        st.session_state.test_running = True
        st.session_state.current_prefix = full_prefix
        st.rerun()
    except Exception as e:
        st.error(f"Failed to start load test: {e}")

# Stop Test Action
if stop_btn:
    if st.session_state.process_pid:
        stop_process(st.session_state.process_pid)
    st.session_state.test_running = False
    st.session_state.process_pid = None
    st.success("Test stopped manually.")
    st.rerun()

# Process Monitoring Loop
if st.session_state.test_running:
    if not check_process_running(st.session_state.process_pid):
        st.session_state.test_running = False
        st.session_state.process_pid = None
        st.success("Test completed successfully!")
        st.rerun()
    else:
        st.info("🔄 Test is currently running... The dashboard will refresh automatically.")
        time.sleep(3)
        st.rerun()

# -----------------
# Visualization Helpers
# -----------------
def plot_live_metrics(history_csv):
    try:
        df = pd.read_csv(history_csv)
        if df.empty:
            return
            
        # Locust aggregates total runs in rows named 'Aggregated'
        if 'Name' in df.columns and 'Aggregated' in df['Name'].values:
            df = df[df['Name'] == 'Aggregated'].copy()
            
        # Clean data and get timestamps
        df['Time'] = pd.to_datetime(df['Timestamp'], unit='s')
        
        st.markdown("### Performance Over Time")
        col1, col2 = st.columns(2)
        
        with col1:
            fig1, ax1 = plt.subplots(figsize=(8, 4))
            ax1.set_title('RPS vs Failures')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Requests / s', color='tab:blue')
            ax1.plot(df['Time'], df['Requests/s'], color='tab:blue', label='RPS', linewidth=2)
            ax1.tick_params(axis='y', labelcolor='tab:blue')
            
            # Create twin axis for failure rates
            ax2 = ax1.twinx()  
            ax2.set_ylabel('Failures / s', color='tab:red')  
            ax2.plot(df['Time'], df['Failures/s'], color='tab:red', label='Failures/s', linestyle='--')
            ax2.tick_params(axis='y', labelcolor='tab:red')
            
            fig1.tight_layout()  
            st.pyplot(fig1)
            plt.close(fig1)
            
        with col2:
            fig2, ax = plt.subplots(figsize=(8, 4))
            ax.set_title('Latency Percentiles (ms)')
            ax.set_xlabel('Time')
            ax.set_ylabel('Latency (ms)')
            
            # Plot standard percentiles
            if '50%' in df.columns:
                ax.plot(df['Time'], df['50%'], label='p50', color='green')
            if '95%' in df.columns:
                ax.plot(df['Time'], df['95%'], label='p95', color='orange')
            if '99%' in df.columns:
                ax.plot(df['Time'], df['99%'], label='p99', color='red')
            
            ax.legend(loc='upper left')
            fig2.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)
            
    except Exception as e:
        st.warning("Waiting for data to populate charts... (refreshing)")

def show_summary_metrics(stats_csv):
    try:
        df = pd.read_csv(stats_csv)
        if df.empty:
            return
            
        if 'Name' in df.columns and 'Aggregated' in df['Name'].values:
            agg = df[df['Name'] == 'Aggregated'].iloc[0]
            
            # Display high-level metrics
            cols = st.columns(4)
            cols[0].metric("Total Requests", f"{agg['Request Count']:,}")
            cols[1].metric("Total Failures", f"{agg['Failure Count']:,}")
            cols[2].metric("Median Latency", f"{agg['Median Response Time']:,} ms")
            cols[3].metric("Avg RPS", f"{round(agg['Requests/s'], 2)}")
            
            # Show per-endpoint breakdown
            st.markdown("### Endpoint Breakdown")
            endpoint_df = df[df['Name'] != 'Aggregated'][['Type', 'Name', 'Request Count', 'Failure Count', 'Median Response Time', 'Requests/s']]
            st.dataframe(endpoint_df, use_container_width=True)
            
    except Exception as e:
        pass

# -----------------
# Main View Tabs
# -----------------
tab_live, tab_compare = st.tabs(["📊 Live / Last Run", "🔍 Compare Past Runs"])

with tab_live:
    if st.session_state.current_prefix:
        history_csv = f"{st.session_state.current_prefix}_stats_history.csv"
        stats_csv = f"{st.session_state.current_prefix}_stats.csv"
        
        st.markdown(f"**Current Dataset:** `{os.path.basename(st.session_state.current_prefix)}`")
        
        if os.path.exists(stats_csv):
            show_summary_metrics(stats_csv)
            
        if os.path.exists(history_csv):
            plot_live_metrics(history_csv)
            
            # Download button for raw data
            with open(history_csv, "rb") as file:
                st.download_button(
                    label="💾 Download Timeseries Data (CSV)",
                    data=file,
                    file_name=f"{os.path.basename(history_csv)}",
                    mime="text/csv"
                )
    else:
        st.info("👈 Configure parameters on the left and click 'Run Test' to begin.")

with tab_compare:
    st.subheader("Compare Past Runs")
    all_runs = sorted(glob.glob(os.path.join(RESULTS_DIR, "*_stats_history.csv")), reverse=True)
    run_names = [os.path.basename(r).replace("_stats_history.csv", "") for r in all_runs]
    
    if len(run_names) >= 2:
        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            run1 = st.selectbox("Select Run A", run_names, index=0)
        with comp_col2:
            run2 = st.selectbox("Select Run B", run_names, index=1)
            
        if run1 and run2 and run1 != run2:
            try:
                df1 = pd.read_csv(os.path.join(RESULTS_DIR, f"{run1}_stats_history.csv"))
                df2 = pd.read_csv(os.path.join(RESULTS_DIR, f"{run2}_stats_history.csv"))
                
                if 'Name' in df1.columns: df1 = df1[df1['Name'] == 'Aggregated'].copy()
                if 'Name' in df2.columns: df2 = df2[df2['Name'] == 'Aggregated'].copy()
                
                # Normalize time to start at 0 for side-by-side comparison
                df1['Seconds Since Start'] = df1['Timestamp'] - df1['Timestamp'].min()
                df2['Seconds Since Start'] = df2['Timestamp'] - df2['Timestamp'].min()
                
                st.markdown("### Requests per Second (RPS) Comparison")
                fig_comp, ax_comp = plt.subplots(figsize=(10, 4))
                ax_comp.plot(df1['Seconds Since Start'], df1['Requests/s'], label=f"Run A ({run1})", color='tab:blue', linewidth=2)
                ax_comp.plot(df2['Seconds Since Start'], df2['Requests/s'], label=f"Run B ({run2})", color='tab:orange', linewidth=2)
                ax_comp.set_xlabel('Time (seconds from start)')
                ax_comp.set_ylabel('Requests / s')
                ax_comp.legend()
                ax_comp.grid(True, alpha=0.3)
                
                st.pyplot(fig_comp)
                plt.close(fig_comp)
            except Exception as e:
                st.error(f"Error rendering comparison: {e}")
        elif run1 == run2:
            st.warning("Please select two different runs to compare.")
    else:
        st.info("You need to complete at least 2 test runs to use the comparison feature.")
