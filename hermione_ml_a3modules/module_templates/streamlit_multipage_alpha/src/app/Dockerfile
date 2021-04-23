FROM python:3.8-slim-buster

# add and install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy app folders

COPY ./data /usr/src/app/data
COPY ./streamlitapp /usr/src/app/project
COPY ./saved_sessions /usr/src/app/saved_sessions
COPY ./static /usr/src/app/static
COPY ./.streamlit /usr/src/app/.streamlit

WORKDIR /usr/src/app
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["project/app.py"]