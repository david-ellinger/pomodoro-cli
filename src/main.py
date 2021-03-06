import typer
import time
import redis

app = typer.Typer()
db = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
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
    set_redis_values(data)


@app.command()
def start():
    data = get_data()
    break_time = data["completed_times"]
    default_time = data["default_time"]
    typer.echo("[*] Started Pomodoro")
    incremental_sleep(default_time)

    typer.echo("[*] Completed Pomodoro")
    db.incrby("completed_times", 1)
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
    data["break_time"] = db.incrby("short_break", 0)
    data["default_time"] = db.incrby("default_time", 0)

    completed_times = db.incry("complted_times", 0)
    if completed_times and completed_times % 4 == 0:
        data["break_time"] = db.incrby("long_break", 0)
        data["fourth_time"] = True

    return data

def set_redis_values(data):
    [db.set(key, data[key]) for key in data.keys()]

if __name__ == "__main__":
    app()
