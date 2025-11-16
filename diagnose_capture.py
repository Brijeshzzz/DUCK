import os
import sys
import subprocess

def check_capture_py():
    script = "part_a/network_capture/capture.py"

    # 1. Does the file exist?
    if not os.path.isfile(script):
        print(f"ERROR: {script} does not exist.")
        return

    # 2. Print first 20 lines for debugging
    with open(script, "r") as f:
        lines = [next(f) for _ in range(20)]
    print("First 20 lines of capture.py:")
    print("-------------------------------")
    for line in lines:
        print(line.rstrip())
    print("-------------------------------")

    # 3. Try running script, checking duration
    try:
        print("Running capture.py standalone (timeout 60s)...")
        result = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=60)
        print("Return code:", result.returncode)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        if result.returncode != 0:
            print("ERROR: Script exited with an error. See above.")
        else:
            print("SUCCESS: Script completed.")
    except subprocess.TimeoutExpired:
        print("ERROR: capture.py timed out after 60 seconds. Likely duration is set too high or waiting for packets.")
    except Exception as e:
        print(f"ERROR: Exception while running capture.py: {e}")
    print("- End diagnostic -")

if __name__ == "__main__":
    check_capture_py()
