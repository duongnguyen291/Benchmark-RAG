#!/usr/bin/env python3
"""
Example script showing how to prepare files for evaluation and run the benchmark.
This script demonstrates the workflow for evaluating pre-extracted Markdown files.
"""

import os
import shutil
from pathlib import Path
import subprocess
import sys

def create_example_structure():
    """Create example directory structure for evaluation."""
    print("📁 Creating example directory structure...")
    
    # Create directories
    base_dir = Path("example_evaluation")
    ground_truth_dir = base_dir / "ground_truth"
    extracted_dir = base_dir / "extracted_files"
    results_dir = base_dir / "results"
    
    # Clean up if exists
    if base_dir.exists():
        shutil.rmtree(base_dir)
    
    # Create directories
    ground_truth_dir.mkdir(parents=True)
    extracted_dir.mkdir(parents=True)
    results_dir.mkdir(parents=True)
    
    # Create example ground truth files (DOCX -> Markdown)
    ground_truth_files = [
        ("document1.md", "# Document 1\n\nThis is the first document.\n\n## Section 1\n\nSome content here.\n\n### Subsection\n\nMore detailed content.\n\n## Section 2\n\nAnother section with **bold text** and *italic text*.\n\n- List item 1\n- List item 2\n- List item 3\n\n| Column 1 | Column 2 | Column 3 |\n|----------|----------|----------|\n| Data 1   | Data 2   | Data 3   |\n| Data 4   | Data 5   | Data 6   |"),
        ("document2.md", "# Document 2\n\nThis is the second document.\n\n## Introduction\n\nThis document contains various formatting.\n\n### Code Example\n\n```python\nprint('Hello, World!')\ndef example_function():\n    return 'This is a function'\n```\n\n## Conclusion\n\nThis concludes the document."),
        ("document3.md", "# Document 3\n\n## Overview\n\nThis document has a different structure.\n\n### Features\n\n1. **Feature 1**: Description of feature 1\n2. **Feature 2**: Description of feature 2\n3. **Feature 3**: Description of feature 3\n\n## Summary\n\nThis is a summary section with some important points:\n\n- Point A\n- Point B\n- Point C\n\n> This is a blockquote with important information.")
    ]
    
    for filename, content in ground_truth_files:
        with open(ground_truth_dir / filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Create example extracted files from different repositories
    repositories = ["marker", "unstructured", "parsr", "dolphin"]
    
    for repo in repositories:
        repo_dir = extracted_dir / repo
        repo_dir.mkdir()
        
        # Create slightly different versions for each repository
        for i, (filename, content) in enumerate(ground_truth_files):
            # Simulate different extraction quality
            if repo == "marker":
                # High quality extraction
                modified_content = content
            elif repo == "unstructured":
                # Medium quality - some formatting lost
                modified_content = content.replace("**", "").replace("*", "")
            elif repo == "parsr":
                # Lower quality - structure issues
                modified_content = content.replace("## ", "# ").replace("### ", "## ")
            else:  # dolphin
                # Different formatting approach
                modified_content = content.replace("|", " | ").replace("\n|", "\n | ")
            
            with open(repo_dir / filename, 'w', encoding='utf-8') as f:
                f.write(modified_content)
    
    print(f"✅ Created example structure in: {base_dir}")
    print(f"   Ground truth files: {ground_truth_dir}")
    print(f"   Extracted files: {extracted_dir}")
    print(f"   Results will be saved to: {results_dir}")
    
    return base_dir

def run_evaluation(base_dir):
    """Run the evaluation on the example files."""
    print("\n🔍 Running evaluation...")
    
    ground_truth_dir = base_dir / "ground_truth"
    extracted_dir = base_dir / "extracted_files"
    results_dir = base_dir / "results"
    
    # Build the command
    cmd = [
        sys.executable, "main.py", "evaluate",
        "--ground-truth", str(ground_truth_dir),
        "--extracted", str(extracted_dir),
        "--output", str(results_dir),
        "--enable-manual-eval"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Evaluation completed successfully!")
        print("\nOutput:")
        print(result.stdout)
        
        if result.stderr:
            print("\nWarnings/Errors:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Evaluation failed with error code {e.returncode}")
        print("Error output:")
        print(e.stderr)
        print("Standard output:")
        print(e.stdout)

def show_file_structure(base_dir):
    """Show the created file structure."""
    print(f"\n📂 File structure created:")
    print(f"{base_dir}/")
    
    def print_tree(path, prefix=""):
        for item in sorted(path.iterdir()):
            if item.is_dir():
                print(f"{prefix}📁 {item.name}/")
                print_tree(item, prefix + "  ")
            else:
                print(f"{prefix}📄 {item.name}")
    
    print_tree(base_dir)

def main():
    """Main function to demonstrate the evaluation workflow."""
    print("🚀 Document Extraction Benchmark - Evaluation Example")
    print("=" * 60)
    
    print("\nThis example demonstrates how to:")
    print("1. Prepare ground truth Markdown files (from DOCX)")
    print("2. Prepare extracted Markdown files from different repositories")
    print("3. Run the evaluation to compare quality")
    print("4. Generate reports and visualizations")
    
    # Create example structure
    base_dir = create_example_structure()
    
    # Show the structure
    show_file_structure(base_dir)
    
    # Run evaluation
    run_evaluation(base_dir)
    
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("1. Replace the example files with your actual ground truth and extracted files")
    print("2. Run the evaluation command with your real data")
    print("3. Review the generated reports in the results directory")
    print("4. Use the manual evaluation interface for detailed assessment")
    
    print(f"\n📁 Your files should be organized like this:")
    print(f"   {base_dir}/")
    print(f"   ├── ground_truth/          # Your DOCX->Markdown files")
    print(f"   │   ├── document1.md")
    print(f"   │   ├── document2.md")
    print(f"   │   └── ...")
    print(f"   ├── extracted_files/       # Repository results")
    print(f"   │   ├── marker/")
    print(f"   │   │   ├── document1.md")
    print(f"   │   │   ├── document2.md")
    print(f"   │   │   └── ...")
    print(f"   │   ├── unstructured/")
    print(f"   │   └── ...")
    print(f"   └── results/              # Evaluation results")
    
    print(f"\n💡 Command to run with your files:")
    print(f"   python main.py evaluate --ground-truth ./your_ground_truth --extracted ./your_extracted_files --output ./your_results")

if __name__ == "__main__":
    main()
