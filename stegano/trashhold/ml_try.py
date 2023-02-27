import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

f_path = R"D:\gilad\לימודים\אריאל\מדמח\שנה ג - 2022-2023\זיהוי תקיפות\מטלה 02\conn_attack.csv"
save_path = R"D:\gilad\לימודים\אריאל\מדמח\שנה ג - 2022-2023\זיהוי תקיפות\מטלה 02\conn_attack_anomaly_labels.csv"

df = pd.read_csv(f_path,names=["record ID","duration_", "src_bytes","dst_bytes"], header=None)

model = IsolationForest()
df_for_ml = list(zip(df["duration_"], df["src_bytes"],df["dst_bytes"]))
model.fit(df_for_ml)
predict = model.predict(df_for_ml)

d = df[["duration_", "src_bytes", "dst_bytes"]]

d['predict'] = predict
d['predict'] = d['predict'].apply(lambda x: 0 if x == 1 else 1)
df['predict'] = d['predict']

