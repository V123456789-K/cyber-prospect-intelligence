import io
import json
import os

import pandas as pd


def load_records(path=None):
    path = path or os.getenv("DATASET_PATH", "data/sample.jsonl")
    records = []
    if path.endswith(".zst"):
        import zstandard as zstd
        with open(path, "rb") as raw:
            with zstd.ZstdDecompressor().stream_reader(raw) as reader:
                text = io.TextIOWrapper(reader, encoding="utf-8")
                for line in text:
                    try: records.append(json.loads(line))
                    except json.JSONDecodeError: continue
        return records
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line=line.strip()
            if not line: continue
            try: records.append(json.loads(line))
            except json.JSONDecodeError: continue
    return records


def build_dataframe(path=None):
    rows=[]
    for record in load_records(path):
        location=record.get("location") or {}
        rows.append({"ip":record.get("ip_str"),"organization":record.get("org"),"asn":record.get("asn"),"country":location.get("country_name"),"city":location.get("city"),"domains":", ".join(record.get("domains") or []),"hostnames":", ".join(record.get("hostnames") or []),"os":record.get("os"),"transport":record.get("transport"),"module":(record.get("_shodan",{}).get("module") if isinstance(record.get("_shodan"),dict) else None),"timestamp":record.get("timestamp"),"raw":record})
    return pd.DataFrame(rows)
