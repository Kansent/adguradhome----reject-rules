import yaml
from pathlib import Path

INPUT = Path("ruleset/reject.yaml")
OUTPUT = Path("output/adguard.txt")

def clash_to_adguard(line: str) -> str | None:
    if line.startswith("DOMAIN-SUFFIX,"):
        domain = line.split(",")[1]
        return f"||{domain}^"
    elif line.startswith("DOMAIN,"):
        domain = line.split(",")[1]
        return f"||{domain}^"
    elif line.startswith("DOMAIN-KEYWORD,"):
        keyword = line.split(",")[1]
        return f"||{keyword}*^"
    elif line.startswith("IP-CIDR,"):
        ip = line.split(",")[1]
        return f"||{ip}^"
    elif line.startswith("IP-CIDR6,"):
        ip = line.split(",")[1]
        return f"||{ip}^"
    elif line.startswith("PROCESS-NAME,"):
        # AdGuard Home 不支持进程名过滤，跳过
        return None
    else:
        return None

def main():
    data = yaml.safe_load(INPUT.read_text())
    payload = data.get("payload", [])

    results = []
    for line in payload:
        line = line.strip()
        rule = clash_to_adguard(line)
        if rule:
            results.append(rule)

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text("\n".join(results), encoding="utf-8")

    print(f"✅ Converted {len(results)} rules -> {OUTPUT}")

if __name__ == "__main__":
    main()
