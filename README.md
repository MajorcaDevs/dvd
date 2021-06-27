# DVD screensaver generator

A small utility that generates a stream of images simulating the good ol' DVD screensavers. Images are sent to [`ffmpeg`][ffmpeg] and the encoded using the provided arguments.

## Requirements

- Python 3.7 or higher
- [`ffmpeg`][ffmpeg] installed and accessible

## Installation

In the releases page, the installable wheel can be found. Download it and install it using `pip install -U dvd-*-py3-none-any.whl`. It might be useful to use a `virtualenv` to install the package.

## Usage

The tool simply generate frames and passes them to `ffmpeg`. In order to properly generate the video output, a set of arguments must be provided to the tool to pass them directly to ffmpeg, but don't worry, see below some examples.

There are several settings that can be changed in the tool to generate the images (see `--help`):

- `width`: The width of the generated images (defaults to 1280)
- `height`: The height of the generated images (defaults to 720)
- `fps`: The frames per second (defaults to 24)
- `scale`: Scale resolution (for testing, defaults to 1 - unmodified)
- `duration`: Duration in seconds of the video (defaults to 60s)
- `live`: Enables live mode (endless generation)

### Simple videos

```bash
# a 720p 1 minute duration video using H264
dvd -- -c:v h264 -b:v 1M -pix_fmt yuv420p -profile:v high video.mkv

# a 1080p 60fps 1 minute duration video using H264
dvd --width 1920 --height 1080 --fps 60 -- -c:v h264 -crf:v 24 -pix_fmt yuv420p -profile:v high video.mkv

# a 4K 60fps 10 hours duration video using HEVC with Nvidia graphics card (extremely slow generation!)
dvd --width 3840 --height 2160 --fps 60 --duration 36000 -- \
    -c:v hevc_nvenc -preset:v slow -rc:v constqp -qp:v 26 -pix_fmt:v p010le video.mkv
```

### Live streaming

```bash
dvd --width 1920 --height 1080 --fps 30 -- \
    # extra input: blank audio
    -f lavfi -i 'anullsrc=channel_layout=stereo:sample_rate=44100' \
    # join audio and generated images stream
    -map '0:v:0' -map '1:a:0' \
    # use H264
    -c:v libx264 -g 30 \
    # video bitrate
    -b:v 400k \
    # video profile and color format
    -pix_fmt yuv420p -profile:v high -preset:v fast \
    # audio codec and bitrate
    -c:a libfdk_aac -b:a 128k -ac 2 \
    # output to streaming service
    -f flv -s 1920x1080 rtmps://...
```

## Develop

To setup the development environment, install it using `pipenv install --dev` and start developing from it. To build the package, run `python -m build` (or `pipenv run python -m build`) to generate the wheel package.

  - [ffmpeg]: https://ffmpeg.org
