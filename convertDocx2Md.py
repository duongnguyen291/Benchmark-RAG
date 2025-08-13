#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess
from pathlib import Path
import sys
import shutil
import re
from bs4 import BeautifulSoup

def check_pandoc():
    try:
        subprocess.run(["pandoc", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Pandoc chưa cài hoặc không có trong PATH. Hãy cài Pandoc rồi thử lại.")
        sys.exit(1)

def html_table_to_pipe(html_content):
    """Convert HTML tables to pipe markdown tables"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')
        
        for table in tables:
            # Extract table data
            rows = []
            for tr in table.find_all('tr'):
                row = []
                for td in tr.find_all(['td', 'th']):
                    # Get text content and clean it
                    cell_text = td.get_text(strip=True).replace('\n', ' ').replace('|', '\\|')
                    row.append(cell_text if cell_text else ' ')
                if row:  # Only add non-empty rows
                    rows.append(row)
            
            if not rows:
                continue
                
            # Create pipe table
            pipe_table = []
            
            # Add header row
            if rows:
                header = '| ' + ' | '.join(rows[0]) + ' |'
                pipe_table.append(header)
                
                # Add separator row
                separator = '|' + '|'.join(['---' for _ in rows[0]]) + '|'
                pipe_table.append(separator)
                
                # Add data rows
                for row in rows[1:]:
                    # Pad row to match header length
                    while len(row) < len(rows[0]):
                        row.append(' ')
                    data_row = '| ' + ' | '.join(row[:len(rows[0])]) + ' |'
                    pipe_table.append(data_row)
            
            # Replace HTML table with pipe table
            pipe_table_str = '\n' + '\n'.join(pipe_table) + '\n'
            table.replace_with(pipe_table_str)
        
        return str(soup)
    except Exception as e:
        print(f"⚠️  Lỗi khi convert HTML table: {e}")
        return html_content

def convert_docx_to_md(src_path: Path, out_dir: Path, overwrite: bool = False, wrap_none: bool = True, use_html_tables: bool = False):
    """Convert một file .docx sang .md (GFM) với media trích xuất riêng theo tên file."""
    stem = src_path.stem
    out_md = out_dir / f"{stem}.md"
    media_dir = out_dir / f"{stem}_media"

    if out_md.exists() and not overwrite:
        print(f"↷ Bỏ qua (đã tồn tại): {out_md}")
        return True

    # Xóa thư mục media cũ nếu overwrite
    if overwrite and media_dir.exists():
        shutil.rmtree(media_dir)

    # Luôn cho phép HTML tables trong quá trình convert, sau đó post-process
    target = "gfm+footnotes+pipe_tables+tex_math_dollars+raw_html"

    # Tùy chọn cho Pandoc
    cmd = [
        "pandoc",
        str(src_path),
        "-t", target,
        "--extract-media", str(media_dir),
        "--markdown-headings=atx",
        "-o", str(out_md),
        "--columns=200"
    ]
    
    if wrap_none:
        cmd.extend(["--wrap=none"])

    # Thực thi Pandoc
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Post-process: Convert HTML tables to pipe tables nếu cần
        if not use_html_tables:
            try:
                with open(out_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Convert HTML tables to pipe tables
                converted_content = html_table_to_pipe(content)
                
                # Clean up BeautifulSoup artifacts
                converted_content = re.sub(r'<html><body>', '', converted_content)
                converted_content = re.sub(r'</body></html>', '', converted_content)
                converted_content = converted_content.strip()
                
                with open(out_md, 'w', encoding='utf-8') as f:
                    f.write(converted_content)
                    
                print(f"✅ Converted: {src_path.name} → {out_md.name} (tables: pipe)")
            except Exception as e:
                print(f"⚠️  Converted với HTML tables: {src_path.name} → {out_md.name} (lỗi post-process: {e})")
        else:
            print(f"✅ Converted: {src_path.name} → {out_md.name} (tables: HTML)")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi chuyển: {src_path} -> {out_md}")
        print(f"   Command: {' '.join(cmd)}")
        print(f"   Error: {e.stderr if e.stderr else str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Batch convert .docx → Markdown (GFM) bằng Pandoc. Mặc định convert HTML tables thành pipe tables.")
    parser.add_argument("input_dir", type=str, help="Thư mục chứa .docx")
    parser.add_argument("output_dir", type=str, help="Thư mục lưu .md và media")
    parser.add_argument("--recursive", action="store_true", help="Quét đệ quy toàn bộ thư mục con")
    parser.add_argument("--overwrite", action="store_true", help="Ghi đè file .md và media nếu đã tồn tại")
    parser.add_argument("--no-wrap-none", action="store_true", help="Không dùng --wrap=none (mặc định có)")
    parser.add_argument("--html-tables", action="store_true", help="Giữ bảng HTML thay vì convert thành pipe (mặc định là pipe)")
    args = parser.parse_args()

    in_dir = Path(args.input_dir).expanduser().resolve()
    out_dir = Path(args.output_dir).expanduser().resolve()

    if not in_dir.exists() or not in_dir.is_dir():
        print("❌ input_dir không tồn tại hoặc không phải thư mục.")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    check_pandoc()
    
    # Check if BeautifulSoup is available
    if not args.html_tables:
        try:
            import bs4
        except ImportError:
            print("❌ Cần cài beautifulsoup4 để convert HTML tables thành pipe:")
            print("   pip install beautifulsoup4")
            sys.exit(1)

    pattern = "**/*.docx" if args.recursive else "*.docx"
    files = sorted(in_dir.glob(pattern))
    if not files:
        print("⟡ Không tìm thấy file .docx nào.")
        sys.exit(0)

    print(f"📝 Tìm thấy {len(files)} file .docx")
    print(f"📁 Đầu ra: {out_dir}")
    print(f"📋 Định dạng bảng: {'HTML' if args.html_tables else 'Pipe markdown (post-processed)'}")
    print()

    ok = fail = 0
    for f in files:
        if convert_docx_to_md(
            src_path=f,
            out_dir=out_dir,
            overwrite=args.overwrite,
            wrap_none=not args.no_wrap_none,
            use_html_tables=args.html_tables
        ):
            ok += 1
        else:
            fail += 1

    print(f"\n— TỔNG KẾT —")
    print(f"  Thành công: {ok}")
    print(f"  Thất bại : {fail}")
    print(f"  Đầu ra   : {out_dir}")

if __name__ == "__main__":
    main()