FROM python:3.7.8-slim

COPY requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt

COPY ./news_scraper /news_scraper
COPY ./news_scraper/bin /news_scraper/bin
COPY ./scrapy.cfg /scrapy.cfg

WORKDIR /news_scraper

ENTRYPOINT ["bash", "/news_scraper/bin/run.sh"]
