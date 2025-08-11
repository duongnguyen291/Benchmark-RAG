"""
Manual evaluation interface module.
Provides web-based interface for human evaluation of extraction quality.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import webbrowser
import threading
import time

from .models import ManualEvaluation

logger = logging.getLogger(__name__)


class ManualEvaluationInterface:
    """Web-based interface for manual evaluation."""
    
    def __init__(self, evaluation_data_path: str):
        """Initialize manual evaluation interface.
        
        Args:
            evaluation_data_path: Path to evaluation data JSON file.
        """
        self.evaluation_data_path = Path(evaluation_data_path)
        self.evaluation_data = self._load_evaluation_data()
        self.current_item_index = 0
        self.evaluations = {}
        
        # Flask app
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _load_evaluation_data(self) -> Dict:
        """Load evaluation data from JSON file."""
        if not self.evaluation_data_path.exists():
            raise FileNotFoundError(f"Evaluation data file not found: {self.evaluation_data_path}")
        
        with open(self.evaluation_data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main evaluation page."""
            return self._render_evaluation_page()
        
        @self.app.route('/submit_evaluation', methods=['POST'])
        def submit_evaluation():
            """Submit evaluation for current item."""
            return self._handle_evaluation_submission()
        
        @self.app.route('/next_item')
        def next_item():
            """Move to next evaluation item."""
            return self._handle_next_item()
        
        @self.app.route('/previous_item')
        def previous_item():
            """Move to previous evaluation item."""
            return self._handle_previous_item()
        
        @self.app.route('/summary')
        def summary():
            """Show evaluation summary."""
            return self._render_summary_page()
        
        @self.app.route('/export_results')
        def export_results():
            """Export evaluation results."""
            return self._export_results()
    
    def _render_evaluation_page(self):
        """Render the main evaluation page."""
        if not self.evaluation_data.get('evaluation_items'):
            return "No evaluation items found."
        
        current_item = self.evaluation_data['evaluation_items'][self.current_item_index]
        
        # Load content files
        ground_truth_content = self._load_file_content(current_item['ground_truth_path'])
        extraction_content = self._load_file_content(current_item['extraction_path'])
        
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Manual Evaluation - Document Extraction Benchmark</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
                .container { max-width: 1400px; margin: 0 auto; }
                .header { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .progress { background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .content { display: flex; gap: 20px; }
                .panel { flex: 1; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .panel h3 { margin-top: 0; color: #333; }
                .content-area { border: 1px solid #ddd; padding: 15px; height: 400px; overflow-y: auto; background: #fafafa; font-family: monospace; white-space: pre-wrap; }
                .evaluation-form { background: white; padding: 20px; border-radius: 8px; margin-top: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .rating-group { margin: 15px 0; }
                .rating-group label { display: block; margin-bottom: 5px; font-weight: bold; }
                .rating-options { display: flex; gap: 10px; }
                .rating-option { display: flex; align-items: center; }
                .rating-option input { margin-right: 5px; }
                .navigation { display: flex; justify-content: space-between; margin-top: 20px; }
                .btn { padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
                .btn-primary { background: #007bff; color: white; }
                .btn-secondary { background: #6c757d; color: white; }
                .btn-success { background: #28a745; color: white; }
                .metrics { background: #e9ecef; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
                .metric { display: inline-block; margin-right: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Manual Evaluation - Document Extraction Benchmark</h1>
                    <p><strong>File:</strong> {{ current_item.file }} | <strong>Repository:</strong> {{ current_item.repository }}</p>
                </div>
                
                <div class="progress">
                    <h3>Progress</h3>
                    <p>Item {{ current_index + 1 }} of {{ total_items }} ({{ progress_percent }}%)</p>
                    <div style="background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden;">
                        <div style="background: #007bff; height: 100%; width: {{ progress_percent }}%;"></div>
                    </div>
                </div>
                
                <div class="metrics">
                    <h4>Automated Metrics:</h4>
                    <div class="metric"><strong>Overall Score:</strong> {{ "%.3f"|format(current_item.metrics.overall_score) }}</div>
                    <div class="metric"><strong>Content Similarity:</strong> {{ "%.3f"|format(current_item.metrics.content_similarity) }}</div>
                    <div class="metric"><strong>Structure Accuracy:</strong> {{ "%.3f"|format(current_item.metrics.structure_accuracy) }}</div>
                    <div class="metric"><strong>Formatting:</strong> {{ "%.3f"|format(current_item.metrics.formatting_preservation) }}</div>
                    <div class="metric"><strong>Table Quality:</strong> {{ "%.3f"|format(current_item.metrics.table_quality) }}</div>
                </div>
                
                <div class="content">
                    <div class="panel">
                        <h3>Ground Truth (DOCX → Markdown)</h3>
                        <div class="content-area">{{ ground_truth_content }}</div>
                    </div>
                    
                    <div class="panel">
                        <h3>Extracted Content (PDF → Markdown)</h3>
                        <div class="content-area">{{ extraction_content }}</div>
                    </div>
                </div>
                
                <div class="evaluation-form">
                    <h3>Manual Evaluation</h3>
                    <form method="POST" action="/submit_evaluation">
                        <div class="rating-group">
                            <label>Overall Quality (1-5):</label>
                            <div class="rating-options">
                                {% for i in range(1, 6) %}
                                <div class="rating-option">
                                    <input type="radio" name="overall_quality" value="{{ i }}" id="overall_{{ i }}" required>
                                    <label for="overall_{{ i }}">{{ i }}</label>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <div class="rating-group">
                            <label>Table Format Quality (1-5):</label>
                            <div class="rating-options">
                                {% for i in range(1, 6) %}
                                <div class="rating-option">
                                    <input type="radio" name="table_format_quality" value="{{ i }}" id="table_{{ i }}" required>
                                    <label for="table_{{ i }}">{{ i }}</label>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <div class="rating-group">
                            <label>Structure Preservation (1-5):</label>
                            <div class="rating-options">
                                {% for i in range(1, 6) %}
                                <div class="rating-option">
                                    <input type="radio" name="structure_preservation" value="{{ i }}" id="structure_{{ i }}" required>
                                    <label for="structure_{{ i }}">{{ i }}</label>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <div class="rating-group">
                            <label>Formatting Accuracy (1-5):</label>
                            <div class="rating-options">
                                {% for i in range(1, 6) %}
                                <div class="rating-option">
                                    <input type="radio" name="formatting_accuracy" value="{{ i }}" id="formatting_{{ i }}" required>
                                    <label for="formatting_{{ i }}">{{ i }}</label>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <div class="rating-group">
                            <label>Comments:</label>
                            <textarea name="comments" rows="4" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;" placeholder="Add your comments here..."></textarea>
                        </div>
                        
                        <div class="navigation">
                            <button type="button" class="btn btn-secondary" onclick="window.location.href='/previous_item'">Previous</button>
                            <button type="submit" class="btn btn-primary">Submit & Next</button>
                            <button type="button" class="btn btn-success" onclick="window.location.href='/summary'">View Summary</button>
                        </div>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        
        progress_percent = ((self.current_item_index + 1) / len(self.evaluation_data['evaluation_items'])) * 100
        
        return render_template_string(template,
                                    current_item=current_item,
                                    current_index=self.current_item_index,
                                    total_items=len(self.evaluation_data['evaluation_items']),
                                    progress_percent=progress_percent,
                                    ground_truth_content=ground_truth_content,
                                    extraction_content=extraction_content)
    
    def _render_summary_page(self):
        """Render evaluation summary page."""
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Evaluation Summary - Document Extraction Benchmark</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .summary { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }
                .stat-card { background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }
                .stat-value { font-size: 24px; font-weight: bold; color: #007bff; }
                .stat-label { color: #6c757d; margin-top: 5px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f8f9fa; font-weight: bold; }
                .btn { padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; margin: 5px; }
                .btn-primary { background: #007bff; color: white; }
                .btn-success { background: #28a745; color: white; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Evaluation Summary</h1>
                    <p>Manual evaluation results for document extraction benchmark</p>
                </div>
                
                <div class="summary">
                    <h2>Statistics</h2>
                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-value">{{ total_evaluations }}</div>
                            <div class="stat-label">Total Evaluations</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{{ "%.2f"|format(avg_overall_quality) }}</div>
                            <div class="stat-label">Avg Overall Quality</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{{ "%.2f"|format(avg_table_quality) }}</div>
                            <div class="stat-label">Avg Table Quality</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{{ "%.2f"|format(avg_structure_quality) }}</div>
                            <div class="stat-label">Avg Structure Quality</div>
                        </div>
                    </div>
                    
                    <h2>Repository Performance</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Repository</th>
                                <th>Evaluations</th>
                                <th>Avg Overall Quality</th>
                                <th>Avg Table Quality</th>
                                <th>Avg Structure Quality</th>
                                <th>Avg Formatting Quality</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for repo in repository_stats %}
                            <tr>
                                <td>{{ repo.name }}</td>
                                <td>{{ repo.count }}</td>
                                <td>{{ "%.2f"|format(repo.avg_overall) }}</td>
                                <td>{{ "%.2f"|format(repo.avg_table) }}</td>
                                <td>{{ "%.2f"|format(repo.avg_structure) }}</td>
                                <td>{{ "%.2f"|format(repo.avg_formatting) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    
                    <div style="margin-top: 20px;">
                        <a href="/" class="btn btn-primary">Continue Evaluation</a>
                        <a href="/export_results" class="btn btn-success">Export Results</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Calculate statistics
        total_evaluations = len(self.evaluations)
        if total_evaluations == 0:
            return "No evaluations submitted yet."
        
        avg_overall_quality = sum(eval_data['overall_quality'] for eval_data in self.evaluations.values()) / total_evaluations
        avg_table_quality = sum(eval_data['table_format_quality'] for eval_data in self.evaluations.values()) / total_evaluations
        avg_structure_quality = sum(eval_data['structure_preservation'] for eval_data in self.evaluations.values()) / total_evaluations
        
        # Repository statistics
        repo_stats = {}
        for item_id, eval_data in self.evaluations.items():
            repo = item_id.split('_')[1]  # Assuming format: file_repo
            if repo not in repo_stats:
                repo_stats[repo] = {'count': 0, 'overall': [], 'table': [], 'structure': [], 'formatting': []}
            
            repo_stats[repo]['count'] += 1
            repo_stats[repo]['overall'].append(eval_data['overall_quality'])
            repo_stats[repo]['table'].append(eval_data['table_format_quality'])
            repo_stats[repo]['structure'].append(eval_data['structure_preservation'])
            repo_stats[repo]['formatting'].append(eval_data['formatting_accuracy'])
        
        repository_stats = []
        for repo, stats in repo_stats.items():
            repository_stats.append({
                'name': repo,
                'count': stats['count'],
                'avg_overall': sum(stats['overall']) / len(stats['overall']),
                'avg_table': sum(stats['table']) / len(stats['table']),
                'avg_structure': sum(stats['structure']) / len(stats['structure']),
                'avg_formatting': sum(stats['formatting']) / len(stats['formatting'])
            })
        
        return render_template_string(template,
                                    total_evaluations=total_evaluations,
                                    avg_overall_quality=avg_overall_quality,
                                    avg_table_quality=avg_table_quality,
                                    avg_structure_quality=avg_structure_quality,
                                    repository_stats=repository_stats)
    
    def _handle_evaluation_submission(self):
        """Handle evaluation form submission."""
        try:
            evaluation = {
                'overall_quality': int(request.form['overall_quality']),
                'table_format_quality': int(request.form['table_format_quality']),
                'structure_preservation': int(request.form['structure_preservation']),
                'formatting_accuracy': int(request.form['formatting_accuracy']),
                'comments': request.form.get('comments', ''),
                'evaluator_name': request.form.get('evaluator_name', 'Anonymous'),
                'timestamp': time.time()
            }
            
            # Save evaluation
            current_item = self.evaluation_data['evaluation_items'][self.current_item_index]
            item_id = f"{current_item['file']}_{current_item['repository']}"
            self.evaluations[item_id] = evaluation
            
            # Move to next item
            if self.current_item_index < len(self.evaluation_data['evaluation_items']) - 1:
                self.current_item_index += 1
            
            return redirect('/')
            
        except Exception as e:
            logger.error(f"Error submitting evaluation: {e}")
            return "Error submitting evaluation", 400
    
    def _handle_next_item(self):
        """Handle next item navigation."""
        if self.current_item_index < len(self.evaluation_data['evaluation_items']) - 1:
            self.current_item_index += 1
        return redirect('/')
    
    def _handle_previous_item(self):
        """Handle previous item navigation."""
        if self.current_item_index > 0:
            self.current_item_index -= 1
        return redirect('/')
    
    def _export_results(self):
        """Export evaluation results."""
        results = {
            'evaluation_data': self.evaluation_data,
            'manual_evaluations': self.evaluations,
            'export_timestamp': time.time()
        }
        
        export_file = self.evaluation_data_path.parent / "manual_evaluation_results.json"
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        
        return jsonify({
            'message': 'Results exported successfully',
            'file': str(export_file)
        })
    
    def _load_file_content(self, file_path: str) -> str:
        """Load content from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            return f"Error loading file: {e}"
    
    def start_server(self, host: str = 'localhost', port: int = 5000, auto_open: bool = True):
        """Start the evaluation server."""
        if auto_open:
            # Open browser in a separate thread
            def open_browser():
                time.sleep(1)  # Wait for server to start
                webbrowser.open(f'http://{host}:{port}')
            
            threading.Thread(target=open_browser, daemon=True).start()
        
        logger.info(f"Starting manual evaluation server at http://{host}:{port}")
        self.app.run(host=host, port=port, debug=False)


def main():
    """Main function to start manual evaluation interface."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python manual_evaluation.py <evaluation_data.json>")
        sys.exit(1)
    
    evaluation_data_path = sys.argv[1]
    
    try:
        interface = ManualEvaluationInterface(evaluation_data_path)
        interface.start_server()
    except Exception as e:
        logger.error(f"Failed to start manual evaluation interface: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
