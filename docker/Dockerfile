# X-11 forwarding:
# http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/

FROM ubuntu:18.04
ENV LC_CTYPE C.UTF-8


# add i386, update everything and install some tools
RUN dpkg --add-architecture i386 && \
apt-get update && \
apt-get install -y \
    sudo \
    strace \
    ltrace \
    curl \
    wget \
    gcc \
    net-tools \
    vim \
    gdb \
    python \
    python-pip \
    python3 \
    python3-pip \
    python-qt4 \
    python3-pyqt4 \
    wget \
    git \
    make \
    procps \
    libpcre3-dev \
    libdb-dev \
    libxt-dev \
    libxaw7-dev \
    libc6:i386 \
    libncurses5:i386 \
    libstdc++6:i386

RUN pip3 install \
    lxml \
    wikipedia \
    requests

# https://skandhurkat.com/post/x-forwarding-on-docker/
RUN apt-get install -qqy x11-apps
RUN apt-get install -y xauth

