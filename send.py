#!/usr/bin/env python3
import socket
import sys
import os

def send_exe(host, port, exe_path):
    if not os.path.exists(exe_path):
        print(f"[-] File not found: {exe_path}")
        return False

    file_size = os.path.getsize(exe_path)
    print(f"[+] EXE size: {file_size} bytes")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Send file size as raw 4-byte little-endian
        sock.sendall(file_size.to_bytes(4, byteorder='little'))

        # Send the EXE in chunks
        with open(exe_path, 'rb') as f:
            sent = 0
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                sock.sendall(chunk)
                sent += len(chunk)
                print(f"\r[+] Sent {sent}/{file_size} bytes", end='')
        print("\n[+] Transfer complete")
        sock.close()
        return True

    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <target_ip> <port> <exe_file>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    exe_path = sys.argv[3]

    if send_exe(host, port, exe_path):
        print("[+] Sender finished.")
    else:
        print("[-] Sender failed.")
