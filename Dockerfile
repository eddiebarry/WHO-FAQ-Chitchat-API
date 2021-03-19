conda create -n venv_name python=3.6
conda activate venv_name
conda install -c pytorch faiss-cpu
# linux
sudo apt install gcc
git clone https://github.com/facebookresearch/fastText.git
cd fastText
sudo pip install .

sudo /Users/edgarmonis/minicond/envs/venv_name/bin/pip 

gunicorn --bind 0.0.0.0:5001 wsgi:app --preload