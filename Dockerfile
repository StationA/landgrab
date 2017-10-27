FROM registry.stationa.io/stationa/base:latest

ADD . /landgrab
WORKDIR /landgrab
RUN pip install .

CMD ["/usr/local/bin/landgrab"]
