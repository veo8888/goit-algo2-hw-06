import json
import time
import sys
from hyperloglog import HyperLogLog

# Set UTF-8 encoding for console output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def load_ip_addresses(log_file_path):
    """
    Load IP addresses from log file.
    """
    ip_addresses = []

    with open(log_file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue

            try:
                log_entry = json.loads(line)
                ip = log_entry.get("remote_addr")

                if ip:
                    ip_addresses.append(ip)
            except json.JSONDecodeError:
                # Ignore invalid JSON lines
                continue
            except Exception as e:
                # Ignore other errors
                continue

    return ip_addresses


def count_unique_exact(ip_addresses):
    """
    Count unique IP addresses using exact method (set).
    """
    return len(set(ip_addresses))


def count_unique_hyperloglog(ip_addresses):
    """
    Count unique IP addresses using HyperLogLog algorithm.
    """
    hll = HyperLogLog(0.01)  # 1% error rate

    for ip in ip_addresses:
        hll.add(ip)

    return len(hll)


def compare_methods(log_file_path):
    """
    Compare exact counting and HyperLogLog methods.
    """
    print("Завантаження даних...")
    ip_addresses = load_ip_addresses(log_file_path)
    total_records = len(ip_addresses)
    print(f"Завантажені записи: {total_records}")

    # Exact counting
    print("\nТочний підрахунок...")
    start_time = time.time()
    exact_count = count_unique_exact(ip_addresses)
    exact_time = time.time() - start_time

    # HyperLogLog counting
    print("Кількість записів HyperLogLog...")
    start_time = time.time()
    hll_count = count_unique_hyperloglog(ip_addresses)
    hll_time = time.time() - start_time

    # Calculate error
    error_absolute = abs(exact_count - hll_count)
    error_percent = (error_absolute / exact_count * 100) if exact_count > 0 else 0

    # Display results
    print("\nРезультати порівняння:")
    print(f"{'':30} {'Точний підрахунок':>20} {'HyperLogLog':>20}")
    print(f"{'Унікальні елементи':30} {exact_count:>20.1f} {hll_count:>20.1f}")
    print(f"{'Час виконання (сек.)':30} {exact_time:>20.2f} {hll_time:>20.2f}")
    print(f"\nПохибка: {error_absolute} ({error_percent:.2f}%)")
    print(f"Прискорення: {exact_time/hll_time:.2f}x" if hll_time > 0 else "N/A")


if __name__ == "__main__":
    log_file = "lms-stage-access.log"
    compare_methods(log_file)
