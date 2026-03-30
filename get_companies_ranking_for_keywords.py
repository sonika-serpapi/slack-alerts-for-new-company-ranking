import os
import json
import time
import requests
import schedule
import serpapi
import tldextract

from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.environ["SERPAPI_API_KEY"]
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK_URL"]

QUERY_LIST = ["ai images tool", "ai image generators", "image creation ai tools"]

DB_FILE = "known_domains.json"


def get_root_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"


def get_all_domains(query_list):
    domains_for_each_query = {}
    client = serpapi.Client(api_key=SERPAPI_KEY)

    for query in query_list:
        domains_for_each_query[query] = set()

        for start in range(0, 30, 10):
            results = client.search(
                {
                    "engine": "google",
                    "google_domain": "google.com",
                    "q": query,
                    "start": start,
                }
            )

            if "organic_results" not in results:
                break

            for result in results["organic_results"]:
                link = result.get("link")
                if not link:
                    continue

                root_domain = get_root_domain(link)
                domains_for_each_query[query].add(root_domain)

    return {k: list(v) for k, v in domains_for_each_query.items()}


def load_domains():
    try:
        with open(DB_FILE) as f:
            return dict(json.load(f))
    except Exception:
        return {}


def save_domains(domains):
    with open(DB_FILE, "w") as f:
        json.dump(domains, f)


def send_slack_alert(domains):
    domains = {
        k: v for k, v in domains.items() if v
    }  # Filter out queries with no new domains

    if not domains:
        requests.post(
            SLACK_WEBHOOK, json={"text": "✅ No new companies detected for any query."}
        )
        return

    for query, companies in domains.items():
        message = {
            "text": f"🚨 New company detected for '{query}':\n" + "\n".join(companies)
        }
        requests.post(SLACK_WEBHOOK, json=message)


def check_for_new_domains():
    print("Checking for new domains...")

    known_domains = load_domains()

    current_domains = get_all_domains(QUERY_LIST)

    new_domains = {}

    for query in current_domains:
        new_domains[query] = list(
            set(current_domains[query]) - set(known_domains.get(query, []))
        )

        known_domains[query] = list(
            set(known_domains.get(query, [])) | set(current_domains[query])
        )

    send_slack_alert(new_domains)

    save_domains(known_domains)


# Schedule the bot to run every day at 9 AM
schedule.every().day.at("09:00").do(check_for_new_domains)
print("Query domain monitoring bot running...")

while True:
    schedule.run_pending()
    time.sleep(60)
