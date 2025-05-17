import re
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def parse_log(log_file):
    timestamps = []
    mem_data = {'total': [], 'free': [], 'used': [], 'buff/cache': []}
    swap_data = {'total': [], 'free': [], 'used': [], 'avail': []}
    script_data_1 = {'cpu': [], 'mem': []}  # For PID 5368
    script_data_2 = {'cpu': [], 'mem': []}  # For PID 5369
    top5_pids = []
    top5_commands = {}

    with open(log_file, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Parsing timestamp
        if line.startswith('Timestamp:'):
            timestamp_str = line.split('Timestamp: ')[1]
            try:
                timestamps.append(datetime.strptime(timestamp_str, '%a %b %d %I:%M:%S %p %Z %Y'))
            except ValueError:
                print(f"Warning: Could not parse timestamp: {timestamp_str}")
            i += 1
            continue

        # Parsing Memory Info
        if line == 'Memory Info:':
            i += 1
            mem_line = lines[i].strip()
            mem_match = re.match(
                r'MiB Mem :\s+(\d+\.\d)\s+total,\s+(\d+\.\d)\s+free,\s+(\d+\.\d)\s+used,\s+(\d+\.\d)\s+buff/cache',
                mem_line)
            if mem_match:
                mem_data['total'].append(float(mem_match.group(1)))
                mem_data['free'].append(float(mem_match.group(2)))
                mem_data['used'].append(float(mem_match.group(3)))
                mem_data['buff/cache'].append(float(mem_match.group(4)))
            else:
                print(f"Warning: Could not parse memory line: {mem_line}")
            i += 1
            swap_line = lines[i].strip()
            swap_match = re.match(
                r'MiB Swap:\s+(\d+\.\d)\s+total,\s+(\d+\.\d)\s+free,\s+(\d+\.\d)\s+used\.\s+(\d+\.\d)\s+avail Mem',
                swap_line)
            if swap_match:
                swap_data['total'].append(float(swap_match.group(1)))
                swap_data['free'].append(float(swap_match.group(2)))
                swap_data['used'].append(float(swap_match.group(3)))
                swap_data['avail'].append(float(swap_match.group(4)))
            else:
                print(f"Warning: Could not parse swap line: {swap_line}")
            i += 1
            continue

        # Parsing Script Process (PID 5368)
        if line.startswith('Script Process (PID 5368):'):
            i += 1
            script_line = lines[i].strip()
            script_match = re.search(r'^\s*5368\s+\w+\s+\d+\s+\d+\s+\d+\s+\S+\s+\d+\s+\w+\s+(\d+\.\d)\s+(\d+\.\d)',
                                     script_line)
            if script_match:
                script_data_1['cpu'].append(float(script_match.group(1)))
                script_data_1['mem'].append(float(script_match.group(2)))
            else:
                print(f"Warning: Could not parse script process (PID 5368) line: {script_line}")
                script_data_1['cpu'].append(0.0)
                script_data_1['mem'].append(0.0)
            i += 1
            continue

        # Parsing Script Process (PID 5369)
        if line.startswith('Script Process (PID 5369):'):
            i += 1
            script_line = lines[i].strip()
            script_match = re.search(r'^\s*5369\s+\w+\s+\d+\s+\d+\s+\d+\s+\S+\s+\d+\s+\w+\s+(\d+\.\d)\s+(\d+\.\d)',
                                     script_line)
            if script_match:
                script_data_2['cpu'].append(float(script_match.group(1)))
                script_data_2['mem'].append(float(script_match.group(2)))
            else:
                print(f"Warning: Could not parse script process (PID 5369) line: {script_line}")
                script_data_2['cpu'].append(0.0)
                script_data_2['mem'].append(0.0)
            i += 1
            continue

        # Parsing Top 5 Processes
        if line == 'Top 5 Processes:':
            current_top5 = []
            i += 1
            while i < len(lines) and lines[i].startswith('PID:'):
                pid_cmd = re.match(r'PID: (\d+), Command: (.+)', lines[i].strip())
                if pid_cmd:
                    pid, cmd = pid_cmd.group(1), pid_cmd.group(2)
                    current_top5.append((pid, cmd))
                    top5_commands.setdefault(pid, cmd)
                else:
                    print(f"Warning: Could not parse top 5 line: {lines[i].strip()}")
                i += 1
            top5_pids.append(current_top5)
            continue

        i += 1

    return timestamps, mem_data, swap_data, script_data_1, script_data_2, top5_pids, top5_commands


def plot_memory(timestamps, mem_data, swap_data):
    if not timestamps:
        print("No data to plot for memory/swap")
        return
    plt.figure(figsize=(12, 8))

    # Memory plot
    plt.subplot(2, 1, 1)
    plt.plot(timestamps, mem_data['total'], label='Total Mem (MiB)')
    plt.plot(timestamps, mem_data['free'], label='Free Mem (MiB)')
    plt.plot(timestamps, mem_data['used'], label='Used Mem (MiB)')
    plt.plot(timestamps, mem_data['buff/cache'], label='Buff/Cache (MiB)')
    plt.title('Memory Usage Over Time')
    plt.xlabel('Time')
    plt.ylabel('Memory (MiB)')
    plt.legend()
    plt.grid(True)

    # Swap plot
    plt.subplot(2, 1, 2)
    plt.plot(timestamps, swap_data['total'], label='Total Swap (MiB)')
    plt.plot(timestamps, swap_data['free'], label='Free Swap (MiB)')
    plt.plot(timestamps, swap_data['used'], label='Used Swap (MiB)')
    plt.plot(timestamps, swap_data['avail'], label='Avail Mem (MiB)')
    plt.title('Swap Usage Over Time')
    plt.xlabel('Time')
    plt.ylabel('Swap (MiB)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('memory_swap_usage.png')
    plt.close()


def plot_script_processes(timestamps, script_data_1, script_data_2):
    if not timestamps or not script_data_1['cpu'] or not script_data_2['cpu']:
        print("No data to plot for script processes")
        return
    plt.figure(figsize=(12, 8))

    # Process 1 (PID 5368)
    plt.subplot(2, 1, 1)
    plt.plot(timestamps, script_data_1['cpu'], label='%CPU (PID 5368)')
    plt.plot(timestamps, script_data_1['mem'], label='%MEM (PID 5368)')
    plt.title('Process mem.bash (PID 5368) Usage Over Time')
    plt.xlabel('Time')
    plt.ylabel('Percentage')
    plt.legend()
    plt.grid(True)

    # Process 2 (PID 5369)
    plt.subplot(2, 1, 2)
    plt.plot(timestamps, script_data_2['cpu'], label='%CPU (PID 5369)')
    plt.plot(timestamps, script_data_2['mem'], label='%MEM (PID 5369)')
    plt.title('Process mem2.ba+ (PID 5369) Usage Over Time')
    plt.xlabel('Time')
    plt.ylabel('Percentage')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('script_processes_usage.png')
    plt.close()


def plot_top5_processes(timestamps, top5_pids, top5_commands):
    if not timestamps or not top5_pids:
        print("No data to plot for top 5 processes")
        return
    plt.figure(figsize=(12, 6))

    # Creating a matrix for process rank (5 for Top 1, 1 for Top 5, 0 for absent)
    unique_pids = list(top5_commands.keys())
    presence = np.zeros((len(unique_pids), len(timestamps)))

    for t_idx, top5 in enumerate(top5_pids):
        for rank, (pid, _) in enumerate(top5, 1):
            if pid in unique_pids:
                p_idx = unique_pids.index(pid)
                presence[p_idx, t_idx] = 6 - rank  # 5 for Top 1, 4 for Top 2, ..., 1 for Top 5

    # Plotting heatmap with custom colormap
    plt.imshow(presence, cmap='Blues', aspect='auto', vmin=0, vmax=5)
    cbar = plt.colorbar(label='Top Position')
    cbar.set_ticks([0, 1, 2, 3, 4, 5])
    cbar.set_label('Top Position (5=Top 1, 1=Top 5)')
    plt.yticks(range(len(unique_pids)), [f"{pid} ({top5_commands[pid]})" for pid in unique_pids])
    plt.xticks(range(len(timestamps)), [t.strftime('%H:%M:%S') for t in timestamps], rotation=45)
    plt.title('Top 5 Processes Rank Over Time')
    plt.xlabel('Time')
    plt.ylabel('PID (Command)')

    plt.tight_layout()
    plt.savefig('top5_processes.png')
    plt.close()


def main():
    log_file = 'logs/top_monitor2.log'
    timestamps, mem_data, swap_data, script_data_1, script_data_2, top5_pids, top5_commands = parse_log(log_file)

    if not timestamps:
        print("Error: No valid data parsed from log file")
        return

    # Plotting
    plot_memory(timestamps, mem_data, swap_data)
    plot_script_processes(timestamps, script_data_1, script_data_2)
    plot_top5_processes(timestamps, top5_pids, top5_commands)
    print("Graphs saved as 'memory_swap_usage.png', 'script_processes_usage.png', and 'top5_processes.png'")


if __name__ == '__main__':
    main()