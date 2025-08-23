"""Scheduling tasks using time.sleep and sched.scheduler."""

from __future__ import annotations

import sched
import time


def schedule_events() -> None:
    scheduler = sched.scheduler(time.time, time.sleep)

    def event(name: str) -> None:
        print(f"{time.strftime('%X')} - Event {name}")

    # schedule two events at different times
    scheduler.enter(1.0, 1, event, argument=("A",))
    scheduler.enter(2.0, 1, event, argument=("B",))
    print("Starting scheduler at", time.strftime("%X"))
    scheduler.run()


if __name__ == "__main__":
    schedule_events()