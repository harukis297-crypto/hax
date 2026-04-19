import multiprocessing
import itertools

base_words = [
    "admin", "root", "user", "guest", "test",
    "password", "pass", "login", "system",
    "manager", "support", "master", "queen",
    "hacker", "dark", "devil", "kali", "linux",
    "alone", "boy", "girl"
]

names = [
    "rahul", "aman", "rohit", "raj",
    "sonu", "vikas", "deepak", "ankit"
]

numbers = ["1","12","123","1234","72","721","2024","2025"]
symbols = ["", "@", "#", "$", "%", "_", "/"]

LIMIT = 2_000_000  # control size


def worker(words, wid):
    count = 0
    filename = f"pass_part_{wid}.txt"

    with open(filename, "w") as f:

        # 🔹 1-word combos
        for word in words:
            for num in numbers:
                for sym in symbols:
                    p = word + sym + num
                    f.write(p + "\n")
                    count += 1

                    if count >= LIMIT:
                        break
                if count >= LIMIT:
                    break
            if count >= LIMIT:
                break

        # 🔹 2-word combos (important)
        for w1, w2 in itertools.product(words, repeat=2):
            combo = w1 + w2

            for num in numbers:
                for sym in symbols:
                    p = combo + sym + num
                    f.write(p + "\n")
                    count += 1

                    if count >= LIMIT:
                        break
                if count >= LIMIT:
                    break
            if count >= LIMIT:
                break

    print(f"[Worker {wid}] Done ({count} passwords)")


def main():
    all_words = base_words + names
    cpu = multiprocessing.cpu_count()

    chunk_size = len(all_words) // cpu + 1
    chunks = [all_words[i:i + chunk_size] for i in range(0, len(all_words), chunk_size)]

    processes = []

    for i, chunk in enumerate(chunks):
        p = multiprocessing.Process(target=worker, args=(chunk, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("\n✅ SMART GENERATION COMPLETE")
    print("📁 Files: pass_part_*.txt")


if __name__ == "__main__":
    main()
