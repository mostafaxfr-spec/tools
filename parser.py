import re
import csv

INPUT_FILE = "sessions.txt"

csv_out = []
userpass_set = set()
users = []
passwords = []

current = {}

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()

        if line.startswith("HostName:"):
            current["ip"] = line.split(":", 1)[1].strip()

        elif line.startswith("UserName:"):
            current["user"] = line.split(":", 1)[1].strip()

        elif line.startswith("Password:"):
            current["pass"] = line.split(":", 1)[1].strip()

            # Once password is found, we assume block is complete
            if {"ip", "user", "pass"} <= current.keys():
                ip = current["ip"]
                user = current["user"]
                pw = current["pass"]

                csv_out.append((ip, user, pw))
                userpass_set.add(f"{user}:{pw}")
                users.append(user)
                passwords.append(pw)

            current = {}

# 1️⃣ CSV: ip,username,password
with open("creds.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ip", "username", "password"])
    writer.writerows(csv_out)

# 2️⃣ username:password (sorted, unique)
with open("userpass.txt", "w") as f:
    for up in sorted(userpass_set):
        f.write(up + "\n")

# 3️⃣ users.txt
with open("users.txt", "w") as f:
    for u in users:
        f.write(u + "\n")

# 4️⃣ passwords.txt (row-corresponding)
with open("passwords.txt", "w") as f:
    for p in passwords:
        f.write(p + "\n")

print("[+] Extraction complete")
print(f"[+] creds.csv        ({len(csv_out)} entries)")
print(f"[+] userpass.txt     ({len(userpass_set)} unique)")
print(f"[+] users.txt / passwords.txt aligned")
