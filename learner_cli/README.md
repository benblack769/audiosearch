### Instructions to download and use dataset


```
# first we need to get the code for audio processing
git clone https://github.com/benblack769/sound-eval
# copy over files from the current directory before cd in
cp process_fma_metadata.py create_json_dataset.py sound-eval/
cd sound-eval
# now we download and extract the data
mkdir data/
cd data/
wget https://os.unil.cloud.switch.ch/fma/fma_small.zip
wget https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
# the unzip utility does not work for some reason, so use 7z
7z x fma_small.zip
7z x fma_metadata.zip
cd ..
python process_fma_metadata.py
# preprocess the audio files
python spectrify_all.py data/fma_small/ data/fma_vecs/ --config=configs/train_opt.yaml
# train model, generate vectors. Requires manual interrupt, probably should wait around 1 hour to train
python spectrogram_doc2vec.py  data/fma_vecs/ data/fma_outs/ --config=configs/train_opt.yaml
# create json dataset for nearest neighbors DB to encode
python create_json_dataset.py
cp data/learned_dataset.json ..
```
