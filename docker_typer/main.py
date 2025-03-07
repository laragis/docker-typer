from dataclasses import dataclass
import os
import subprocess
import time
from typing import Optional
import pendulum
from typer import secho, echo, Typer, Context, colors
import typer
from environs import env
from rich import print
from shlex import join, split
from functools import wraps
from pathlib import Path

from .settings import global_options

from .utils import docker_compose_command, get_compose_opts, log_execution_time, print_cmd, set_env_and_run

env.read_env()

app = Typer()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def local(ctx: Context):
    set_env_and_run(ctx, "local")


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def dev(ctx: Context):
    set_env_and_run(ctx, "development")
    

@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def prod(ctx: Context):
    set_env_and_run(ctx, "production")


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
def main(
    ctx: Context, 
    env_file: str = None, 
    working_dir: str = None, 
    dry_run: bool = False
): 
    if env_file: global_options.env_file = env_file
    if working_dir: global_options.working_dir = working_dir
    
    # docker-typer --env-file .env --working-dir ./ build
    # docker-typer build
    # docker-typer --env-file .env.prod prod build
    pass


if __name__ == "__main__":
    app()