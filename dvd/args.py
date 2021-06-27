import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(prog='dvd')

    parser.add_argument('--width', help='Width of the generated images', type=int, default=1280)
    parser.add_argument('--height', help='Height of the generated images', type=int, default=720)
    parser.add_argument('--fps', help='Frames per second', type=float, default=24)
    parser.add_argument('--scale', help='Scale resolution', type=float, default=1)

    duration_group = parser.add_mutually_exclusive_group()
    duration_group.add_argument('--duration', help='Duration of the video in seconds', type=float, default=60)
    duration_group.add_argument('--live', help='Enable live mode (endless generation)', action='store_true')

    parser.add_argument('ffmpeg_args', help='Arguments that will be sent to ffmpeg in order to generate the output', nargs='+')

    return parser.parse_args()
