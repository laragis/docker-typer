import typer

import items
import users

app = typer.Typer()
app.add_typer(users.app, name="users")
app.add_typer(items.app, name="items")

@app.command()
def conquer(name: str):
    print(f"Conquering reign: {name}")


@app.command()
def destroy(name: str):
    print(f"Destroying reign: {name}")

if __name__ == "__main__":
    app()