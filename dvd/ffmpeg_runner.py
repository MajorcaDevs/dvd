from subprocess import Popen, PIPE, DEVNULL
import signal
import sys

def run_ffmpeg(fps: float, is_live: bool, *args):
    ffmpeg = Popen(
        ['ffmpeg', '-y', *(['-re'] if is_live else []), '-f', 'image2pipe', '-c:v', 'bmp', '-r', str(fps), '-i', '-', *args],
        stdin=PIPE,
        stdout=DEVNULL,
        stderr=DEVNULL,
    )

    def stop_handler(sig, frame):
        print('')
        print('Detected early close, finishing...')
        ffmpeg.stdin.close()
        if is_live:
            ffmpeg.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)

    return ffmpeg
