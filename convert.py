# convert.py
from pathlib import Path
from datetime import datetime
from typing import Optional
import yaml
import os

INPUT = Path("ruleset/reject.yaml")
OUTPUT = Path("output/reject.txt")

def clash_to_adguard(line: str) -> Optional[str]:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    parts = [p.strip() for p in line.split(",", 1)]
    if not parts:
        return None
    kind = parts[0]
    rest = parts[1] if len(parts) > 1 else ""
    if kind in ("DOMAIN-SUFFIX", "DOMAIN"):
        return f"||{rest}^"
    if kind == "DOMAIN-KEYWORD":
        return f"||{rest}*^"
    if kind in ("IP-CIDR", "IP-CIDR6"):
        return f"||{rest}^"
    return None  # PROCESS-NAME 或其他类型忽略

def parse_yaml_payload(path: Path):
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for key in ("payload", "rules", "payloads"):
                if key in data and isinstance(data[key], list):
                    return data[key]
            # 找第一个 list
            for v in data.values():
                if isinstance(v, list):
                    return v
            return []
        elif isinstance(data, list):
            return data
        return []
    except Exception:
        return []

def main():
    payload = parse_yaml_payload(INPUT)
    results = []
    for item in payload:
        if not isinstance(item, str):
            continue
        r = clash_to_adguard(item)
        if r:
            results.append(r)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(results)
    size_kb = len(content.encode("utf-8")) // 1024
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    header = f"# Last update: {timestamp} | Size: {size_kb} KB\n"
    OUTPUT.write_text(header + content + ("\n" if results else ""), encoding="utf-8")
    print(f"✅ Converted {len(results)} rules -> {OUTPUT} (size: {size_kb} KB)")

if __name__ == "__main__":
    main()
