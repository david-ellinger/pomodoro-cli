import typer
import time
from db import Database

app = typer.Typer()
db = Database()
db.set("completed_times", 0)


@app.command()
def init(
    default_time: int = typer.Option(25, prompt=True),
    short_break: int = typer.Option(5, prompt=True),
    long_break: int = typer.Option(15, prompt=True),
) -> None:
    data = {
        "default_time": default_time,
        "short_break": short_break,
        "long_break": long_break,
    }
    create = typer.confirm(f"Are you sure? {data=}")
    if not create:
        typer.echo("Not creating")
        raise typer.Abort()
    typer.echo("Creating...")
    db.set_redis_values(data)


@app.command()
def start():
    data = get_data()
    break_time = data["completed_times"]
    default_time = data["default_time"]
    typer.echo("[*] Started Pomodoro")
    incremental_sleep(default_time)

    typer.echo("[*] Completed Pomodoro")
    db.db.incrby("completed_times", 1)
    start_rest = typer.confirm("Start rest?")
    if not start_rest:
        typer.echo("Existing...")
        typer.Abort()
    incremental_sleep(break_time)
    typer.echo("[*] Session Finished")


def incremental_sleep(sleep_time: int) -> None:
    pomodoro_chunks = [1 for _ in range(sleep_time)]
    for t in pomodoro_chunks:
        time.sleep(60 * t)
        typer.echo("[-] 1 min passed")


def get_data() -> dict:
    data = {
        "fourth_time": False,
        "break_time": 0,
    }
    data["break_time"] = db.db.incrby("short_break", 0)
    data["default_time"] = db.db.incrby("default_time", 0)

    completed_times = db.db.incry("complted_times", 0)
    if completed_times and completed_times % 4 == 0:
        data["break_time"] = db.db.incrby("long_break", 0)
        data["fourth_time"] = True

    return data


if __name__ == "__main__":
    app()
