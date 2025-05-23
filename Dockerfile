# based on debian
FROM rust:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    unzip \
    cmake \
    libboost-all-dev \
    libssl-dev \
    libx11-dev \
    libxft-dev \
    libcgal-dev \
    libgmp-dev \
    libmpfi-dev \
    libgeos++-dev  \
    yasm \
    python3 \
    python3-pip \
    python3-venv \
    default-jre \
    default-jdk \
    time \
    ccache \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/lib/ccache:$PATH"
