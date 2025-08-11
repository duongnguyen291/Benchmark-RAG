# Document Extraction Benchmark Framework

A comprehensive framework for benchmarking document extraction tools that convert PDF and DOCX files to Markdown format. This tool evaluates various GitHub repositories and tools for their extraction quality, performance, and accuracy.

## 🚀 Features

- **Multi-Repository Support**: Test multiple GitHub repositories (marker, Unstructured, Parsr, Dolphin, ADE Landing AI)
- **Comprehensive Evaluation**: Multiple metrics including content similarity, structure accuracy, formatting preservation, and table quality
- **Ground Truth Generation**: Automatic generation of ground truth from DOCX files using mammoth
- **Performance Measurement**: Track processing times and success rates
- **Manual Evaluation Interface**: Web-based interface for human assessment
- **Rich Visualizations**: Generate charts, heatmaps, and interactive dashboards
- **Parallel Processing**: Support for concurrent extraction and evaluation
- **Extensible Architecture**: Easy to add new repositories and evaluation metrics

## 📋 Requirements

- Python 3.8+
- Git (for cloning repositories)
- Node.js (for some repositories like Parsr)

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd BenchmarkRAG
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python main.py list-repos
```

## 📁 Project Structure

```
BenchmarkRAG/
├── src/                          # Source code
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── models.py                 # Data models and structures
│   ├── ground_truth.py           # Ground truth generation
│   ├── repository_manager.py     # Repository setup and management
│   ├── evaluator.py              # Evaluation metrics and algorithms
│   ├── benchmark_runner.py       # Main benchmark orchestration
│   ├── report_generator.py       # Report and visualization generation
│   └── manual_evaluation.py      # Manual evaluation interface
├── config/
│   └── repos_config.yaml         # Repository configurations
├── test_files/                   # Test documents (DOCX + PDF pairs)
├── results/                      # Benchmark results and reports
├── main.py                       # CLI interface
├── example_usage.py              # Example usage scripts
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🎯 Quick Start

### 1. Prepare Test Files

Create a `test_files` directory with your DOCX and PDF pairs:

```bash
mkdir test_files
# Add your files:
# test_files/document1.docx
# test_files/document1.pdf
# test_files/document2.docx
# test_files/document2.pdf
# etc.
```

### 2. Run Basic Benchmark

```bash
# Run benchmark with all repositories
python main.py run --test-files ./test_files --output ./results

# Run with specific repositories
python main.py run --test-files ./test_files --output ./results --repos marker unstructured

# Enable manual evaluation
python main.py run --test-files ./test_files --output ./results --enable-manual-eval
```

### 3. View Results

Results are saved in the output directory:
- `summary_report.json` - High-level summary
- `detailed_report.json` - Detailed metrics
- `performance_comparison.png` - Performance charts
- `interactive_dashboard.html` - Interactive visualizations
- `report.html` - HTML report

## 🔍 Evaluation Mode (Pre-Extracted Files)

If you have already extracted Markdown files from various repositories and want to evaluate them against your ground truth:

### 1. Prepare Your Files

Organize your files in this structure:
```
your_data/
├── ground_truth/          # Your DOCX->Markdown files
│   ├── document1.md
│   ├── document2.md
│   └── ...
├── extracted_files/       # Repository results
│   ├── marker/
│   │   ├── document1.md
│   │   ├── document2.md
│   │   └── ...
│   ├── unstructured/
│   │   ├── document1.md
│   │   ├── document2.md
│   │   └── ...
│   └── ...
```

### 2. Run Evaluation

```bash
# Basic evaluation
python main.py evaluate --ground-truth ./your_data/ground_truth --extracted ./your_data/extracted_files --output ./results

# With manual evaluation interface
python main.py evaluate --ground-truth ./your_data/ground_truth --extracted ./your_data/extracted_files --output ./results --enable-manual-eval

# Example with specific options
python main.py evaluate \
  --ground-truth ./ground_truth \
  --extracted ./extracted_files \
  --output ./evaluation_results \
  --enable-manual-eval \
  --host localhost \
  --port 5000
```

### 3. Test with Example

Run the example to see how it works:
```bash
python example_evaluation.py
```

This will create sample files and run a complete evaluation to demonstrate the workflow.

### 4. Manual Evaluation (Optional)

```bash
python main.py manual-eval ./results/manual_evaluation_data.json
```

This opens a web interface for human evaluation of extraction quality.

## 📊 Evaluation Metrics

### Automated Metrics

1. **Content Similarity**
   - BERTScore: Semantic similarity using BERT embeddings
   - ROUGE Score: N-gram overlap metrics
   - BLEU Score: Translation quality metric
   - Exact Match: Perfect content match
   - Word Overlap: Jaccard similarity

2. **Structure Accuracy**
   - Header Accuracy: F1-score for headers
   - List Accuracy: List preservation rate
   - Section Order: Kendall's tau for section ordering
   - Paragraph Accuracy: Paragraph structure preservation

3. **Formatting Preservation**
   - Bold/Italic Accuracy: Formatting preservation
   - Link Accuracy: Hyperlink preservation
   - Image Accuracy: Image handling quality

