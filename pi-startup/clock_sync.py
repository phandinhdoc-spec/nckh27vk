#!/usr/bin/env python3
"""Boot-time SNTP bootstrap, independent of D-Bus and TLS clock validation."""
import itertools
import os
import socket
import struct
import subprocess
import sys
import time

EPOCH = 2208988800
# Public Cloudflare addresses let bootstrap work before DNS/Tailscale is up.
SERVERS = ('162.159.200.1', '162.159.200.123', '0.pool.ntp.org', '1.pool.ntp.org')


def decode_reply(packet, token, elapsed):
    if len(packet) < 48:
        raise ValueError('Short NTP reply')
    if packet[0] >> 6 == 3 or (packet[0] & 7) != 4 or ((packet[0] >> 3) & 7) not in (3, 4):
        raise ValueError('Unsynchronized server or invalid NTP mode/version')
    if not 1 <= packet[1] <= 15 or packet[24:32] != token:
        raise ValueError('NTP stratum/origin mismatch')
    seconds, fraction = struct.unpack('!II', packet[40:48])
    if seconds == 0 and fraction == 0:
        raise ValueError('Missing server timestamp')
    epoch = seconds - EPOCH + fraction / 2**32
    # Support the 2036 era rollover without trusting the Pi's broken clock.
    if epoch < 1704067200:
        epoch += 2**32
    if not 1704067200 <= epoch < 4102444800 or not 0 <= elapsed <= 4:
        raise ValueError('Implausible time or excessive latency')
    return epoch + elapsed / 2


def query(server):
    # The first address is sufficient; retry other providers on failure.
    family, kind, proto, _, address = socket.getaddrinfo(server, 123, type=socket.SOCK_DGRAM)[0]
    with socket.socket(family, kind, proto) as sock:
        sock.settimeout(4)
        sock.connect(address)  # Filter replies to the selected endpoint.
        packet = bytearray(48)
        packet[0] = 0x23  # Version 4, client mode.
        token = struct.pack('!I', (int(time.time()) + EPOCH) & 0xffffffff) + os.urandom(4)
        packet[40:48] = token
        start = time.monotonic()
        sock.send(packet)
        reply = sock.recv(512)
        received = time.monotonic()
        return decode_reply(reply, token, received - start), received


def consensus(samples, now):
    adjusted = [stamp + now - received for stamp, received in samples]
    for a, b in itertools.combinations(adjusted, 2):
        if abs(a - b) <= 3:
            return (a + b) / 2
    raise ValueError('Need two NTP servers agreeing within 3 seconds')


def attempt():
    samples = []
    for server in SERVERS:
        try:
            samples.append(query(server))
            try:
                consensus(samples, time.monotonic())
                break
            except ValueError:
                pass
        except (OSError, ValueError) as exc:
            print(f'[clock] {server}: {exc}', flush=True)
    stamp = consensus(samples, time.monotonic())
    subprocess.run(['/usr/bin/date', '-u', '-s', f'@{stamp:.3f}'], check=True, timeout=10)
    print('[clock] Network time set using date; allowing tailscaled to start.', flush=True)


def main():
    if os.geteuid() != 0:
        sys.exit('Run as root to set the system clock')
    while True:
        try:
            attempt()
            return
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            print(f'[clock] Waiting for network time: {exc}; retry in 15 seconds', flush=True)
            time.sleep(15)


if __name__ == '__main__':
    main()
