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

from .settings import DEFAULT_ENV_FILE

from .utils import docker_compose_command, get_compose_opts, log_execution_time, print_cmd, set_env_and_run

app = Typer()

env.read_env()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def local(ctx: Context):
    set_env_and_run(ctx, "")


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def dev(ctx: Context):
    set_env_and_run(ctx, ".development")
    

@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def prod(ctx: Context):
    set_env_and_run(ctx, ".production")


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
@log_execution_time
def up(ctx: Context):
    docker_compose_command(ctx, "up")

        
@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
@log_execution_time
def down(ctx: Context):
    docker_compose_command(ctx, "down")
    

@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
@log_execution_time
def build(ctx: Context):
    docker_compose_command(ctx, "build")
    
    
@app.callback()
def main(verbose: bool = False):
    pass


if __name__ == "__main__":
    app()