4. **Table Quality**
   - Structure Preservation: Table structure accuracy
   - Content Accuracy: Cell content similarity
   - Format Consistency: Markdown vs HTML format detection

5. **Performance**
   - Processing Time: Total extraction time
   - Success Rate: Successful extractions percentage

### Manual Evaluation

- Overall Quality (1-5 scale)
- Table Format Quality (1-5 scale)
- Structure Preservation (1-5 scale)
- Formatting Accuracy (1-5 scale)
- Comments and feedback

## 🔧 Configuration

### Repository Configuration

Edit `config/repos_config.yaml` to add or modify repositories:

```yaml
repositories:
  marker:
    name: "Marker"
    repo_url: "https://github.com/fabiensabatie/marker"
    description: "High-performance PDF to Markdown converter"
    setup_commands:
      - "git clone https://github.com/fabiensabatie/marker.git"
      - "cd marker && pip install -r requirements.txt"
    extract_command: "python marker.py {input_file} --output {output_file}"
    output_format: "markdown"
    supported_formats: ["pdf"]
```

### Evaluation Configuration

```yaml
evaluation:
  metrics:
    - "content_similarity"
    - "structure_accuracy" 
    - "formatting_preservation"
    - "table_quality"
    - "processing_time"
  
  bert_score:
    model: "microsoft/deberta-v3-base"
    batch_size: 16
```

## 🚀 Advanced Usage

### Programmatic Usage

```python
from src.models import BenchmarkConfig
from src.benchmark_runner import BenchmarkRunner

# Create configuration
config = BenchmarkConfig(
    test_files_dir="./test_files",
    output_dir="./results",
    repositories_to_test=["marker", "unstructured"],
    enable_manual_evaluation=True,
    parallel_processing=True,
    max_workers=4
)

# Run benchmark
runner = BenchmarkRunner(config)
summary = runner.run_benchmark()

# Get results
best_repo = summary.get_best_repository()
fastest_repo = summary.get_fastest_repository()
ranking = runner.get_repository_ranking()
```

### Custom Evaluation

```python
from src.evaluator import DocumentEvaluator
from src.models import ExtractionResult

# Initialize evaluator
evaluator = DocumentEvaluator()

# Evaluate extraction
evaluation_result = evaluator.evaluate_extraction(
    extraction_result, ground_truth_path
)

print(f"Overall score: {evaluation_result.overall_score}")
print(f"Content similarity: {evaluation_result.content_similarity.bert_score}")
```

### Ground Truth Generation

```python
from src.ground_truth import GroundTruthGenerator

# Generate ground truth
gt_generator = GroundTruthGenerator("./ground_truth")
output_path, processing_time = gt_generator.generate_ground_truth("document.docx")
```

## 📈 Results Interpretation

### Overall Score

The overall score is a weighted combination of all metrics:
- Content Similarity: 40%
- Structure Accuracy: 25%
- Formatting Preservation: 20%
- Table Quality: 15%

### Performance Analysis

- **Success Rate**: Percentage of successful extractions
- **Processing Time**: Average time per document
- **Quality vs Speed**: Trade-off analysis in visualizations

### Repository Comparison

- Side-by-side comparison of all metrics
- Statistical significance testing
- Performance ranking

## 🔍 Troubleshooting

### Common Issues

1. **Repository Setup Fails**
   - Check internet connection
   - Verify Git is installed
   - Check repository URLs in config

2. **Evaluation Metrics Fail**
   - Install missing dependencies: `pip install bert-score rouge-score`
   - Check GPU availability for BERTScore

3. **Manual Evaluation Interface**
   - Ensure Flask is installed
   - Check port availability (default: 5000)
   - Verify evaluation data file exists

### Debug Mode

```bash
python main.py run --test-files ./test_files --output ./results --verbose
```

### Log Files

Check log files in the output directory:
- `benchmark.log` - Detailed execution logs
- `extraction_results.json` - Raw extraction results
- `evaluation_results.json` - Evaluation metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Update tests and documentation
5. Submit a pull request

### Adding New Repositories

1. Add configuration to `config/repos_config.yaml`
2. Test setup commands
3. Verify extraction command format
4. Update documentation

### Adding New Metrics

1. Extend `DocumentEvaluator` class
2. Add metric calculation methods
3. Update data models in `models.py`
4. Add visualization support

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Marker](https://github.com/fabiensabatie/marker) - High-performance PDF to Markdown converter
- [Unstructured](https://github.com/Unstructured-IO/unstructured) - Document processing library
- [Parsr](https://github.com/axa-group/Parsr) - Document parsing tool
- [Mammoth](https://github.com/mwilliamson/mammoth.js) - DOCX to HTML/Markdown converter
- [BERTScore](https://github.com/Tiiiger/bert_score) - BERT-based evaluation metric

## 📞 Support

For questions and support:
- Create an issue on GitHub
- Check the troubleshooting section
- Review example usage scripts

---

**Happy Benchmarking! 🚀** 
