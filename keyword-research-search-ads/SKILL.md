---
name: keyword-research-search-ads
description: Dùng khi cần nghiên cứu/cào bộ từ khóa để lên kế hoạch chạy Google Search Ads — kích hoạt khi người dùng nói "tìm từ khóa", "research keyword", "cào từ khóa", "lên bộ từ khóa cho chiến dịch Search", "keyword planner", "search volume". Kết nối API DataForSEO (Google Ads Keyword Data) để lấy từ khóa liên quan kèm volume tìm kiếm, sau đó xuất ra 1 file Excel — cột Từ khóa, cột Volume — được chia theo từng chủ đề/ad group riêng biệt.
allowed-tools: Read, Write, Bash, Edit, Glob
version: 1.0.0
---

# Nghiên cứu bộ từ khóa cho Google Search Ads

Skill này dùng được cho bất kỳ project/khách hàng nào. File script nằm cố định
trong thư mục skill (`scripts/`); **file kết quả (CSV trung gian + Excel cuối)
luôn được lưu vào thư mục làm việc của project hiện tại**, không lưu vào
trong thư mục skill.

## Đầu vào cần hỏi người dùng (nếu chưa cung cấp)

1. Từ khóa hạt giống (seed keywords) — sản phẩm/dịch vụ cốt lõi.
2. Ngành/lĩnh vực kinh doanh, để hỗ trợ việc gom chủ đề.
3. Thị trường & ngôn ngữ (mặc định Việt Nam / tiếng Việt).
4. Có muốn loại các từ khóa thương hiệu đối thủ / từ khóa không liên quan không.

## Quy trình

1. **Kiểm tra kết nối API**: skill dùng DataForSEO — API bên ngoài cho dữ liệu
   Google Ads Keyword Data (search volume thật). Kiểm tra 2 biến môi trường
   `DATAFORSEO_LOGIN` và `DATAFORSEO_PASSWORD` đã được set chưa
   (`echo $DATAFORSEO_LOGIN` / PowerShell `$env:DATAFORSEO_LOGIN`). Nếu chưa
   có, hướng dẫn người dùng đăng ký tài khoản miễn phí dùng thử tại
   https://dataforseo.com rồi set biến môi trường trước khi tiếp tục.
   - Phương án thay thế: nếu người dùng đã có Google Ads API developer token
     (Google Keyword Planner chính chủ), có thể dùng
     `KeywordPlanIdeaService.GenerateKeywordIdeas` thay cho DataForSEO — báo
     cho người dùng biết đây là lựa chọn "chuẩn Google" nhưng cần thời gian
     xin duyệt developer token.

2. **Lấy dữ liệu thô**: chạy
   ```
   python "<đường dẫn skill>/scripts/fetch_keywords.py" \
       --seeds "seed1,seed2,seed3" --location 2704 --language vi \
       --out raw_keywords.csv
   ```
   (`--location 2704` = Việt Nam; đổi mã theo thị trường khác nếu cần, xem
   bảng location_code của DataForSEO).

3. **Phân tích & gán chủ đề**: đọc `raw_keywords.csv`, tự suy luận và gán mỗi
   từ khóa vào một chủ đề (topic/ad group) dựa theo search intent — ví dụ
   theo dòng sản phẩm, theo giai đoạn phễu (tìm hiểu/so sánh/mua ngay), hoặc
   theo địa điểm. Loại bỏ từ khóa rác, trùng lặp, hoặc thương hiệu đối thủ
   nếu người dùng yêu cầu. Ghi kết quả ra file CSV trung gian
   `tagged_keywords.csv` với 3 cột: `keyword,volume,topic`.

4. **Xuất file Excel cuối cùng**: chạy
   ```
   python "<đường dẫn skill>/scripts/build_keyword_report.py" \
       --in tagged_keywords.csv --out "Bo-tu-khoa-<TenKhachHang>.xlsx"
   ```
   File Excel sinh ra gồm:
   - Sheet **"Tổng hợp"**: toàn bộ từ khóa, cột Từ khóa / Volume / Chủ đề.
   - Mỗi chủ đề một sheet riêng: chỉ 2 cột Từ khóa / Volume, sắp xếp Volume
     giảm dần — sẵn sàng để tạo ad group tương ứng trong Google Ads.

5. Báo lại cho người dùng: tổng số từ khóa, số chủ đề, top từ khóa volume cao
   nhất mỗi chủ đề, và đường dẫn file Excel đã lưu.

## Lưu ý

- Không tự bịa số liệu volume nếu API lỗi hoặc thiếu credential — báo lỗi rõ
  ràng và dừng lại để người dùng xử lý, thay vì tạo dữ liệu giả.
- Nếu người dùng chỉ cung cấp file từ khóa có sẵn (không cần gọi API), vẫn có
  thể dùng thẳng bước 3-4 (gán chủ đề + xuất Excel) trên dữ liệu đó.
