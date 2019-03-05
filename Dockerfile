FROM python:3.7.2-alpine

LABEL maintainer="kaden@vermilion.tech"

WORKDIR /usr/src/app

COPY . .

RUN python setup.py install

ENTRYPOINT [ "realvalidation" ]

CMD [ "--help" ]
