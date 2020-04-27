import pandas as pd
import math

features = ["hair", "feathers", "eggs", "milk", "airborne", "aquatic", "predator", "toothed", "backbone", "breathes",
            "venomous", "fins", "legs", "tail", "domestic", "catsize"]

zoo_data = pd.read_csv("zoo.data",
                       header=None,
                       names=["name"] + features + ["type"])

N = len(zoo_data.index)
types = list(range(1, 8))
for feature in features:
    feature_groups = zoo_data.groupby([feature]).size().to_dict()
    feature_type_groups = zoo_data.groupby([feature, "type"]).size().to_dict()
    H = 0
    for i, Ni in feature_groups.items():
        Hi = 0
        for type in types:
            Nij = feature_type_groups[(i, type)] if feature_type_groups.keys().__contains__((i, type)) else None
            if Nij is None:
                continue
            pij = Nij / Ni
            Hi -= 0 if pij == 0 else pij * math.log2(pij)
        H += (Ni * Hi)/N
    print(feature + "    " + str(round(H, 2)))

# pip3 install termgraph
# termgraph data.dat --width 80 --color cyan
