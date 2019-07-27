FROM ubuntu:18.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# timezone info
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install apt packages
RUN apt-get update
RUN apt-get install -y --fix-missing \
    apt-transport-https ca-certificates curl software-properties-common \
    iputils-ping \
    mc \
    mysql-client-5.7 \
    python3 python3-pip ipython3 \
    python3-mysqldb python3-psycopg2 python3-pymssql
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# install pip3 packages
RUN pip3 install \
    unittest-xml-reporting \
    coverage

RUN mkdir etlxci
WORKDIR /etlxci
