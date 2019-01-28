docker run -p 4000:4000 --rm -it --volume="$PWD/vendor/bundle:/usr/local/bundle" --volume="$PWD:/srv/jekyll" jekyll/jekyll jekyll serve --watch
