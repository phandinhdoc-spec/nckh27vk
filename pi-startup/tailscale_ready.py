#!/usr/bin/env python3
"""Wait for an authenticated Tailscale connection before launching the app."""
import json
import subprocess
import time


def ready(status):
    return (status.get('BackendState') == 'Running'
            and bool(status.get('TailscaleIPs'))
            and status.get('Self', {}).get('Online') is True)


def main():
    while True:
        try:
            print('[tailscale] Running tailscale up (30 second limit)', flush=True)
            subprocess.run(['tailscale', 'up', '--timeout=30s'], check=True, timeout=40)
            result = subprocess.run(['tailscale', 'status', '--json'], check=True,
                                    capture_output=True, text=True, timeout=10)
            status = json.loads(result.stdout)
            if ready(status):
                print('[tailscale] Ready; starting /root/pi/app.py', flush=True)
                return
            print(f'[tailscale] Not ready: {status.get("BackendState")}; waiting', flush=True)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            print(f'[tailscale] {exc}. If login is required, run tailscale up via local SSH and open its link.', flush=True)
        time.sleep(15)


if __name__ == '__main__':
    main()
