---
name: landing-page-review
description: Dùng khi cần review website/trang đích (landing page) trước hoặc trong khi chạy quảng cáo Google Ads — kích hoạt khi người dùng nói "review website", "review landing page", "check LDP", "đánh giá trang đích", "audit landing page cho Google Ads". Sử dụng checklist review chuẩn có sẵn (46 hạng mục, đồng bộ từ Google Sheet chủ) để đánh giá và xuất file Excel kết quả cho từng khách hàng/dự án.
allowed-tools: Read, Write, Bash, Edit, Glob, WebFetch
version: 1.0.0
---

# Review Website / Landing Page cho Google Ads

Skill dùng chung cho mọi project/khách hàng. Template checklist nằm cố định
trong thư mục skill (`templates/`); **file kết quả review luôn được lưu vào
thư mục làm việc của project hiện tại**, không lưu vào trong thư mục skill.

## Nguồn checklist (source of truth)

Checklist gốc do người dùng duy trì trên Google Sheet:
https://docs.google.com/spreadsheets/d/1q3BLNVSDLwtdxUOWGut1ia1zvKyDPd9RkY3_IBh1Pxw/edit?gid=498393758

Bản đồng bộ mới nhất được lưu sẵn tại:
- `templates/landing_page_review_checklist.csv` — bản dữ liệu thô, dễ đọc.
- `templates/landing_page_review_checklist.xlsx` — bản Excel đã format, dùng
  làm file gốc để tạo báo cáo review.

Cấu trúc mỗi dòng: `STT, Giai đoạn, Hạng mục đánh giá, Hạng mục con, Chi tiết
công việc, Tỉ lệ đáp ứng (checkbox TRUE/FALSE cho mục bắt buộc), Mức độ quan
trọng, Tình trạng (để trống — nơi điền kết quả review)`.

4 giai đoạn trong checklist:
1. **Xác định thông tin** (STT 1-5): bước chuẩn bị trước khi review — đọc
   brief, xác định mục tiêu chiến dịch, loại website, kênh/hình thức quảng cáo.
2. **Checklist chung** (STT 6-13): UX, thân thiện di động, tốc độ tải trang
   (PageSpeed Insights, Testmysite), domain/SSL, favicon.
3. **Check list cơ bản** (STT 14-19): mã tracking (GTM/GA/Ads/Pixel), tương
   thích trình duyệt, liên kết fanpage, live chat.
4. **Check list nâng cao**: STT 20-39 dành cho **website/LDP bán hàng**
   (danh mục, trang sản phẩm, đặt hàng, chính sách); STT 40-46 dành cho
   **website/LDP dịch vụ** (thông tin dịch vụ, form CTA liên hệ). Chỉ áp dụng
   nhóm phù hợp với loại website đang review.

Nếu người dùng cập nhật checklist trên Google Sheet, chạy lại
`python scripts/sync_checklist_from_sheet.py` để đồng bộ 2 file template trên.

## Quy trình review

1. Hỏi người dùng (nếu chưa rõ): URL landing page, loại website (bán hàng /
   dịch vụ / website hoàn chỉnh khác LDP), tên khách hàng/dự án.
2. Đọc `templates/landing_page_review_checklist.csv` để biết đầy đủ các hạng
   mục cần kiểm tra, xác định nhóm nâng cao nào áp dụng (bán hàng hay dịch vụ).
3. Thu thập dữ liệu thực tế về trang:
   - Dùng `WebFetch` (hoặc trình duyệt Chrome nếu cần xem trực quan/tương tác)
     để đọc nội dung, bố cục, CTA, thông tin liên hệ, chính sách, mã tracking
     (view-source để tìm gtag/GTM/fbq/ttq) của trang.
   - Gọi **Google PageSpeed Insights API** (miễn phí, không cần key cho tần
     suất thấp) để lấy điểm tốc độ mobile/desktop cho hạng mục STT 10:
     `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<URL>&strategy=mobile`
     và `&strategy=desktop`.
   - Kiểm tra Mobile-Friendly (Google Search Console / thử nghiệm responsive)
     cho STT 9, và SSL/https cho STT 12.
4. Với mỗi hạng mục có thể đánh giá được, ghi kết quả vào một file JSON tạm
   `ket_qua_review.json`, key là STT, value gồm `ty_le_dap_ung` (true/false,
   chỉ áp dụng cho các mục có checkbox bắt buộc) và `tinh_trang` (mô tả ngắn
   gọn kết quả + lý do, ví dụ: `"Đạt - tốc độ mobile 78/100"` hoặc
   `"Chưa đạt - thiếu chính sách đổi trả"`). Bỏ qua STT thuộc nhóm không áp
   dụng (VD bỏ nhóm "Website/LDP bán hàng" khi đang review website dịch vụ).
5. Chạy script xuất báo cáo:
   ```
   python "<đường dẫn skill>/scripts/fill_review_report.py" \
       --results ket_qua_review.json --out "Review-LDP-<TenKhachHang>.xlsx"
   ```
6. Tóm tắt cho người dùng: số mục Đạt/Chưa đạt, đặc biệt nhấn mạnh các mục có
   "Mức độ quan trọng" = Cực kỳ quan trọng đang Chưa đạt, kèm đề xuất cải
   thiện ưu tiên xử lý trước khi chạy/tiếp tục chạy quảng cáo.

## Lưu ý

- Không tự suy diễn "Đạt" khi chưa thực sự kiểm tra được (ví dụ không truy
  cập được trang, hoặc API PageSpeed lỗi) — ghi rõ "Không kiểm tra được - lý
  do" thay vì đoán.
- Giữ đúng cấu trúc 8 cột của checklist gốc, không tự thêm/xoá hạng mục —
  nếu cần sửa nội dung checklist, sửa trên Google Sheet gốc rồi chạy lại
  `sync_checklist_from_sheet.py`.
