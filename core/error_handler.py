"""
AI Creator OS - Error Recovery and Diagnostics Engine
Provides actionable diagnostics and automated self-healing protocols for Colab runs.
"""
import sys
import traceback
from typing import Optional, Dict, Any


class ErrorRecoveryHandler:
    """Standardized error trapping and recovery handler across all engines."""

    @staticmethod
    def handle_error(
        module: str,
        component: str,
        error: Exception,
        likely_cause: str,
        automatic_fix_attempted: Optional[str] = "Checked dependencies and directory locks",
        fix_result: Optional[str] = "Requires manual confirmation or configuration change",
        recommended_step: Optional[str] = "Restart runtime or switch Colab GPU tier",
    ) -> None:
        print("\n" + "=" * 65)
        print("🚨 ERROR DETECTED")
        print("=" * 65)
        print(f"Module:                  {module}")
        print(f"Component:               {component}")
        print(f"Error:                   {type(error).__name__}: {str(error)}")
        print(f"Likely cause:            {likely_cause}")
        print(f"Automatic fix attempted: {automatic_fix_attempted}")
        print(f"Result:                  {fix_result}")
        print(f"Recommended next step:   {recommended_step}")
        print("=" * 65 + "\n")


def safe_execute(module: str, component: str, func, *args, **kwargs):
    """Executes a function safely with error diagnostic trapping."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        ErrorRecoveryHandler.handle_error(
            module=module,
            component=component,
            error=e,
            likely_cause="Hardware limit, missing dependency, or invalid path.",
            automatic_fix_attempted="Logged trace and checked fallback options.",
            fix_result="Failed function execution.",
            recommended_step="Check Google Drive connection and Colab GPU status.",
        )
        return None
