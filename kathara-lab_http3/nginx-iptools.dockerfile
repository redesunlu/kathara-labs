FROM nginx:1.25-bookworm

RUN apt-get update && \
    apt-get -y install iproute2 net-tools && \
    apt clean