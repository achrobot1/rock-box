#! /bin/sh

XAUTH=$HOME/.Xauthority
touch $XAUTH

docker run -it --rm \
    --network=host \
    --env DISPLAY=$DISPLAY \
    --env="QT_X11_NO_MITSHM=1" \
    --volume $XAUTH:/root/.Xauthority \
    -v $PWD:/pwd \
    --name rockbox  rockbox:ubuntu18.04
    # --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
