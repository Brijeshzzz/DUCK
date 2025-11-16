import os
import subprocess

LOGS_DIR = "part_a/logs"
TOR_PORTS = [9001, 9002, 9050, 9051, 9030]

def find_latest_capture():
    files = [f for f in os.listdir(LOGS_DIR) if f.endswith(".pcap")]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(LOGS_DIR, x)), reverse=True)
    return os.path.join(LOGS_DIR, files[0]) if files else None

def analyze_capture(pcap_file):
    print(f"Analyzing pcap file: {pcap_file}")
    print(f"File size: {os.path.getsize(pcap_file)} bytes")

def analyze_tor_ports_and_lengths(pcap_file):
    print("\\nTor port and length analysis:")

    port_filter = " or ".join([f"tcp.port=={port}" for port in TOR_PORTS])
    cmd = [
        "tshark",
        "-r", pcap_file,
        "-Y", port_filter,
        "-T", "fields",
        "-e", "frame.number",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "tcp.srcport",
        "-e", "tcp.dstport",
        "-e", "frame.len"
    ]

    print("Checking for Tor-related ports in packets...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.strip().split("\\n")
    port_hits = len(lines)
    print(f"Packets to Tor-related ports: {port_hits}")

    lengths = [int(l.split('\\t')[-1]) for l in lines if l and l.split('\\t')[-1].isdigit()]
    cell_count = lengths.count(512)
    total_count = len(lengths)
    if total_count > 0:
        percent_cells = 100 * cell_count / total_count
        print(f"512-byte Tor cell packets: {cell_count}/{total_count} ({percent_cells:.2f}%)")
    else:
        print("No packets found for Tor relay ports.")

if __name__ == "__main__":
    pcap = find_latest_capture()
    if pcap:
        analyze_capture(pcap)
        analyze_tor_ports_and_lengths(pcap)
    else:
        print("No pcap file found in logs.")
