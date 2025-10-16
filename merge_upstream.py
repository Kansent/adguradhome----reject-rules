from pathlib import Path
import requests
from datetime import datetime

OUTPUT = Path("output/nextdns-native-tracking-domains.txt")
OUTPUT.parent.mkdir(exist_ok=True)

URLS = [
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/refs/heads/main/domains/windows",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/refs/heads/main/domains/apple",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/refs/heads/main/domains/samsung",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/refs/heads/main/domains/xiaomi",
]

def fetch_url(url):
    print(f"⬇️ Fetching {url}")
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text.splitlines()

def main():
    domains = set()
    for url in URLS:
        try:
            domains.update(fetch_url(url))
        except Exception as e:
            print(f"⚠️ Failed to fetch {url}: {e}")

    domains = sorted(d.strip() for d in domains if d.strip() and not d.startswith("#"))

    # 生成头部信息
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    size_kb = round(len("\n".join(domains)) / 1024, 2)
    header = [
        f"# NextDNS native tracking domains",
        f"# Last update: {timestamp}",
        f"# Total domains: {len(domains)} ({size_kb} KB)",
        "",
    ]

    OUTPUT.write_text("\n".join(header + domains), encoding="utf-8")
    print(f"✅ Generated {OUTPUT} with {len(domains)} domains.")

if __name__ == "__main__":
    main()
