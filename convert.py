# convert.py
from pathlib import Path
from datetime import datetime
from typing import Optional
import yaml

INPUT = Path("ruleset/reject.yaml")
OUTPUT = Path("output/adguard.txt")

def clash_to_adguard(line: str) -> Optional[str]:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    # 支持带空格的逗号分隔
    parts = [p.strip() for p in line.split(",", 1)]
    if not parts:
        return None
    kind = parts[0]
    rest = parts[1] if len(parts) > 1 else ""
    if kind == "DOMAIN-SUFFIX":
        return f"||{rest}^"
    if kind == "DOMAIN":
        return f"||{rest}^"
    if kind == "DOMAIN-KEYWORD":
        return f"||{rest}*^"
    if kind == "IP-CIDR" or kind == "IP-CIDR6":
        return f"||{rest}^"
    if kind == "PROCESS-NAME":
        return None
    return None

def parse_yaml_payload(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        # 常见字段名：payload, rules, 或者直接是 list
        if isinstance(data, dict):
            for key in ("payload", "rules", "payloads"):
                if key in data and isinstance(data[key], list):
                    return data[key]
            # 如果 dict 里有一个顶层 list 的值，则取第一个 list
            for v in data.values():
                if isinstance(v, list):
                    return v
            return []
        elif isinstance(data, list):
            return data
        else:
            return []
    except Exception:
        # YAML 解析失败时，按行读取文本尝试解析（兼容奇怪格式）
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
            # 取以逗号开头或含有常见前缀的行
            filtered = [ln.strip() for ln in lines if any(ln.strip().startswith(p) for p in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6", "PROCESS-NAME"))]
            return filtered
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
    header = f"# Auto-generated from {INPUT} — Last update: {datetime.utcnow().isoformat()}Z\n"
    OUTPUT.write_text(header + "\n".join(results) + ("\n" if results else ""), encoding="utf-8")
    print(f"✅ Converted {len(results)} rules -> {OUTPUT}")

if __name__ == "__main__":
    main()
