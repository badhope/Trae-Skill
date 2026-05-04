# Error Handler
# Comprehensive error handling and recovery system
# Thesis Specialist Platform v2.2

from typing import Dict, Optional, Any
from datetime import datetime
import traceback

class AgentError(Exception):
    """Base exception class for agent errors"""
    def __init__(self, code: str, message: str, solution: str = ""):
        super().__init__(message)
        self.code = code
        self.message = message
        self.solution = solution
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            'error_code': self.code,
            'error_message': self.message,
            'solution': self.solution,
            'timestamp': self.timestamp
        }

class ConfigurationError(AgentError):
    """Configuration errors"""
    def __init__(self, message: str, solution: str = ""):
        super().__init__('CONFIG_ERROR', message, solution)

class ExecutionError(AgentError):
    """Execution errors"""
    def __init__(self, message: str, solution: str = ""):
        super().__init__('EXECUTION_ERROR', message, solution)

class ValidationError(AgentError):
    """Validation errors"""
    def __init__(self, message: str, solution: str = ""):
        super().__init__('VALIDATION_ERROR', message, solution)

class ToolCallError(AgentError):
    """Tool call errors"""
    def __init__(self, message: str, solution: str = ""):
        super().__init__('TOOL_ERROR', message, solution)

class MemoryError(AgentError):
    """Memory operation errors"""
    def __init__(self, message: str, solution: str = ""):
        super().__init__('MEMORY_ERROR', message, solution)

class ErrorHandler:
    """Comprehensive error handler with recovery strategies"""

    def __init__(self):
        self.error_history = []
        self.recovery_attempts = {}

    def handle_error(self, error: AgentError, context: Dict = None) -> Dict:
        """Handle error and provide recovery suggestions"""
        error_record = {
            'error': error.to_dict(),
            'context': context or {},
            'recovered': False,
            'recovery_attempts': []
        }

        recovery_result = self._attempt_recovery(error, context)
        error_record['recovered'] = recovery_result['success']
        error_record['recovery_attempts'] = recovery_result['attempts']

        self.error_history.append(error_record)

        if len(self.error_history) > 100:
            self.error_history = self.error_history[-50:]

        return error_record

    def _attempt_recovery(self, error: AgentError, context: Dict = None) -> Dict:
        """Attempt to recover from error based on error type"""
        attempts = []
        success = False

        if error.code == 'CONFIG_ERROR':
            attempts, success = self._recover_from_config_error(error, context)
        elif error.code == 'EXECUTION_ERROR':
            attempts, success = self._recover_from_execution_error(error, context)
        elif error.code == 'VALIDATION_ERROR':
            attempts, success = self._recover_from_validation_error(error, context)
        elif error.code == 'TOOL_ERROR':
            attempts, success = self._recover_from_tool_error(error, context)
        elif error.code == 'MEMORY_ERROR':
            attempts, success = self._recover_from_memory_error(error, context)

        return {
            'success': success,
            'attempts': attempts
        }

    def _recover_from_config_error(self, error: AgentError, context: Dict) -> tuple:
        """Recovery strategy for configuration errors"""
        attempts = []
        attempts.append({
            'action': 'Check configuration file',
            'description': 'Verify agent.yaml exists and has correct format'
        })

        if context and 'file_path' in context:
            attempts.append({
                'action': 'Validate YAML syntax',
                'description': f'Check YAML syntax in {context["file_path"]}'
            })

        attempts.append({
            'action': 'Use defaults',
            'description': 'Fallback to default configuration'
        })

        return attempts, False

    def _recover_from_execution_error(self, error: AgentError, context: Dict) -> tuple:
        """Recovery strategy for execution errors"""
        attempts = []
        attempts.append({
            'action': 'Retry execution',
            'description': 'Retry the failed operation once'
        })

        if context and 'expert_id' in context:
            attempts.append({
                'action': 'Switch to default expert',
                'description': f'Fallback from {context["expert_id"]} to writing-expert'
            })

        attempts.append({
            'action': 'Simplify task',
            'description': 'Reduce task complexity'
        })

        expert_id = context.get('expert_id', 'unknown')
        if self.recovery_attempts.get(expert_id, 0) < 3:
            self.recovery_attempts[expert_id] = self.recovery_attempts.get(expert_id, 0) + 1
            return attempts, True

        return attempts, False

    def _recover_from_validation_error(self, error: AgentError, context: Dict) -> tuple:
        """Recovery strategy for validation errors"""
        attempts = []
        attempts.append({
            'action': 'Request clarification',
            'description': 'Ask user for more information'
        })
        attempts.append({
            'action': 'Use defaults',
            'description': 'Apply default values for missing fields'
        })
        return attempts, True

    def _recover_from_tool_error(self, error: AgentError, context: Dict) -> tuple:
        """Recovery strategy for tool errors"""
        attempts = []
        attempts.append({
            'action': 'Retry tool call',
            'description': 'Retry the tool call once'
        })
        if context and 'tool_id' in context:
            attempts.append({
                'action': 'Use alternative tool',
                'description': f'Find alternative for {context["tool_id"]}'
            })
        attempts.append({
            'action': 'Skip tool',
            'description': 'Continue without using the tool'
        })
        return attempts, True

    def _recover_from_memory_error(self, error: AgentError, context: Dict) -> tuple:
        """Recovery strategy for memory errors"""
        attempts = []
        attempts.append({
            'action': 'Retry memory operation',
            'description': 'Retry the memory read/write operation'
        })
        attempts.append({
            'action': 'Use in-memory cache',
            'description': 'Fallback to temporary in-memory storage'
        })
        attempts.append({
            'action': 'Continue without memory',
            'description': 'Proceed with fresh context'
        })
        return attempts, True

    def get_error_report(self) -> Dict:
        """Generate error report"""
        error_counts = {}
        for record in self.error_history:
            code = record['error']['error_code']
            error_counts[code] = error_counts.get(code, 0) + 1

        return {
            'total_errors': len(self.error_history),
            'error_distribution': error_counts,
            'recovered_count': sum(1 for r in self.error_history if r['recovered']),
            'recovery_rate': sum(1 for r in self.error_history if r['recovered']) / max(len(self.error_history), 1)
        }

    def log_exception(self, exception: Exception, context: Dict = None):
        """Log unexpected exceptions"""
        error_info = {
            'type': type(exception).__name__,
            'message': str(exception),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'timestamp': datetime.now().isoformat()
        }

        self.error_history.append({
            'error': error_info,
            'context': context or {},
            'recovered': False,
            'recovery_attempts': []
        })

        import logging
        logger = logging.getLogger('agent-error-handler')
        logger.error(f"Unexpected exception: {type(exception).__name__}: {exception}", exc_info=True)

    def clear_history(self):
        """Clear error history"""
        self.error_history.clear()
        self.recovery_attempts.clear()

if __name__ == '__main__':
    handler = ErrorHandler()

    try:
        raise ConfigurationError('Missing required config section', 'Check agent.yaml')
    except AgentError as e:
        result = handler.handle_error(e, {'file_path': 'agent.yaml'})
        print(f"Handled error: {result['error']['error_code']}")
        print(f"Recovered: {result['recovered']}")

    print("\nError Report:")
    print(handler.get_error_report())
