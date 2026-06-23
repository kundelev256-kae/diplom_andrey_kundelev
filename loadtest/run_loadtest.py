import subprocess
import sys
import os
import json
import time

RESULTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loadtest_results.json")


def run_locust_test(users=10, spawn_rate=2, run_time="30s"):
    locustfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locustfile.py")

    cmd = [
        sys.executable, "-m", "locust",
        "-f", locustfile,
        "--headless",
        "-u", str(users),
        "-r", str(spawn_rate),
        "--run-time", run_time,
        "--host", "https://itstep.by",
        "--only-summary",
        "--csv=loadtest_results",
    ]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__)),
        env=env,
    )

    stdout, stderr = process.communicate(timeout=120)
    return stdout.decode("utf-8", errors="replace"), stderr.decode("utf-8", errors="replace"), process.returncode


def get_results():
    stats_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loadtest_results_stats.csv")

    if not os.path.exists(stats_file):
        return None

    for encoding in ["utf-8", "utf-8-sig", "cp1251", "latin-1"]:
        try:
            with open(stats_file, "r", encoding=encoding) as f:
                lines = f.readlines()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    else:
        return None

    if len(lines) < 2:
        return None

    headers = lines[0].strip().split(",")

    aggregated_line = None
    for line in lines[1:]:
        if "Aggregated" in line:
            aggregated_line = line.strip().split(",")
            break

    if not aggregated_line:
        aggregated_line = lines[-1].strip().split(",")

    results = {}
    for i, header in enumerate(headers):
        if i < len(aggregated_line):
            results[header.strip()] = aggregated_line[i].strip()

    return results


def format_results(raw_output, stats):
    report_lines = []
    report_lines.append("=" * 50)
    report_lines.append("ОТЧЕТ ПО НАГРУЗОЧНОМУ ТЕСТИРОВАНИЮ")
    report_lines.append("=" * 50)
    report_lines.append(f"Цель: https://itstep.by")
    report_lines.append(f"Дата: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    if stats:
        report_lines.append("СТАТИСТИКА:")
        report_lines.append("-" * 50)

        stat_map = {}
        for key, value in stats.items():
            stat_map[key.lower().strip()] = value

        stat_names = {
            "request count": "Всего запросов",
            "failure count": "Неудачных запросов",
            "median response time": "Медианное время (мс)",
            "average response time": "Среднее время (мс)",
            "min response time": "Мин. время (мс)",
            "max response time": "Макс. время (мс)",
            "average size": "Ср. размер ответа (байт)",
            "requests/s": "Запросов/сек",
        }

        for key, label in stat_names.items():
            for stat_key, stat_value in stat_map.items():
                if key in stat_key:
                    report_lines.append(f"  {label}: {stat_value}")
                    break

        report_lines.append("")
    else:
        report_lines.append("Статистика не загружена")
        report_lines.append("")

    if raw_output:
        report_lines.append("ВЫВОД LOCUST:")
        report_lines.append("-" * 50)
        lines = raw_output.strip().split("\n")
        for line in lines[-30:]:
            report_lines.append(f"  {line}")

    report_lines.append("")
    report_lines.append("=" * 50)

    return "\n".join(report_lines)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    users = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    spawn_rate = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    run_time = sys.argv[3] if len(sys.argv) > 3 else "30s"

    print(f"Запуск нагрузочного тестирования: {users} пользователей, {run_time}...")

    stdout, stderr, returncode = run_locust_test(users, spawn_rate, run_time)

    stats = get_results()
    report = format_results(stdout, stats)
    print(report)

    report_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loadtest_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nОтчет сохранен: {report_file}")
