#!/usr/bin/env python3
"""
Test script to verify the Document Extraction Benchmark Framework installation.
This script checks if all components are working correctly.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        # Test core imports
        from src.config import config_manager
        from src.models import BenchmarkConfig, ProcessingTime
        from src.ground_truth import GroundTruthGenerator
        from src.repository_manager import RepositoryManager
        from src.evaluator import DocumentEvaluator
        from src.benchmark_runner import BenchmarkRunner
        from src.report_generator import ReportGenerator
        from src.manual_evaluation import ManualEvaluationInterface
        
        print("✅ All core modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_configuration():
    """Test configuration loading."""
    print("\n🔍 Testing configuration...")
    
    try:
        from src.config import config_manager
        
        # Test repository configuration
        repos = config_manager.get_repositories()
        print(f"✅ Loaded {len(repos)} repository configurations")
        
        # Test ground truth configuration
        gt_config = config_manager.get_ground_truth_config()
        print(f"✅ Ground truth tool: {gt_config.tool}")
        
        # Test evaluation configuration
        eval_config = config_manager.get_evaluation_config()
        print(f"✅ Evaluation metrics: {len(eval_config.metrics)} metrics configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_data_models():
    """Test data model creation."""
    print("\n🔍 Testing data models...")
    
    try:
        from src.models import (
            ProcessingTime, ContentSimilarityMetrics, StructureAccuracyMetrics,
            FormattingPreservationMetrics, TableQualityMetrics, ExtractionResult,
            EvaluationResult, BenchmarkConfig
        )
        
        # Test ProcessingTime
        pt = ProcessingTime(total_time=1.5, extraction_time=1.2)
        print(f"✅ ProcessingTime created: {pt.total_time}s")
        
        # Test ContentSimilarityMetrics
        csm = ContentSimilarityMetrics(
            bert_score=0.85, rouge_score=0.78, bleu_score=0.72,
            exact_match=0.0, word_overlap=0.82
        )
        print(f"✅ ContentSimilarityMetrics created: BERT={csm.bert_score:.2f}")
        
        # Test BenchmarkConfig
        config = BenchmarkConfig(
            test_files_dir="./test_files",
            output_dir="./results",
            repositories_to_test=["marker", "unstructured"]
        )
        print(f"✅ BenchmarkConfig created: {len(config.repositories_to_test)} repos")
        
        return True
        
    except Exception as e:
        print(f"❌ Data model test failed: {e}")
        return False


def test_ground_truth_generator():
    """Test ground truth generator initialization."""
    print("\n🔍 Testing ground truth generator...")
    
    try:
        from src.ground_truth import GroundTruthGenerator
        
        # Test initialization
        gt_generator = GroundTruthGenerator("./test_output/ground_truth")
        print("✅ GroundTruthGenerator initialized successfully")
        
        # Test output directory creation
        if gt_generator.output_dir.exists():
            print("✅ Output directory created")
        
        return True
        
    except Exception as e:
        print(f"❌ Ground truth generator test failed: {e}")
        return False


def test_repository_manager():
    """Test repository manager initialization."""
    print("\n🔍 Testing repository manager...")
    
    try:
        from src.repository_manager import RepositoryManager
        
        # Test initialization
        repo_manager = RepositoryManager("./test_output/repositories")
        print("✅ RepositoryManager initialized successfully")
        
        # Test repository listing
        repos = repo_manager.list_available_repositories()
        print(f"✅ Found {len(repos)} available repositories")
        
        return True
        
    except Exception as e:
        print(f"❌ Repository manager test failed: {e}")
        return False


def test_evaluator():
    """Test evaluator initialization."""
    print("\n🔍 Testing evaluator...")
    
    try:
        from src.evaluator import DocumentEvaluator
        
        # Test initialization
        evaluator = DocumentEvaluator()
        print("✅ DocumentEvaluator initialized successfully")
        
        # Test configuration access
        config = evaluator.config
        print(f"✅ Evaluator config loaded: {len(config.metrics)} metrics")
        
        return True
        
    except Exception as e:
        print(f"❌ Evaluator test failed: {e}")
        return False


def test_report_generator():
    """Test report generator initialization."""
    print("\n🔍 Testing report generator...")
    
    try:
        from src.report_generator import ReportGenerator
        
        # Test initialization
        report_gen = ReportGenerator("./test_output/reports")
        print("✅ ReportGenerator initialized successfully")
        
        # Test output directory creation
        if report_gen.output_dir.exists():
            print("✅ Reports directory created")
        
        return True
        
    except Exception as e:
        print(f"❌ Report generator test failed: {e}")
        return False


def test_benchmark_runner():
    """Test benchmark runner initialization."""
    print("\n🔍 Testing benchmark runner...")
    
    try:
        from src.benchmark_runner import BenchmarkRunner
        from src.models import BenchmarkConfig
        
        # Create test configuration
        config = BenchmarkConfig(
            test_files_dir="./test_files",
            output_dir="./test_output/benchmark",
            repositories_to_test=["marker"],
            enable_manual_evaluation=False,
            parallel_processing=False
        )
        
        # Test initialization
        runner = BenchmarkRunner(config)
        print("✅ BenchmarkRunner initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Benchmark runner test failed: {e}")
        return False


def test_dependencies():
    """Test if required dependencies are available."""
    print("\n🔍 Testing dependencies...")
    
    dependencies = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('plotly', 'plotly'),
        ('flask', 'flask'),
        ('yaml', 'pyyaml'),
        ('mammoth', 'mammoth'),
        ('docx', 'python-docx'),
    ]
    
    optional_dependencies = [
        ('bert_score', 'bert-score'),
        ('rouge_score', 'rouge-score'),
    ]
    
    all_good = True
    
    # Test required dependencies
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {package_name} available")
        except ImportError:
            print(f"❌ {package_name} not available")
            all_good = False
    
    # Test optional dependencies
    for module_name, package_name in optional_dependencies:
        try:
            __import__(module_name)
            print(f"✅ {package_name} available (optional)")
        except ImportError:
            print(f"⚠️  {package_name} not available (optional)")
    
    return all_good


def cleanup_test_files():
    """Clean up test files."""
    print("\n🧹 Cleaning up test files...")
    
    test_dirs = [
        "./test_output",
    ]
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            import shutil
            try:
                shutil.rmtree(test_dir)
                print(f"✅ Cleaned up {test_dir}")
            except Exception as e:
                print(f"⚠️  Could not clean up {test_dir}: {e}")


def main():
    """Run all tests."""
    print("🚀 Document Extraction Benchmark Framework - Installation Test")
    print("=" * 70)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Data Models", test_data_models),
        ("Ground Truth Generator", test_ground_truth_generator),
        ("Repository Manager", test_repository_manager),
        ("Evaluator", test_evaluator),
        ("Report Generator", test_report_generator),
        ("Benchmark Runner", test_benchmark_runner),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The framework is ready to use.")
        print("\nNext steps:")
        print("1. Create a 'test_files' directory with DOCX and PDF pairs")
        print("2. Run: python main.py list-repos")
        print("3. Run: python main.py run --test-files ./test_files --output ./results")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Check Python version (requires 3.8+)")
        print("3. Verify all files are in the correct locations")
    
    # Cleanup
    cleanup_test_files()
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
