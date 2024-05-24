from datetime import datetime, timedelta, UTC

from .args import parse_arguments
from .ffmpeg_runner import run_ffmpeg
from .image_generator import generate_frame, generate_random_color_dvd_logo, get_scaled_dvd_logo
from .position_generator import generate_dvd_positions


def main():
    args = parse_arguments()
    ffmpeg = run_ffmpeg(args.fps, args.live, *args.ffmpeg_args)

    resolution = (int(args.width / args.scale), int(args.height / args.scale))
    scl = (240 / args.height) * 40
    speed = int(1000 / args.scale / scl * 2)
    dvd_logo = get_scaled_dvd_logo(args.scale, scl)
    dvd_logo_color = dvd_logo

    total_points = int(100 * args.fps) if args.live else int(args.duration * args.fps)
    points = generate_dvd_positions(
        resolution,
        (dvd_logo.width, dvd_logo.height),
        speed,
        args.fps,
        None if args.live else args.duration,
    )

    i = 1
    last_print = datetime.now(UTC) - timedelta(seconds=2)
    for x, y, recalculate in points:
        start_frame_time = datetime.now(UTC)

        if recalculate:
            dvd_logo_color = generate_random_color_dvd_logo(dvd_logo)
        generate_frame((int(x), int(y)), resolution, dvd_logo, dvd_logo_color).save(ffmpeg.stdin, 'BMP')

        end_frame_time = datetime.now(UTC)
        took = end_frame_time - start_frame_time
        tt = took.seconds + took.microseconds / 1000000
        if (end_frame_time - last_print).seconds >= 1:
            print(f'\r{i * 100 // total_points}% {i}: ({int(x)}, {int(y)}) - {tt}s       \033[7D', end='')
            last_print = end_frame_time
        i += 1

    print(f'\r{i * 100 // total_points}% {i}: ({int(x)}, {int(y)}) - {tt}s       ')
    print('Waiting to ffmpeg to finish')
    ffmpeg.stdin.close()
    ffmpeg.wait()
    print('Finished')


if __name__ == '__main__':
    main()
