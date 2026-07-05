---
name: quote-builder
description: Dùng khi cần lên file báo giá/đề xuất (proposal) hoàn thiện cho dự án chạy Google Ads — kích hoạt khi người dùng nói "lên báo giá", "làm proposal", "báo giá cho khách hàng X", "media plan", "lên KPI dự kiến". Ghép dữ liệu từ skill keyword-research-search-ads (bộ từ khóa) và skill landing-page-review (kết quả review LDP) cùng kế hoạch KPI/ngân sách vào 1 file Excel báo giá hoàn chỉnh, dùng chung template nhiều tab đã có sẵn.
allowed-tools: Read, Write, Bash, Edit, Glob
version: 1.0.0
---

# Lên file báo giá (Media Plan / Proposal) cho Google Ads

Skill dùng chung cho mọi project/khách hàng. Template gốc nằm cố định trong
thư mục skill (`templates/quote_template.xlsx`); **luôn làm việc trên 1 bản
sao của template**, lưu vào thư mục làm việc của project hiện tại — không
sửa trực tiếp file trong `templates/`.

## Nguồn template (source of truth)

Workbook gốc do người dùng duy trì trên Google Sheet:
https://docs.google.com/spreadsheets/d/1q3BLNVSDLwtdxUOWGut1ia1zvKyDPd9RkY3_IBh1Pxw

Gồm các tab:
1. **`1. KPIs | Master`** — kế hoạch KPI/ngân sách theo hình thức quảng cáo
   (SEARCH, PERFORMANCE MAX, DEMAND GEN, DISPLAY, DISPLAY - REMARKETING,
   VIDEO, APP) và theo từng tháng (Jan-Dec) + cột Total cả năm. **Đây chính
   là phần "báo giá"** — ngân sách (Budget) kèm hiệu suất dự kiến (Impr, CTR,
   Click, CPC, CR, Conv, Cost/Conv, và Revenue/ROAS nếu có AOV) là căn cứ để
   khách hàng duyệt chi phí.
2. **`2. Target | Search`** — nơi điền bộ từ khóa lấy từ skill
   `keyword-research-search-ads`, mỗi chủ đề 1 khối 2 cột (Keyword | Search
   Volume).
3. `2. Target | Non-Search` — targeting cho hình thức phi Search (địa điểm,
   nhân khẩu học, audience...). **Điền thủ công**, ngoài phạm vi tự động của
   3 skill hiện có — hỏi người dùng nếu cần bổ sung, hoặc để trống cho account
   strategist điền tay.
4. `3. Review Account` — checklist audit cấu trúc tài khoản Google Ads.
   **Điền thủ công**, không thuộc phạm vi 3 skill hiện có.
5. **`4. Review Website`** — kết quả review landing page lấy từ skill
   `landing-page-review` (cùng cấu trúc checklist, không có cột STT).
6-8. Các tab phụ (checklist điều kiện, negative keyword, quy trình tối ưu) —
   giữ nguyên như template, không tự động điền.

Nếu người dùng cập nhật template gốc trên Google Sheet, chạy lại
`python scripts/sync_template_from_sheet.py` để đồng bộ.

## Quy trình lên báo giá

1. **Tạo bản làm việc**: copy `templates/quote_template.xlsx` thành file mới
   trong thư mục project, ví dụ `Bao-gia-<TenKhachHang>.xlsx`.

2. **Điền bộ từ khóa (nếu đã chạy skill keyword-research-search-ads)**: dùng
   file `tagged_keywords.csv` (keyword,volume,topic) đã tạo ở skill đó:
   ```
   python "<đường dẫn skill>/scripts/fill_target_search.py" \
       --workbook "Bao-gia-<TenKhachHang>.xlsx" --keywords tagged_keywords.csv
   ```

3. **Điền kết quả review website (nếu đã chạy skill landing-page-review)**:
   dùng file `ket_qua_review.json` (key = STT) đã tạo ở skill đó:
   ```
   python "<đường dẫn skill>/scripts/fill_review_website.py" \
       --workbook "Bao-gia-<TenKhachHang>.xlsx" --results ket_qua_review.json
   ```

4. **Lên kế hoạch KPI/ngân sách**: hỏi người dùng (nếu chưa có) cho từng hình
   thức quảng cáo sẽ triển khai và từng tháng: ngân sách dự kiến (Budget),
   CPC ước tính, Impression ước tính, tỷ lệ chuyển đổi ước tính (CR), và AOV
   nếu là mô hình bán hàng có doanh thu tính được. Ghi thành file JSON
   `ke_hoach_kpi.json` theo đúng schema mô tả trong
   `scripts/fill_kpis_master.py`, rồi chạy:
   ```
   python "<đường dẫn skill>/scripts/fill_kpis_master.py" \
       --workbook "Bao-gia-<TenKhachHang>.xlsx" --plan ke_hoach_kpi.json
   ```
   Script tự tính Click = Budget/CPC, CTR = Click/Impr, Conv = Click*CR,
   Cost/Conv = Budget/Conv (và Revenue/ROAS nếu có AOV), tự cộng dồn cột
   Total theo năm cho từng hình thức, và tự tính dòng "Total" tổng hợp tất cả
   hình thức theo từng tháng + cả năm.

5. Đọc lại 3 sheet đã điền, tóm tắt cho người dùng: tổng ngân sách, hiệu suất
   dự kiến (Click/Conv/Cost per Conv) theo từng hình thức, số từ khóa/chủ đề
   đã lên, và các điểm cần lưu ý từ review website (đặc biệt các mục "Cực kỳ
   quan trọng" đang Chưa đạt) trước khi gửi báo giá cho khách hàng.

## Lưu ý

- Không tự bịa số Impr/CPC/CR nếu người dùng chưa cung cấp — đây là số liệu
  kinh doanh quan trọng, cần hỏi rõ hoặc lấy từ dữ liệu thực tế (VD từ
  Keyword Planner, lịch sử tài khoản cũ) thay vì đoán.
- Không thay đổi cấu trúc cột/tên sheet trong template — nếu cần sửa cấu
  trúc, sửa trên Google Sheet gốc rồi chạy lại `sync_template_from_sheet.py`.
- Có thể chạy độc lập từng bước (chỉ điền từ khóa, hoặc chỉ điền KPI...) tùy
  vào việc các skill khác đã được chạy trước đó hay chưa.
