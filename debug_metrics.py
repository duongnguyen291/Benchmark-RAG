#!/usr/bin/env python3
"""
Debug script to check metrics calculation
"""

import sys
from pathlib import Path
from src.evaluator import DocumentEvaluator
from src.models import ExtractionResult, ProcessingTime

def debug_single_file():
    """Debug metrics for a single file"""
    
    # Setup paths
    ground_truth_file = Path("./your_data/ground_truth/[123doc] - File9.md")
    marker_file = Path("./your_data/extracted_files/marker_advance/[123doc] - File9.md")
    parsr_file = Path("./your_data/extracted_files/parsr/[123doc] - File9.md")
    
    # Initialize evaluator
    evaluator = DocumentEvaluator()
    
    # Read files
    with open(ground_truth_file, 'r', encoding='utf-8') as f:
        ground_truth_content = f.read()
    
    with open(marker_file, 'r', encoding='utf-8') as f:
        marker_content = f.read()
    
    with open(parsr_file, 'r', encoding='utf-8') as f:
        parsr_content = f.read()
    
    # Debug headers
    print("=== HEADER DEBUG ===")
    gt_headers = evaluator._extract_headers(ground_truth_content)
    marker_headers = evaluator._extract_headers(marker_content)
    parsr_headers = evaluator._extract_headers(parsr_content)
    
    print(f"Ground truth headers: {gt_headers}")
    print(f"Marker headers: {marker_headers}")
    print(f"Parsr headers: {parsr_headers}")
    print()
    
    # Create extraction results
    marker_result = ExtractionResult(
        file_path=str(ground_truth_file),
        repository_name="marker_advance",
        output_path=str(marker_file),
        processing_time=ProcessingTime(0.0, 0.0),
        success=True,
        output_content=marker_content
    )
    
    parsr_result = ExtractionResult(
        file_path=str(ground_truth_file),
        repository_name="parsr",
        output_path=str(parsr_file),
        processing_time=ProcessingTime(0.0, 0.0),
        success=True,
        output_content=parsr_content
    )
    
    # Evaluate
    print("=== MARKER ADVANCE ===")
    marker_eval = evaluator.evaluate_extraction(marker_result, str(ground_truth_file))
    print(f"Overall score: {marker_eval.overall_score:.3f}")
    print(f"Content similarity - word_overlap: {marker_eval.content_similarity.word_overlap:.3f}")
    print(f"Content similarity - rouge: {marker_eval.content_similarity.rouge_score:.3f}")
    print(f"Content similarity - bleu: {marker_eval.content_similarity.bleu_score:.3f}")
    print(f"Structure accuracy - header: {marker_eval.structure_accuracy.header_accuracy:.3f}")
    print(f"Structure accuracy - list: {marker_eval.structure_accuracy.list_accuracy:.3f}")
    print(f"Table quality - content: {marker_eval.table_quality.content_accuracy:.3f}")
    print(f"Table quality - structure: {marker_eval.table_quality.structure_preservation:.3f}")
    
    print("\n=== PARSR ===")
    parsr_eval = evaluator.evaluate_extraction(parsr_result, str(ground_truth_file))
    print(f"Overall score: {parsr_eval.overall_score:.3f}")
    print(f"Content similarity - word_overlap: {parsr_eval.content_similarity.word_overlap:.3f}")
    print(f"Content similarity - rouge: {parsr_eval.content_similarity.rouge_score:.3f}")
    print(f"Content similarity - bleu: {parsr_eval.content_similarity.bleu_score:.3f}")
    print(f"Structure accuracy - header: {parsr_eval.structure_accuracy.header_accuracy:.3f}")
    print(f"Structure accuracy - list: {parsr_eval.structure_accuracy.list_accuracy:.3f}")
    print(f"Table quality - content: {parsr_eval.table_quality.content_accuracy:.3f}")
    print(f"Table quality - structure: {parsr_eval.table_quality.structure_preservation:.3f}")

if __name__ == "__main__":
    debug_single_file()
