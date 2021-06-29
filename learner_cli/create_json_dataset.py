import pandas
import base64
import numpy as np
import json

track_data = pandas.read_csv("data/fma_metadata/track_info.csv")
last_vector_num = int(open("data/fma_outs/epoc_num.txt").read())
vectors = np.load("data/final_word_vecs.npy")#np.load(f"data/fma_outs/vector_at_{last_vector_num}.npy")

all_fnames = open("data/fma_outs/music_list.txt").readlines()
all_fnames = [fname.strip()[2:][:-4] for fname in all_fnames]

fma_small = pandas.DataFrame({
    "id": all_fnames,
    "url": ["http://datasets-mirror.s3.amazonaws.com/fma_small/"+fname for fname in all_fnames]
})

new_dataframe = pandas.merge(fma_small,track_data,how="inner",on="id")
assert len(new_dataframe.index) == len(track_data.index)
print(new_dataframe['url'])
datas = json.loads(new_dataframe.to_json(orient="records"))
new_datas = []
for vec, data in zip(vectors, datas):
    bytes = base64.b64encode(vec.astype("float64").tobytes()).decode("utf-8")
    new_entry = {
        "key": bytes,
        "value": data,
    }
    new_datas.append(new_entry)
json.dump(new_datas,open("data/learned_dataset.json",'w'))
