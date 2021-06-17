# conda create -n venv_name python=3.6
# conda activate venv_name
# conda install -c pytorch faiss-cpu
# # linux
# sudo apt install gcc
# git clone https://github.com/facebookresearch/fastText.git
# cd fastText
# sudo pip install .

# sudo /Users/edgarmonis/minicond/envs/venv_name/bin/pip 

# gunicorn --worker-class gevent --bind 0.0.0.0:5001   wsgi:app --workers 2 --worker-connections 2000 --timeout 60 --preload

FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
# COPY . .
# ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

RUN git clone --branch dev/data-from-script https://github.com/eddiebarry/WHO-FAQ-Chitchat-API.git

WORKDIR /app/WHO-FAQ-Chitchat-API

RUN conda env create -f env.yaml

RUN git clone https://github.com/facebookresearch/fastText.git

WORKDIR /app/WHO-FAQ-Chitchat-API/fastText
RUN apt-get update
RUN apt install -y g++
RUN /opt/conda/envs/myenv/bin/pip install .

RUN /opt/conda/envs/myenv/bin/pip install emoji==1.2.0 spacy==2.3.2

# downloading lexical model:
RUN ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "-m", "spacy", "download", "en_core_web_sm"]

WORKDIR /app/WHO-FAQ-Chitchat-API
RUN ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "download_weights.py"]

# updating the indexed sentences and the JSON datasets from the Excel script:
RUN ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "demo.py"]

# conda run --no-capture-output -n myenv python download_weights.py
# # Make RUN commands use the new environment:
# SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# # Make sure the environment is activated:
# RUN echo "Make sure flask is installed:"
# RUN python -c "import flask"

# # The code to run when container is started:
# COPY run.py .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "gunicorn", "--worker-class", "gevent", "--bind", "0.0.0.0:5001", "wsgi:app", "--workers", "2", "--worker-connections", "2000", "--timeout", "60", "--preload"]