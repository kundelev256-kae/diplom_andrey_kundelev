from locust import HttpUser, task, between, events
import json
import time
import os

RESULTS_FILE = "loadtest_results.json"


class ItStepUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://itstep.by"

    def on_start(self):
        self.client.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        })

    @task(5)
    def main_page(self):
        self.client.get("/", name="Главная страница")

    @task(3)
    def vacancies_page(self):
        self.client.get("/careers/", name="Вакансии")

    @task(3)
    def contacts_page(self):
        self.client.get("/kontakty/", name="Контакты")

    @task(2)
    def news_page(self):
        self.client.get("/news/", name="Новости")

    @task(2)
    def articles_page(self):
        self.client.get("/stati-i-publikaczii/", name="Статьи")

    @task(2)
    def qa_course(self):
        self.client.get("/testirovanie-po-qa/", name="Курс QA")

    @task(1)
    def python_course(self):
        self.client.get("/razrabotka-po-na-python/", name="Курс Python")

    @task(1)
    def java_course(self):
        self.client.get("/razrabotka-po-na-java/", name="Курс Java")

    @task(1)
    def ux_ui_course(self):
        self.client.get("/ux-ui-dizajn/", name="Курс UX/UI")

    @task(1)
    def devops_course(self):
        self.client.get("/devops-engineer/", name="Курс DevOps")

    @task(1)
    def robots_txt(self):
        self.client.get("/robots.txt", name="robots.txt")


results_data = {
    "start_time": None,
    "end_time": None,
    "total_requests": 0,
    "failed_requests": 0,
    "avg_response_time": 0,
    "rps": 0,
    "min_response_time": 0,
    "max_response_time": 0,
    "p50": 0,
    "p90": 0,
    "p95": 0,
    "p99": 0,
    "status_codes": {},
    "errors": [],
}


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    results_data["start_time"] = time.time()
    results_data["total_requests"] = 0
    results_data["failed_requests"] = 0
    results_data["status_codes"] = {}
    results_data["errors"] = []


@events.request.add_listener
def on_request(request_type, name, response_time, response_length,
               exception, context, start_time, **kwargs):
    results_data["total_requests"] += 1

    if response_time:
        if results_data["min_response_time"] == 0 or response_time < results_data["min_response_time"]:
            results_data["min_response_time"] = response_time
        if response_time > results_data["max_response_time"]:
            results_data["max_response_time"] = response_time

    if exception:
        results_data["failed_requests"] += 1
        results_data["errors"].append({
            "name": name,
            "error": str(exception),
            "time": response_time,
        })


@events.quitting.add_listener
def on_quit(environment, **kwargs):
    results_data["end_time"] = time.time()
    stats = environment.runner.stats

    total_time = results_data["end_time"] - results_data["start_time"]
    results_data["rps"] = results_data["total_requests"] / total_time if total_time > 0 else 0

    try:
        if stats.total.use_response_time_counts:
            results_data["p50"] = stats.total.get_response_time_percentile(0.5)
            results_data["p90"] = stats.total.get_response_time_percentile(0.9)
            results_data["p95"] = stats.total.get_response_time_percentile(0.95)
            results_data["p99"] = stats.total.get_response_time_percentile(0.99)

        results_data["avg_response_time"] = stats.total.get_response_time_mean()

        for stat in stats.entries.values():
            code = "N/A"
            if hasattr(stat, 'last_request') and stat.last_request and hasattr(stat.last_request, 'metadata') and stat.last_request.metadata:
                code = f"{stat.last_request.metadata.get('response_code', 'N/A')}"
            results_data["status_codes"][code] = results_data["status_codes"].get(code, 0) + stat.num_requests
    except Exception:
        pass

    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), RESULTS_FILE)
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
