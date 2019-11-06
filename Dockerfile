FROM python:3
WORKDIR /
RUN pip install pytest
COPY . /
RUN /install.sh
RUN python3 /ipinfo/scripts/ipinfo_db_update.py

CMD [ "pytest", "tests"]