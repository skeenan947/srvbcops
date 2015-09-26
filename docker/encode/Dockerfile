FROM ubuntu

WORKDIR /root

RUN mkdir /root/scripts/

ADD scripts /root/scripts

RUN \
  apt-get update && \
  apt-get -q -y install libav-tools s3cmd python-pip python-boto && \
  pip install qtfaststart

VOLUME /root/video

CMD /root/scripts/enc.sh
