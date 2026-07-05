#!/usr/bin/env python3
"""
Dong bo toan bo workbook bao gia/media plan (nhieu tab) tu Google Sheet goc
ve templates/quote_template.xlsx cua skill.

Google Sheet nguon (public):
    https://docs.google.com/spreadsheets/d/1q3BLNVSDLwtdxUOWGut1ia1zvKyDPd9RkY3_IBh1Pxw

Cac tab trong file:
    1. KPIs | Master           - ke hoach KPI/ngan sach theo hinh thuc & thang (chinh la "bao gia")
    2. Target | Search         - noi dien bo tu khoa (tu Skill keyword-research-search-ads)
    2. Target | Non-Search     - targeting cho cac hinh thuc phi Search (dien thu cong)
    3. Review Account          - checklist audit tai khoan Google Ads (dien thu cong)
    4. Review Website          - noi dien ket qua review LDP (tu Skill landing-page-review)
    5-7. Cac tab phu / ghi chu

Chay lai script nay khi ban cap nhat cau truc file goc tren Google Sheet.

Cach dung:
    python sync_template_from_sheet.py
"""
import argparse
import os
import urllib.request

DEFAULT_SHEET_ID = "1q3BLNVSDLwtdxUOWGut1ia1zvKyDPd9RkY3_IBh1Pxw"


def main():
    ap = argparse.ArgumentParser(description="Dong bo template bao gia (toan bo workbook) tu Google Sheet goc")
    ap.add_argument("--sheet-id", default=DEFAULT_SHEET_ID)
    args = ap.parse_args()

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(here, "templates", "quote_template.xlsx")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    url = f"https://docs.google.com/spreadsheets/d/{args.sheet_id}/export?format=xlsx"
    urllib.request.urlretrieve(url, out_path)
    print(f"Da dong bo template bao gia vao {out_path}")


if __name__ == "__main__":
    main()
