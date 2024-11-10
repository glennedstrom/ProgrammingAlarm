# app/utils/challenge_manager.py

import os
import yaml
import logging
from pathlib import Path
import random
import markdown
from typing import Dict, List, Optional, Any
import traceback

class ProgrammingChallenge:
    """Represents a single programming challenge."""
    def __init__(self, name: str, description: str, starter_code: str, test_cases: List[Dict[str, Any]]):
        self.name = name
        self.description = markdown.markdown(description)  # Convert MD to HTML
        self.starter_code = starter_code
        self.test_cases = test_cases

    def __repr__(self):
        return f"ProgrammingChallenge(name='{self.name}')"

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'starter_code': self.starter_code,
            'test_cases': self.test_cases
        }

class TestResult:
    """Represents the result of a single test case."""
    def __init__(self, passed: bool, description: str, input_data: Any, 
                 expected: Any, actual: Any, error: Optional[str] = None):
        self.passed = passed
        self.description = description
        self.input = input_data
        self.expected = expected
        self.actual = actual
        self.error = error

    def to_dict(self):
        return {
            'passed': self.passed,
            'description': self.description,
            'input': self.input,
            'expected': self.expected,
            'actual': self.actual,
            'error': self.error
        }

class ChallengeManager:
    """Manages loading and testing programming challenges."""
    def __init__(self):
        self.problems_dir = Path(__file__).parent.parent / 'problems'
        self.challenges: Dict[str, ProgrammingChallenge] = {}
        self.load_all_challenges()
    
    def load_all_challenges(self):
        """Load all challenges from the problems directory."""
        if not self.problems_dir.exists():
            logging.error(f"Problems directory not found at {self.problems_dir}")
            raise FileNotFoundError(f"Problems directory not found at {self.problems_dir}")
        
        logging.info("Loading programming challenges...")
        
        for problem_dir in self.problems_dir.iterdir():
            if problem_dir.is_dir():
                try:
                    self.load_challenge(problem_dir)
                    logging.info(f"Loaded challenge: {problem_dir.name}")
                except Exception as e:
                    logging.error(f"Error loading challenge {problem_dir.name}: {e}")
    
    def load_challenge(self, problem_dir: Path):
        """Load a single challenge from its directory."""
        # Check for required files
        required_files = ['instructions.md', 'starter.py', 'tests.yaml']
        for file in required_files:
            if not (problem_dir / file).exists():
                raise FileNotFoundError(f"Missing required file {file} in {problem_dir}")
        
        # Read all challenge files
        with open(problem_dir / 'instructions.md', 'r', encoding='utf-8') as f:
            description = f.read()
        
        with open(problem_dir / 'starter.py', 'r', encoding='utf-8') as f:
            starter_code = f.read()
        
        with open(problem_dir / 'tests.yaml', 'r', encoding='utf-8') as f:
            try:
                test_cases = yaml.safe_load(f)
            except yaml.YAMLError as e:
                logging.error(f"Error parsing tests.yaml in {problem_dir}: {e}")
                raise
        
        # Validate test cases format
        self._validate_test_cases(test_cases, problem_dir.name)
        
        # Create and store challenge object
        challenge = ProgrammingChallenge(
            name=problem_dir.name,
            description=description,
            starter_code=starter_code,
            test_cases=test_cases
        )
        
        self.challenges[problem_dir.name] = challenge
    
    def _validate_test_cases(self, test_cases: List[Dict], challenge_name: str):
        """Validate the format of test cases."""
        if not isinstance(test_cases, list):
            raise ValueError(f"Test cases for {challenge_name} must be a list")
        
        required_keys = {'function', 'description', 'input', 'expected'}
        for i, test in enumerate(test_cases, 1):
            if not isinstance(test, dict):
                raise ValueError(f"Test case {i} in {challenge_name} must be a dictionary")
            
            missing_keys = required_keys - test.keys()
            if missing_keys:
                raise ValueError(
                    f"Test case {i} in {challenge_name} missing required keys: {missing_keys}"
                )
    
    def get_random_challenge(self) -> Optional[ProgrammingChallenge]:
        """Return a random challenge from the available problems."""
        if not self.challenges:
            raise ValueError("No challenges available")
        return random.choice(list(self.challenges.values()))
    
    def get_challenge(self, name: str) -> Optional[ProgrammingChallenge]:
        """Get a specific challenge by name."""
        return self.challenges.get(name)
    
    def test_solution(self, challenge_id: str, solution_code: str) -> Dict[str, Any]:
        """Test a solution against all test cases for a challenge."""
        challenge = self.get_challenge(challenge_id)
        if not challenge:
            return {'error': 'Challenge not found'}
        
        namespace = {}
        results = []
        all_passed = True
        
        try:
            # Execute the solution code
            exec(solution_code, namespace)
            
            # Run each test case
            for test in challenge.test_cases:
                try:
                    # Get the function to test
                    func = namespace[test['function']]
                    
                    # Call function with appropriate parameters
                    if isinstance(test['input'], dict):
                        actual = func(**test['input'])
                    else:
                        actual = func(test['input'])
                    
                    # Compare result
                    passed = actual == test['expected']
                    all_passed = all_passed and passed
                    
                    # Store result
                    result = TestResult(
                        passed=passed,
                        description=test['description'],
                        input_data=test['input'],
                        expected=test['expected'],
                        actual=actual
                    )
                    
                except Exception as e:
                    all_passed = False
                    result = TestResult(
                        passed=False,
                        description=test['description'],
                        input_data=test['input'],
                        expected=test['expected'],
                        actual=None,
                        error=str(e)
                    )
                    
                results.append(result.to_dict())
            
            return {
                'all_passed': all_passed,
                'test_results': results
            }
            
        except Exception as e:
            return {
                'error': f"Error executing solution: {str(e)}",
                'traceback': traceback.format_exc()
            }

    def reload_challenges(self):
        """Reload all challenges from disk."""
        self.challenges.clear()
        self.load_all_challenges()
    
    def list_challenges(self) -> List[str]:
        """Return a list of available challenge names."""
        return sorted(self.challenges.keys())
    
    def get_challenge_count(self) -> int:
        """Return the number of available challenges."""
        return len(self.challenges)

    def get_challenge_details(self, name: str) -> Optional[Dict]:
        """Get detailed information about a challenge."""
        challenge = self.get_challenge(name)
        if challenge:
            return challenge.to_dict()
        return None
