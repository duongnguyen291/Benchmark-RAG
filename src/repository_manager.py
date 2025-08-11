"""
Repository management module.
Handles setup, execution, and management of GitHub repositories for extraction.
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
import json
import time

from .config import config_manager, RepositoryConfig
from .models import ExtractionResult, ProcessingTime

logger = logging.getLogger(__name__)


class RepositoryManager:
    """Manages GitHub repositories for document extraction."""
    
    def __init__(self, repos_dir: str = "repositories"):
        """Initialize repository manager.
        
        Args:
            repos_dir: Directory to store cloned repositories.
        """
        self.repos_dir = Path(repos_dir)
        self.repos_dir.mkdir(parents=True, exist_ok=True)
        self.repositories = config_manager.get_repositories()
        self.setup_status = {}
    
    def setup_repository(self, repo_id: str) -> bool:
        """Setup a specific repository.
        
        Args:
            repo_id: Repository identifier.
            
        Returns:
            True if setup successful, False otherwise.
        """
        if repo_id not in self.repositories:
            logger.error(f"Repository {repo_id} not found in configuration")
            return False
        
        repo_config = self.repositories[repo_id]
        repo_path = self.repos_dir / repo_id
        
        try:
            # Check if already setup
            if repo_path.exists() and self._is_repository_ready(repo_id):
                logger.info(f"Repository {repo_id} already setup")
                self.setup_status[repo_id] = True
                return True
            
            # Clone repository if not exists
            if not repo_path.exists():
                logger.info(f"Cloning repository {repo_id}...")
                self._clone_repository(repo_config, repo_path)
            
            # Run setup commands
            logger.info(f"Running setup commands for {repo_id}...")
            self._run_setup_commands(repo_config, repo_path)
            
            self.setup_status[repo_id] = True
            logger.info(f"Repository {repo_id} setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup repository {repo_id}: {e}")
            self.setup_status[repo_id] = False
            return False
    
    def setup_all_repositories(self, repo_ids: Optional[List[str]] = None) -> Dict[str, bool]:
        """Setup multiple repositories.
        
        Args:
            repo_ids: List of repository IDs to setup. If None, setup all.
            
        Returns:
            Dictionary mapping repo_id to setup success status.
        """
        if repo_ids is None:
            repo_ids = list(self.repositories.keys())
        
        results = {}
        for repo_id in repo_ids:
            results[repo_id] = self.setup_repository(repo_id)
        
        return results
    
    def extract_with_repository(self, repo_id: str, input_file: str, output_dir: str) -> ExtractionResult:
        """Extract document using a specific repository.
        
        Args:
            repo_id: Repository identifier.
            input_file: Path to input file (PDF).
            output_dir: Directory to save output.
            
        Returns:
            ExtractionResult with results and timing information.
        """
        if repo_id not in self.repositories:
            raise ValueError(f"Repository {repo_id} not found")
        
        if not self.setup_status.get(repo_id, False):
            raise RuntimeError(f"Repository {repo_id} not properly setup")
        
        repo_config = self.repositories[repo_id]
        repo_path = self.repos_dir / repo_id
        output_path = Path(output_dir) / f"{Path(input_file).stem}_{repo_id}.md"
        
        start_time = time.time()
        
        try:
            # Prepare command
            command = self._prepare_extract_command(
                repo_config, input_file, str(output_path), repo_path
            )
            
            # Execute extraction
            logger.info(f"Running extraction with {repo_id}...")
            result = self._execute_extract_command(command, repo_path)
            
            end_time = time.time()
            processing_time = ProcessingTime(
                total_time=end_time - start_time,
                extraction_time=end_time - start_time
            )
            
            # Read output content
            output_content = None
            if output_path.exists():
                with open(output_path, 'r', encoding='utf-8') as f:
                    output_content = f.read()
            
            return ExtractionResult(
                file_path=input_file,
                repository_name=repo_config.name,
                output_path=str(output_path),
                processing_time=processing_time,
                success=result['success'],
                error_message=result.get('error'),
                output_content=output_content
            )
            
        except Exception as e:
            end_time = time.time()
            processing_time = ProcessingTime(
                total_time=end_time - start_time,
                extraction_time=end_time - start_time
            )
            
            logger.error(f"Extraction failed for {repo_id}: {e}")
            return ExtractionResult(
                file_path=input_file,
                repository_name=repo_config.name,
                output_path=str(output_path),
                processing_time=processing_time,
                success=False,
                error_message=str(e)
            )
    
    def _clone_repository(self, repo_config: RepositoryConfig, repo_path: Path):
        """Clone repository from GitHub."""
        try:
            subprocess.run(
                ["git", "clone", repo_config.repo_url, str(repo_path)],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to clone repository: {e.stderr}")
    
    def _run_setup_commands(self, repo_config: RepositoryConfig, repo_path: Path):
        """Run setup commands for repository."""
        for command in repo_config.setup_commands:
            try:
                logger.debug(f"Running command: {command}")
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutes timeout
                )
                
                if result.returncode != 0:
                    logger.warning(f"Setup command failed: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                raise RuntimeError(f"Setup command timed out: {command}")
            except Exception as e:
                logger.warning(f"Setup command error: {e}")
    
    def _prepare_extract_command(self, repo_config: RepositoryConfig, 
                                input_file: str, output_path: str, repo_path: Path) -> str:
        """Prepare extraction command with proper substitutions."""
        command = repo_config.extract_command
        
        # Replace placeholders
        command = command.replace("{input_file}", input_file)
        command = command.replace("{output_file}", output_path)
        command = command.replace("{output_dir}", str(Path(output_path).parent))
        
        return command
    
    def _execute_extract_command(self, command: str, repo_path: Path) -> Dict[str, any]:
        """Execute extraction command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'error': result.stderr if result.returncode != 0 else None
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timed out'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _is_repository_ready(self, repo_id: str) -> bool:
        """Check if repository is ready for use."""
        repo_path = self.repos_dir / repo_id
        
        # Basic checks
        if not repo_path.exists():
            return False
        
        # Check for .git directory (indicating it's a git repository)
        if not (repo_path / ".git").exists():
            return False
        
        # Additional checks can be added here based on repository type
        return True
    
    def get_repository_info(self, repo_id: str) -> Optional[Dict[str, any]]:
        """Get information about a repository."""
        if repo_id not in self.repositories:
            return None
        
        repo_config = self.repositories[repo_id]
        repo_path = self.repos_dir / repo_id
        
        info = {
            'name': repo_config.name,
            'description': repo_config.description,
            'repo_url': repo_config.repo_url,
            'local_path': str(repo_path),
            'is_setup': self.setup_status.get(repo_id, False),
            'exists': repo_path.exists()
        }
        
        return info
    
    def cleanup_repository(self, repo_id: str):
        """Clean up a repository (remove local copy)."""
        repo_path = self.repos_dir / repo_id
        if repo_path.exists():
            shutil.rmtree(repo_path)
            logger.info(f"Cleaned up repository {repo_id}")
    
    def list_available_repositories(self) -> List[str]:
        """List all available repository IDs."""
        return list(self.repositories.keys())
    
    def get_setup_status(self) -> Dict[str, bool]:
        """Get setup status of all repositories."""
        return self.setup_status.copy()
