import os
import glob
from docx2pdf import convert
import argparse

class PDFConverter:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.processed_files = []
        
        # Tạo folder con để lưu file output
        self.output_pdf_folder = os.path.join(folder_path, "converted_pdf")
        
        # Tạo folder nếu chưa tồn tại
        os.makedirs(self.output_pdf_folder, exist_ok=True)
    
    def process_docx_file(self, file_path):
        """Chuyển đổi một file DOCX sang PDF"""
        try:
            print(f"Đang xử lý: {file_path}")
            
            # Tạo tên file PDF mới
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            pdf_file = os.path.join(self.output_pdf_folder, f"{base_name}.pdf")
            
            # Chuyển đổi sang PDF
            convert(file_path, pdf_file)
            print(f"Đã chuyển đổi sang PDF: {pdf_file}")
            
            self.processed_files.append({
                'original': file_path,
                'pdf': pdf_file
            })
            
            return True
            
        except Exception as e:
            print(f"Lỗi khi xử lý file {file_path}: {str(e)}")
            return False
    
    def process_folder(self):
        """Xử lý tất cả file DOCX trong folder"""
        if not os.path.exists(self.folder_path):
            print(f"Folder không tồn tại: {self.folder_path}")
            return False
        
        # Tìm tất cả file DOCX
        docx_files = glob.glob(os.path.join(self.folder_path, "*.docx"))
        
        if not docx_files:
            print(f"Không tìm thấy file DOCX nào trong folder: {self.folder_path}")
            return False
        
        print(f"Tìm thấy {len(docx_files)} file DOCX")
        print(f"File PDF sẽ được lưu vào: {self.output_pdf_folder}")
        
        success_count = 0
        for docx_file in docx_files:
            if self.process_docx_file(docx_file):
                success_count += 1
        
        print(f"\nHoàn thành! Đã xử lý thành công {success_count}/{len(docx_files)} file")
        return True
    
    def get_summary(self):
        """Trả về tóm tắt các file đã xử lý"""
        return self.processed_files

def main():
    parser = argparse.ArgumentParser(description='Chuyển đổi file DOCX sang PDF')
    parser.add_argument('folder_path', help='Đường dẫn đến folder chứa file DOCX')
    
    args = parser.parse_args()
    
    # Tạo converter
    converter = PDFConverter(folder_path=args.folder_path)
    
    # Xử lý folder
    converter.process_folder()
    
    # In tóm tắt
    summary = converter.get_summary()
    if summary:
        print("\n=== TÓM TẮT ===")
        for item in summary:
            print(f"Gốc: {item['original']}")
            print(f"PDF: {item['pdf']}")
            print("-" * 50)

if __name__ == "__main__":
    # Ví dụ sử dụng trực tiếp trong code
    folder_path = input("Nhập đường dẫn folder chứa file DOCX: ").strip()
    
    converter = PDFConverter(folder_path)
    converter.process_folder()
    
    # In tóm tắt
    summary = converter.get_summary()
    if summary:
        print("\n=== TÓM TẮT CÁC FILE ĐÃ XỬ LÝ ===")
        for i, item in enumerate(summary, 1):
            print(f"{i}. File gốc: {os.path.basename(item['original'])}")
            print(f"   PDF: {os.path.basename(item['pdf'])}")
            print()