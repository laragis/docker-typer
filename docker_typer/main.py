import os
import subprocess
import time
import pendulum
from typer import secho, echo, Typer, Context, colors
import typer
from environs import env
from rich import print
from shlex import join, split
from functools import wraps

from .utils import log_execution_time

app = Typer()

env.read_env()

APP_ENV = env("APP_ENV", default="local")

DEFAULT_ENV_FILE = ".env"

def get_compose_opts():
    opts = []
    
    if APP_ENV != "local":
        env_file = env("_ENV_FILE")
        opts = [*opts, "--env-file", env_file]
        
        compose_file = "docker-compose.yml" if APP_ENV == "local" else f"docker-compose.{APP_ENV}.yml"
        opts = [*opts, "--file", compose_file]
        
    return opts

@app.callback()
def callback():
    """
    Awesome Docker Typer
    """
    

@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def local(ctx: Context):
    os.environ["_ENV_FILE"] = DEFAULT_ENV_FILE
    env.read_env(env('_ENV_FILE'), override=True)
    
    echo("Local")
    subprocess.run(f"docker-typer " + " ".join(ctx.args), shell=True, check=True)


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def dev(ctx: Context):
    os.environ["_ENV_FILE"] = DEFAULT_ENV_FILE + ".development"
    env.read_env(env('_ENV_FILE'), override=True)
    
    echo("Development")
    subprocess.run(f"docker-typer " + " ".join(ctx.args), shell=True, check=True)
    

@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def prod(ctx: Context):
    os.environ["_ENV_FILE"] = DEFAULT_ENV_FILE + ".production"
    env.read_env(env('_ENV_FILE'), override=True)
    echo("Production")
    subprocess.run(f"docker-typer " + " ".join(ctx.args), shell=True, check=True)
    
@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def up(ctx: Context):
    command = ['docker', 'compose', *get_compose_opts(), "up", *ctx.args]
    # command = ['lss', '-al']
    echo(join(command))
    # subprocess.run(command, check=True)

        
@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def down(ctx: Context):
    command = ['docker', 'compose', *get_compose_opts(), "down", *ctx.args]
    subprocess.run(command, check=True)
    



@app.command()
@log_execution_time
def build():
    calc_time = pendulum.now().to_datetime_string()
    print(f"[blue][{calc_time}][/blue] 🔎 docker compose build")
    
    time.sleep(5)
    
    
    
@app.callback()
def main(verbose: bool = False):
    pass


if __name__ == "__main__":
    app()