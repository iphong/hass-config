# My Home HA Configs

My second build from scratch with Home Assistant and ESPHome.

## FFMpeg examples

Convert mjpeg to h264 mp4
```sh
export INPUT="video.mov"

ffmpeg -i $INPUT -pix_fmt rv32 -b:v 4000k -c:v libx264 out.mp4

ffmpeg -i $INPUT -strict -2 -c:v h264 out.mp4
```
