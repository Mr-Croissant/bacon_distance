FROM python:3.12-slim

RUN mkdir /usr/bacon_app

WORKDIR /usr/bacon_app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY setup.py ./
COPY bacon/ ./bacon/


RUN pip install .
RUN chmod 777 -R bacon
RUN python bacon/generate_db.py

CMD ["streamlit", "run", "--server.address", "0.0.0.0", "bacon/app.py"]