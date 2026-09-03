# Mở đầu

Trong nghiên cứu này, chúng tôi xây dựng tập dữ liệu hỏi đáp pháp luật tiếng Việt gồm 5.980 ngữ cảnh.
Mục 2 tổng quan các tài nguyên liên quan, Mục 3 mô tả quy trình xây dựng dữ liệu, Mục 4 báo cáo kết quả đánh giá và Mục 5 nêu các hạn chế.

# Phương pháp

Chúng tôi lấy mẫu ngữ cảnh trong khoảng 100–3.000 ký tự.
Bảng 1 trình bày phân bố độ dài, và Hình 2 cho thấy tỷ lệ trùng lặp theo giáo trình.
Quy trình dùng thư viện suy luận vLLM ở chế độ lượng tử hóa 4 bit, nhiệt độ lấy mẫu 0,7.

# Tuyên bố dữ liệu

Bộ dữ liệu công bố tại DOI 10.5281/zenodo.1234567 và kho lưu trữ https://github.com/example/vi-legalqa.
Phụ lục A liệt kê toàn bộ nguồn giáo trình.

# Tính cấp thiết của đề tài

Tài nguyên đánh giá cho miền pháp luật tiếng Việt còn thiếu, nên năng lực của các mô hình hiện có chưa được đo trên văn bản quy phạm trong nước.

# Hạn chế

Nhãn nhận thức là nhãn thao tác, nên các so sánh giữa mô hình chỉ có giá trị trong phạm vi định nghĩa nhãn này.
