from numpy import random
import numpy as np
import pandas as pd

rows = 6
cols = 3
MAX_NUMS = 256
PXL_FORM = 3
columns=['R', 'G', 'B']

im_arr = random.randint(MAX_NUMS, size=(rows, cols, PXL_FORM))
print(im_arr)
print()

im_2d = im_arr.reshape(-1, PXL_FORM)
df = pd.DataFrame(im_2d, columns=columns)
print(df)
print('\n')

#print()
#print(np.zeros((rows*cols, 3)))
mm = pd.DataFrame(np.zeros((MAX_NUMS, 3), dtype='int64'), columns=columns)

for col_name in df.columns.values:
    mm[col_name] = df.groupby(col_name)[col_name].count()

#mm += pd.DataFrame(df.groupby('g').size())
#m.fill
mm = mm.fillna(0).astype('int64')
print(mm[(mm.select_dtypes(include=['number']) != 0).any(1)])
print(mm)
print(np.array(mm['R']))

my_dict = {'R': [0, 1, 2, 3], 'G': [4, 5, 6, 7]}
temp = pd.DataFrame(my_dict)
print(np.array(temp['G']))



