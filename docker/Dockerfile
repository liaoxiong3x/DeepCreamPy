FROM debian:stretch-slim

ENV BUILD_PACKAGES="\
        build-essential \
        linux-headers-4.9 \
        python3-dev \
        cmake \
        tcl-dev \
        xz-utils \
        zlib1g-dev \
        git \
        curl \
        unzip" \
    APT_PACKAGES="\
        ca-certificates \
        openssl \
        bash \
        graphviz \
        fonts-noto \
        libpng16-16 \
        libfreetype6 \
        libjpeg62-turbo \
        libgomp1 \
        python3 \
        python3-pip" \
    PYTHON_VERSION=3.6.7 \
    PATH=/usr/local/bin:$PATH \
    PYTHON_PIP_VERSION=9.0.1 \
    MODELS=1byrmn6wp0r27lSXcT9MC4j-RQ2R04P1Z \
    LANG=C.UTF-8

COPY gd.sh /opt
WORKDIR /opt
RUN set -ex; \
    apt-get update -y; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends ${APT_PACKAGES}; \
    apt-get install -y --no-install-recommends ${BUILD_PACKAGES}; \
    ln -s /usr/bin/idle3 /usr/bin/idle; \
    ln -s /usr/bin/pydoc3 /usr/bin/pydoc; \
    ln -s /usr/bin/python3 /usr/bin/python; \
    ln -s /usr/bin/python3-config /usr/bin/python-config; \
    ln -s /usr/bin/pip3 /usr/bin/pip; \
    pip install -U -v setuptools wheel; \
    cd /opt && \
    git clone https://github.com/deeppomf/DeepCreamPy.git && \
    cd /opt/DeepCreamPy && \
    pip install -U -v -r requirements.txt && \
    mkdir -p models/ && \
    bash /opt/gd.sh ${MODELS}; \
    unzip model.zip && \
    mv model.h5 models && \
    apt-get remove --purge --auto-remove -y ${BUILD_PACKAGES}; \
    apt-get clean; \
    apt-get autoclean; \
    apt-get autoremove; \
    rm -rf /tmp/* /var/tmp/*; \
    rm -rf /var/lib/apt/lists/*; \
    rm -f /var/cache/apt/archives/*.deb \
        /var/cache/apt/archives/partial/*.deb \
        /var/cache/apt/*.bin; \
    find /usr/lib/python3 -name __pycache__ | xargs rm -r; \
    rm -rf /root/.[acpw]*;

VOLUME [ "/opt/DeepCreamPy/decensor_input", "/opt/DeepCreamPy/decensor_output" ]

WORKDIR /opt/DeepCreamPy
ENTRYPOINT [ "/usr/bin/python", "/opt/DeepCreamPy/decensor.py" ]


