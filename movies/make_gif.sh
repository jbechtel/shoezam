#! /bin/bash
ffmpeg -i Shoezam_Vid.mov  -pix_fmt rgb24 -r 10 -f gif - | gifsicle --optimize=3 --delay=3 > out.gif
