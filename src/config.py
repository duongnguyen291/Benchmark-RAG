"""
Configuration management for the benchmark framework.
Handles loading and validating configuration from YAML files.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class RepositoryConfig:
    """Configuration for a single repository."""
    name: str
    repo_url: str
    description: str
    setup_commands: List[str]
    extract_command: str
    output_format: str
    supported_formats: List[str]


@dataclass
class GroundTruthConfig:
    """Configuration for ground truth generation."""
    tool: str
    command: str
    description: str


@dataclass
class EvaluationConfig:
    """Configuration for evaluation metrics."""
    metrics: List[str]
    bert_score: Dict[str, Any]
    manual_evaluation: Dict[str, Any]


class ConfigManager:
    """Manages configuration loading and validation."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file. If None, uses default.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "repos_config.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _validate_config(self):
        """Validate configuration structure."""
        required_sections = ['repositories', 'ground_truth', 'evaluation']
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
    
    def get_repositories(self) -> Dict[str, RepositoryConfig]:
        """Get repository configurations."""
        repos = {}
        for repo_id, repo_data in self.config['repositories'].items():
            repos[repo_id] = RepositoryConfig(
                name=repo_data['name'],
                repo_url=repo_data['repo_url'],
                description=repo_data['description'],
                setup_commands=repo_data['setup_commands'],
                extract_command=repo_data['extract_command'],
                output_format=repo_data['output_format'],
                supported_formats=repo_data['supported_formats']
            )
        return repos
    
    def get_ground_truth_config(self) -> GroundTruthConfig:
        """Get ground truth configuration."""
        gt_data = self.config['ground_truth']['docx_to_markdown']
        return GroundTruthConfig(
            tool=gt_data['tool'],
            command=gt_data['command'],
            description=gt_data['description']
        )
    
    def get_evaluation_config(self) -> EvaluationConfig:
        """Get evaluation configuration."""
        eval_data = self.config['evaluation']
        return EvaluationConfig(
            metrics=eval_data['metrics'],
            bert_score=eval_data['bert_score'],
            manual_evaluation=eval_data['manual_evaluation']
        )
    
    def get_repository(self, repo_id: str) -> Optional[RepositoryConfig]:
        """Get configuration for a specific repository."""
        repos = self.get_repositories()
        return repos.get(repo_id)
    
    def list_repositories(self) -> List[str]:
        """List all available repository IDs."""
        return list(self.config['repositories'].keys())


# Global configuration instance
config_manager = ConfigManager()
