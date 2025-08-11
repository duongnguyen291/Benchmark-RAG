# Quick Start Guide - Evaluating Pre-Extracted Files

This guide will help you quickly set up and run the benchmark framework to evaluate your pre-extracted Markdown files.

## 🚀 Step 1: Setup (One-time)

### 1.1 Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Or run the setup script
python setup.py
```

### 1.2 Test Installation
```bash
# Test that everything works
python test_installation.py
```

## 📁 Step 2: Prepare Your Files

### 2.1 Directory Structure
Organize your files exactly like this:

```
your_data/
├── ground_truth/          # Your DOCX->Markdown files (ground truth)
│   ├── document1.md
│   ├── document2.md
│   ├── document3.md
│   └── ... (up to 10 files)
├── extracted_files/       # Repository results
│   ├── marker/
│   │   ├── document1.md
│   │   ├── document2.md
│   │   ├── document3.md
│   │   └── ...
│   ├── unstructured/
│   │   ├── document1.md
│   │   ├── document2.md
│   │   ├── document3.md
│   │   └── ...
│   ├── parsr/
│   │   ├── document1.md
│   │   ├── document2.md
│   │   ├── document3.md
│   │   └── ...
│   └── ... (other repositories)
```

### 2.2 File Naming Convention
- **Ground truth files**: `document1.md`, `document2.md`, etc.
- **Extracted files**: Must have the same names as ground truth files
- **Repository folders**: Use repository names (marker, unstructured, parsr, dolphin, etc.)

### 2.3 Example File Preparation
```bash
# Create your directory structure
mkdir -p your_data/ground_truth
mkdir -p your_data/extracted_files/marker
mkdir -p your_data/extracted_files/unstructured
mkdir -p your_data/extracted_files/parsr

# Copy your files
cp your_docx_to_markdown_files/*.md your_data/ground_truth/
cp marker_results/*.md your_data/extracted_files/marker/
cp unstructured_results/*.md your_data/extracted_files/unstructured/
cp parsr_results/*.md your_data/extracted_files/parsr/
```

## 🔍 Step 3: Run Evaluation

### 3.1 Basic Evaluation
```bash
python main.py evaluate \
  --ground-truth ./your_data/ground_truth \
  --extracted ./your_data/extracted_files \
  --output ./evaluation_results
```

### 3.2 With Manual Evaluation Interface
```bash
python main.py evaluate \
  --ground-truth ./your_data/ground_truth \
  --extracted ./your_data/extracted_files \
  --output ./evaluation_results \
  --enable-manual-eval
```

### 3.3 With Custom Options
```bash
python main.py evaluate \
  --ground-truth ./your_data/ground_truth \
  --extracted ./your_data/extracted_files \
  --output ./evaluation_results \
  --enable-manual-eval \
  --host localhost \
  --port 5000 \
  --verbose
```

## 📊 Step 4: View Results

### 4.1 Generated Files
After running the evaluation, you'll find these files in your output directory:

```
evaluation_results/
├── detailed_report.json          # Detailed metrics for each file
├── summary_report.json           # High-level summary
├── report.html                   # HTML report with charts
├── performance_comparison.png    # Performance comparison chart
├── metric_heatmap.png           # Metric comparison heatmap
├── processing_time_chart.png    # Processing time analysis
├── score_distribution.png       # Score distribution charts
├── interactive_dashboard.html   # Interactive Plotly dashboard
└── manual_evaluation_data.json  # Data for manual evaluation
```

### 4.2 Key Metrics Explained
- **Content Similarity**: How well the extracted content matches ground truth (BERTScore, ROUGE, BLEU)
- **Structure Accuracy**: How well headers, lists, and document structure are preserved
- **Formatting Preservation**: How well bold, italic, links, and other formatting are maintained
- **Table Quality**: How well tables are extracted and formatted
- **Overall Score**: Weighted combination of all metrics

## 🔍 Step 5: Manual Evaluation (Optional)

### 5.1 Start Manual Evaluation Interface
```bash
python main.py manual-eval ./evaluation_results/manual_evaluation_data.json
```

### 5.2 What You Can Do
- View ground truth and extracted content side-by-side
- Rate quality on a 1-5 scale for different criteria
- Add comments and notes
- Navigate between files and repositories
- Export evaluation results

## 🧪 Step 6: Test with Example

Before using your real data, test the system with example files:

```bash
# Run the example (creates sample files and runs evaluation)
python example_evaluation.py
```

This will:
1. Create sample ground truth and extracted files
2. Run a complete evaluation
3. Generate all reports and visualizations
4. Show you exactly what to expect

## 📋 Common Commands

### List Available Repositories
```bash
python main.py list-repos
```

### Check Help
```bash
python main.py --help
python main.py evaluate --help
```

### Run with Verbose Logging
```bash
python main.py evaluate \
  --ground-truth ./your_data/ground_truth \
  --extracted ./your_data/extracted_files \
  --output ./evaluation_results \
  --verbose
```

## 🚨 Troubleshooting

### Common Issues

1. **"No Markdown files found"**
   - Check that your ground truth directory contains `.md` files
   - Ensure file extensions are lowercase

2. **"No repository folders found"**
   - Check that your extracted_files directory contains subdirectories
   - Ensure repository folders are named correctly

3. **"No extracted file found for [filename]"**
   - Check that extracted files have the same names as ground truth files
   - Ensure file names match exactly (case-sensitive)

4. **Import errors**
   - Run `pip install -r requirements.txt` to install dependencies
   - Check Python version (requires 3.8+)

### Getting Help
- Check the main README.md for detailed documentation
- Run `python test_installation.py` to diagnose issues
- Use `--verbose` flag for detailed logging

## 📈 Understanding Results

### Best Practices
1. **Start with the example**: Run `python example_evaluation.py` first
2. **Use consistent naming**: Ensure all files have matching names
3. **Check file encoding**: Use UTF-8 encoding for all Markdown files
4. **Review manual evaluation**: Use the web interface for detailed assessment
5. **Compare multiple runs**: Run evaluations multiple times to ensure consistency

### Expected Output
- **High scores (0.8-1.0)**: Excellent extraction quality
- **Medium scores (0.6-0.8)**: Good extraction with minor issues
- **Low scores (0.4-0.6)**: Significant quality issues
- **Very low scores (<0.4)**: Major problems with extraction

## 🎯 Next Steps

After running your evaluation:

1. **Review the HTML report** for comprehensive analysis
2. **Use the interactive dashboard** for detailed exploration
3. **Run manual evaluation** for human assessment
4. **Compare different repositories** to find the best tool for your use case
5. **Iterate and improve** based on the results

---

**Need help?** Check the main README.md or run the example script to see the system in action!
