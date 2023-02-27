from tensorflow import keras
from PIL import Image
import numpy as np
from tqdm import tqdm
from movie import *

from model.seganalysis import *

# Load the trained model
model = keras.models.load_model('data/stego.mdl')

# print(files)
# Load the image and preprocess it
def predict(file: str):
    img = Image.open(file)
    img = img.resize((64, 64))  # Resize to the same size as the training data
    img_arr = (np.array(img) % 16) / 16.0  # Normalize pixel values
    img_arr = np.expand_dims(img_arr, axis=0)  # Add batch dimension

    # Make a prediction
    pred = model.predict(img_arr, verbose=0)

    # Print the predicted class
    class_idx = np.argmax(pred)
    return class_idx



# print('Predicted class:', predict('../data/pics/4_lsb/airplane_0005.png'))
#
#
# files, labels = Steganalysis.get_files()
# prediction = []
# for i in tqdm(range(len(files))):
#     file = files[i]
#     pred = predict(file)
#     prediction += [1 if pred != 0 else 0]
# labels = [(1 if label != 0 else 0) for label in labels]
#
# print()
# value_accu(prediction, labels)
def predict_video(file_name):
    prediction = []
    frame_extraction(file_name)
    files = glob.glob('data/tmp/*.png')

    for file in files:
        pred = predict(file)
        prediction += [1 if pred != 0 else 0]

    if sum(prediction) == 0:
        print('Benign')
    else:
        print('Malware')