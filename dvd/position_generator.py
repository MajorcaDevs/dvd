from itertools import islice
from random import randint, uniform
from typing import Iterable, Optional, Tuple

def dvd_positions(resolution, dvd_logo_size, speed, fps):
    position = (
        randint(0, resolution[0] - dvd_logo_size[0]),
        randint(0, resolution[1] - dvd_logo_size[1]),
        False
    )
    direction = (1, 1)

    while True:
        new_position = (
            position[0] + direction[0] * speed / fps,
            position[1] + direction[1] * speed / fps,
            False
        )

        recalculate = False
        rand = uniform(0.95, 1.05)
        if new_position[0] <= 0:
            direction = (rand, direction[1])
            recalculate = True
        elif new_position[0] + dvd_logo_size[0] >= resolution[0]:
            direction = (-rand, direction[1])
            recalculate = True
        if new_position[1] <= 0:
            direction = (direction[0], rand)
            recalculate = True
        elif new_position[1] + dvd_logo_size[1] >= resolution[1]:
            direction = (direction[0], -rand)
            recalculate = True

        if recalculate:
            new_position = (
                position[0] + direction[0] * speed / fps,
                position[1] + direction[1] * speed / fps,
                True
            )

        yield new_position
        position = new_position

def generate_dvd_positions(
    resolution: Tuple[int, int],
    dvd_logo_size: Tuple[int, int],
    speed: float,
    fps: int,
    duration: Optional[int],
) -> Iterable[Tuple[float, float, bool]]:
    points = dvd_positions(resolution, dvd_logo_size, speed, fps)
    if duration is not None:
        total_points = int(duration * fps)
        return islice(points, total_points)

    return points
