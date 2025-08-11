#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess
from pathlib import Path
import sys
import shutil

def check_pandoc():
    try:
        subprocess.run(["pandoc", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Pandoc chưa cài hoặc không có trong PATH. Hãy cài Pandoc rồi thử lại.")
        sys.exit(1)

def convert_docx_to_md(src_path: Path, out_dir: Path, overwrite: bool = False, wrap_none: bool = True):
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

    # Định dạng Markdown: GFM + footnotes + pipe_tables + tex_math_dollars (+raw_html để giữ những phần khó)
    target = "gfm+footnotes+pipe_tables+tex_math_dollars+raw_html"

    # Tùy chọn hữu ích cho LLM/RAG:
    # --wrap=none: giữ nguyên dòng, giảm rủi ro ngắt dòng làm hỏng bảng/mã
    # --markdown-headings=atx: dùng # ## ### … (thân thiện công cụ)
    cmd = [
        "pandoc",
        str(src_path),
        "-t", target,
        "--extract-media", str(media_dir),
        "--markdown-headings=atx",
        "-o", str(out_md),
    ]
    if wrap_none:
        cmd.extend(["--wrap=none"])

    # Thực thi
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Converted: {src_path.name} → {out_md.name}  (media: {media_dir.name})")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi chuyển: {src_path} -> {out_md}\n   Command: {' '.join(cmd)}\n   {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Batch convert .docx → Markdown (GFM) bằng Pandoc, giữ bảng/hình/link/chú thích.")
    parser.add_argument("input_dir", type=str, help="Thư mục chứa .docx")
    parser.add_argument("output_dir", type=str, help="Thư mục lưu .md và media")
    parser.add_argument("--recursive", action="store_true", help="Quét đệ quy toàn bộ thư mục con")
    parser.add_argument("--overwrite", action="store_true", help="Ghi đè file .md và media nếu đã tồn tại")
    parser.add_argument("--no-wrap-none", action="store_true", help="Không dùng --wrap=none (mặc định có)")
    args = parser.parse_args()

    in_dir = Path(args.input_dir).expanduser().resolve()
    out_dir = Path(args.output_dir).expanduser().resolve()

    if not in_dir.exists() or not in_dir.is_dir():
        print("❌ input_dir không tồn tại hoặc không phải thư mục.")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    check_pandoc()

    pattern = "**/*.docx" if args.recursive else "*.docx"
    files = sorted(in_dir.glob(pattern))
    if not files:
        print("⟡ Không tìm thấy file .docx nào.")
        sys.exit(0)

    ok = fail = 0
    for f in files:
        if convert_docx_to_md(
            src_path=f,
            out_dir=out_dir,
            overwrite=args.overwrite,
            wrap_none=not args.no_wrap_none
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
