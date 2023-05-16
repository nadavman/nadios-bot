FROM python:3.10-alpine
RUN mkdir /bot
ADD . /bot
WORKDIR /bot
RUN pip install .
CMD ["python", "/bot/src/nadios_bot/main.py"]