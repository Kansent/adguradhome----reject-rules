from pathlib import Path
from datetime import datetime
import requests

UPSTREAM_URLS = [
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/refs/heads/main/domains/windows",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/refs/heads/main/domains/apple",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/refs/heads/main/domains/samsung",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/refs/heads/main/domains/xiaomi",
]

OUTPUT = Path("output/nextdns-native-tracking-domains.txt")

def download_domains(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    lines = [line.strip() for line in resp.text.splitlines() if line.strip() and not line.startswith("#")]
    return lines

def main():
    all_domains = set()
    for url in UPSTREAM_URLS:
        all_domains.update(download_domains(url))

    rules = [f"||{d}^" for d in sorted(all_domains)]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(rules)
    size_kb = len(content.encode("utf-8")) // 1024
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    header = f"# Last update: {timestamp} | Size: {size_kb} KB\n"
    OUTPUT.write_text(header + content + ("\n" if rules else ""), encoding="utf-8")
    print(f"✅ Merged {len(rules)} upstream domains -> {OUTPUT}")

if __name__ == "__main__":
    main()
