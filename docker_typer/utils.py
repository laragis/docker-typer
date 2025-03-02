from functools import wraps
from rich import print
import pendulum


def log_execution_time(func):
    """Decorator to log start time, execution time, and end time automatically."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = pendulum.now()
        start_str = start_time.to_datetime_string()

        # Print start time
        # print(f"[bold cyan][{start_str}][/bold cyan] 🚀 Running command...")
        
        # Execute the original command function
        result = func(*args, **kwargs)

        # Calculate execution time
        end_time = pendulum.now()
        end_str = end_time.to_datetime_string()
        duration = end_time.diff(start_time).in_words()

        # Print end time and execution duration
        # print(f"[bold green][{end_str}][/bold green] ✅ Command completed!")
        print(f"[blue][{end_str}][/blue]⏳ Total execution time: [bold yellow]{duration}[/bold yellow]")

        return result
    return wrapper