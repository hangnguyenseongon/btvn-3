#!/usr/bin/env python3
"""
Ket noi toi DataForSEO API (Keywords Data - Google Ads) de lay danh sach
tu khoa lien quan + luong tim kiem (search volume) hang thang, phuc vu
nghien cuu bo tu khoa cho Google Search Ads.

Yeu cau bien moi truong:
    DATAFORSEO_LOGIN     - email/login tai khoan DataForSEO
    DATAFORSEO_PASSWORD  - mat khau / API password

Dang ky tai khoan (co goi mien phi de test): https://dataforseo.com

Cach dung:
    python fetch_keywords.py --seeds "dich vu ke toan,thue tron goi" \
        --location 2704 --language vi --out raw_keywords.csv

    --location 2704 = Vietnam, --language vi = tieng Viet (mac dinh)
    Danh sach location_code khac: https://docs.dataforseo.com/v3/appendix/locations/
"""
import argparse
import base64
import csv
import json
import os
import sys
import urllib.request
import urllib.error

API_URL = "https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords/live"


def build_request(seeds, location_code, language_code, limit):
    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        sys.exit(
            "Thieu bien moi truong DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD.\n"
            "Dang ky tai khoan tai https://dataforseo.com roi set:\n"
            "  Windows PowerShell:  $env:DATAFORSEO_LOGIN='...'; $env:DATAFORSEO_PASSWORD='...'\n"
        )

    payload = [{
        "keywords": seeds,
        "location_code": location_code,
        "language_code": language_code,
        "sort_by": "search_volume",
        "limit": limit,
    }]

    body = json.dumps(payload).encode("utf-8")
    token = base64.b64encode(f"{login}:{password}".encode("utf-8")).decode("ascii")
    req = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        },
    )
    return req


def main():
    ap = argparse.ArgumentParser(description="Lay tu khoa + volume tu DataForSEO (Google Ads Keyword Data)")
    ap.add_argument("--seeds", required=True, help="Danh sach tu khoa hat giong, cach nhau bang dau phay")
    ap.add_argument("--location", type=int, default=2704, help="location_code (mac dinh 2704 = Vietnam)")
    ap.add_argument("--language", default="vi", help="language_code (mac dinh vi)")
    ap.add_argument("--limit", type=int, default=200, help="So luong tu khoa toi da tra ve moi seed")
    ap.add_argument("--out", help="Duong dan file CSV de luu ket qua tho (keyword,volume)")
    args = ap.parse_args()

    seeds = [s.strip() for s in args.seeds.split(",") if s.strip()]
    if not seeds:
        sys.exit("Can it nhat 1 tu khoa hat giong trong --seeds")

    req = build_request(seeds, args.location, args.language, args.limit)

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"DataForSEO API loi HTTP {e.code}: {e.read().decode('utf-8', 'ignore')}")
    except urllib.error.URLError as e:
        sys.exit(f"Khong ket noi duoc toi DataForSEO API: {e}")

    tasks = data.get("tasks") or []
    rows = []
    seen = set()
    for task in tasks:
        for result in (task.get("result") or []):
            keyword = (result.get("keyword") or "").strip()
            volume = result.get("search_volume")
            if not keyword or keyword.lower() in seen:
                continue
            seen.add(keyword.lower())
            rows.append({"keyword": keyword, "volume": volume if volume is not None else 0})

    rows.sort(key=lambda r: r["volume"], reverse=True)

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["keyword", "volume"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"Da luu {len(rows)} tu khoa vao {args.out}")
    else:
        print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
