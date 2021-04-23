import fasttext
import fasttext.util

fasttext.util.download_model('en', if_exists='ignore')

# conda run --no-capture-output -n myenv python download_weights.py