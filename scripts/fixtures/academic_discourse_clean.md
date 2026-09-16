# Kết quả

Trong ngữ cảnh oracle, mô hình trả lời trên đoạn nguồn đã được cung cấp sẵn. Thiết kế này cô lập năng lực tạo câu trả lời khỏi sai số truy hồi; vì vậy kết quả chỉ đặc trưng cho giai đoạn trả lời khi ngữ cảnh liên quan đã biết.

# Hạn chế

Nhãn Bloom được gán tự động mà không có đối chiếu chuyên gia. Do đó, các phân tích theo bậc nhận thức sử dụng nhãn này như một biến thao tác và không ước lượng độ tin cậy phân loại.

# Hướng nghiên cứu

Một nghiên cứu thẩm định với mẫu phân tầng và nhiều chuyên gia có thể ước lượng độ nhất quán của nhãn. Kết quả đó sẽ cho biết liệu các so sánh theo bậc Bloom có ổn định khi thay nhãn tự động bằng nhãn tham chiếu hay không.

# Phương pháp

Quy trình gồm ba giai đoạn: trích xuất ngữ cảnh, tạo câu hỏi và lọc ứng viên. Mỗi giai đoạn tạo một đầu ra riêng để có thể xác định nơi phát sinh hao hụt dữ liệu.
