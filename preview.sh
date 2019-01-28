#/bin/bash

# args: 1: UID that you want the container to run as - id -u for info
docker run -e JEKYLL_UID=$1 -p 4000:4000 --rm -it --volume="$PWD/vendor/bundle:/usr/local/bundle" --volume="$PWD:/srv/jekyll" jekyll/jekyll jekyll serve --watch
