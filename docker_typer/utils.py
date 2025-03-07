from functools import wraps
import os
import subprocess
from environs import env
from rich import print
import pendulum
from shlex import join, split
from typer import Context, echo
from .settings import APP_ENV, global_options, DEFAULT_ENV_FILE


def get_calc_time_style():
    calc_time = pendulum.now().to_datetime_string()
    return f"[blue][{calc_time}][/blue]"


def print_cmd(cmd):
    print(f"{get_calc_time_style()} == ▶️  [green]{join(cmd)}[/green] ==")


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
        print(f"[blue][{end_str}][/blue] == ⏳ Total execution time: [bold yellow]{duration}[/bold yellow] ==")

        return result
    return wrapper

def get_compose_opts():
    opts = []
    
    if APP_ENV != "local":
        opts = [*opts, "--env-file", env("_ENV_FILE")]
        
        compose_file = "docker-compose.yml" if APP_ENV == "local" else f"docker-compose.{APP_ENV}.yml"
        opts = [*opts, "--file", compose_file]
        
    return opts

def docker_compose_command(ctx: Context, command: str):
    cmd = ["docker", "compose", *get_compose_opts(), command, *ctx.args]
    print_cmd(cmd)
    subprocess.run(cmd, check=True)
    
    
def set_env_and_run(ctx: Context, mode: str):
    env_file_suffix = DEFAULT_ENV_FILE if mode == "local" else f".{mode}"
    env_file = global_options.env_file if global_options.is_dirty("env_file") else f"{DEFAULT_ENV_FILE}{env_file_suffix}"
    
    os.environ["_ENV_FILE"] = env_file
    env.read_env(env_file, override=True)
    
    match mode:
        case "local":
            print(f"{(get_calc_time_style())} 🚀 Running on [bold green]**Local**[/bold green] environment. This is your personal development machine.")
        case "development":
            print(f"{(get_calc_time_style())} 👨‍💻 Running on [bold green]**Development**[/bold green] environment. Used for coding, debugging, and integration.")
        case "testing":
            print(f"{(get_calc_time_style())} 🧪 Running on [bold green]**Testing**[/bold green] environment. Used for QA and automated tests.")
        case "staging":
            print(f"{(get_calc_time_style())} 📦 Running on [bold green]**Staging**[/bold green] environment. Mirrors production for final verification.")
        case "production":
            print(f"{(get_calc_time_style())} 🌍 Running on [bold green]**Production**[/bold green] environment. Live system used by real users. ")
            
    subprocess.run(split(f"docker-typer {' '.join(ctx.args)}"), check=True)