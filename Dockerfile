FROM python:3.9

ENV PYTHONBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    curl \
    git \
    python3-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# OPTIONAL: Install newer version of cmake (if needed)
RUN curl -fsSL https://cmake.org/files/v3.26/cmake-3.26.4.tar.gz | tar -xz && \
    cd cmake-3.26.4 && \
    ./bootstrap && \
    make -j$(nproc) && \
    make install

WORKDIR /code

COPY . /code

# RUN pip install cmake && pip install -r requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8101

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8101  
