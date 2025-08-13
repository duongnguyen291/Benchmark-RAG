# BenchmarkRAG - Đánh giá hiệu suất cho tiếng Việt

## Mô tả
Phiên bản tối ưu hóa của benchmark để đánh giá hiệu suất trích xuất thông tin từ tài liệu tiếng Việt.

## Cài đặt

```bash
pip install -r requirements.txt
pip install underthesea python-Levenshtein
```

## Sử dụng

```bash
python leivein_benchmark_optimized.py
```

## Metrics
- Precision: Độ chính xác
- Recall: Độ bao phủ  
- F1-Score: Trung bình điều hòa
- Accuracy: Độ chính xác tổng thể

## Thư viện sử dụng
- underthesea: Xử lý tiếng Việt
- python-Levenshtein: Tính độ tương đồng
- scipy: Ma trận khoảng cách
