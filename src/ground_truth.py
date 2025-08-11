"""
Ground truth generation module.
Handles conversion of DOCX files to Markdown for use as ground truth.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple
import mammoth
from docx import Document
import logging

from .config import config_manager
from .models import ProcessingTime

logger = logging.getLogger(__name__)


class GroundTruthGenerator:
    """Generates ground truth Markdown from DOCX files."""
    
    def __init__(self, output_dir: str):
        """Initialize ground truth generator.
        
        Args:
            output_dir: Directory to save generated ground truth files.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = config_manager.get_ground_truth_config()
    
    def generate_ground_truth(self, docx_file: str) -> Tuple[str, ProcessingTime]:
        """Generate ground truth Markdown from DOCX file.
        
        Args:
            docx_file: Path to the DOCX file.
            
        Returns:
            Tuple of (output_path, processing_time)
        """
        docx_path = Path(docx_file)
        if not docx_path.exists():
            raise FileNotFoundError(f"DOCX file not found: {docx_file}")
        
        # Generate output filename
        output_filename = docx_path.stem + "_ground_truth.md"
        output_path = self.output_dir / output_filename
        
        start_time = self._get_time()
        
        try:
            if self.config.tool == "mammoth":
                output_path, processing_time = self._convert_with_mammoth(
                    docx_file, output_path
                )
            else:
                raise ValueError(f"Unsupported ground truth tool: {self.config.tool}")
            
            logger.info(f"Generated ground truth: {output_path}")
            return str(output_path), processing_time
            
        except Exception as e:
            logger.error(f"Failed to generate ground truth for {docx_file}: {e}")
            raise
    
    def _convert_with_mammoth(self, docx_file: str, output_path: Path) -> Tuple[str, ProcessingTime]:
        """Convert DOCX to Markdown using mammoth."""
        start_time = self._get_time()
        
        try:
            # Read DOCX file
            with open(docx_file, "rb") as docx:
                # Convert to HTML first for better formatting preservation
                html_result = mammoth.convert_to_html(docx)
                html_content = html_result.value
                
                # Convert HTML to Markdown
                markdown_content = self._html_to_markdown(html_content)
                
                # Write to file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                end_time = self._get_time()
                processing_time = ProcessingTime(
                    total_time=end_time - start_time,
                    extraction_time=end_time - start_time
                )
                
                return str(output_path), processing_time
                
        except Exception as e:
            logger.error(f"Mammoth conversion failed: {e}")
            raise
    
    def _html_to_markdown(self, html_content: str) -> str:
        """Convert HTML content to Markdown format."""
        import re
        
        # Basic HTML to Markdown conversion
        markdown = html_content
        
        # Headers
        markdown = re.sub(r'<h1>(.*?)</h1>', r'# \1', markdown)
        markdown = re.sub(r'<h2>(.*?)</h2>', r'## \1', markdown)
        markdown = re.sub(r'<h3>(.*?)</h3>', r'### \1', markdown)
        markdown = re.sub(r'<h4>(.*?)</h4>', r'#### \1', markdown)
        markdown = re.sub(r'<h5>(.*?)</h5>', r'##### \1', markdown)
        markdown = re.sub(r'<h6>(.*?)</h6>', r'###### \1', markdown)
        
        # Bold and italic
        markdown = re.sub(r'<strong>(.*?)</strong>', r'**\1**', markdown)
        markdown = re.sub(r'<b>(.*?)</b>', r'**\1**', markdown)
        markdown = re.sub(r'<em>(.*?)</em>', r'*\1*', markdown)
        markdown = re.sub(r'<i>(.*?)</i>', r'*\1*', markdown)
        
        # Links
        markdown = re.sub(r'<a href="([^"]*)">(.*?)</a>', r'[\2](\1)', markdown)
        
        # Lists
        markdown = re.sub(r'<ul>(.*?)</ul>', r'\1', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<ol>(.*?)</ol>', r'\1', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<li>(.*?)</li>', r'- \1', markdown)
        
        # Paragraphs
        markdown = re.sub(r'<p>(.*?)</p>', r'\1\n\n', markdown)
        
        # Line breaks
        markdown = re.sub(r'<br/?>', r'\n', markdown)
        
        # Tables - basic conversion
        markdown = re.sub(r'<table>(.*?)</table>', r'\n\1\n', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<tr>(.*?)</tr>', r'\1\n', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<td>(.*?)</td>', r'|\1', markdown)
        markdown = re.sub(r'<th>(.*?)</th>', r'|\1', markdown)
        
        # Clean up extra whitespace
        markdown = re.sub(r'\n\s*\n\s*\n', r'\n\n', markdown)
        markdown = markdown.strip()
        
        return markdown
    
    def _get_time(self) -> float:
        """Get current time in seconds."""
        import time
        return time.time()
    
    def batch_generate(self, docx_files: list) -> dict:
        """Generate ground truth for multiple DOCX files.
        
        Args:
            docx_files: List of DOCX file paths.
            
        Returns:
            Dictionary mapping input files to output paths and processing times.
        """
        results = {}
        
        for docx_file in docx_files:
            try:
                output_path, processing_time = self.generate_ground_truth(docx_file)
                results[docx_file] = {
                    'output_path': output_path,
                    'processing_time': processing_time,
                    'success': True
                }
            except Exception as e:
                logger.error(f"Failed to process {docx_file}: {e}")
                results[docx_file] = {
                    'output_path': None,
                    'processing_time': None,
                    'success': False,
                    'error': str(e)
                }
        
        return results
    
    def validate_ground_truth(self, ground_truth_path: str) -> bool:
        """Validate generated ground truth file.
        
        Args:
            ground_truth_path: Path to the ground truth file.
            
        Returns:
            True if valid, False otherwise.
        """
        try:
            with open(ground_truth_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic validation checks
            if len(content.strip()) == 0:
                logger.warning(f"Ground truth file is empty: {ground_truth_path}")
                return False
            
            # Check for basic markdown structure
            if not any(line.startswith('#') for line in content.split('\n')):
                logger.warning(f"No headers found in ground truth: {ground_truth_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate ground truth {ground_truth_path}: {e}")
            return False
