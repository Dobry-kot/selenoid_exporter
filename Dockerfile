FROM python:3.7
RUN apt update && apt install -y nano
RUN mkdir /selenoid_exporter
RUN useradd selenoid
RUN chown -R selenoid:selenoid /selenoid_exporter
COPY . /selenoid_exporter
WORKDIR /selenoid_exporter
RUN pip install --upgrade pip && pip install -r requirements.txt
USER selenoid
EXPOSE 64580
