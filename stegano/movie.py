import os
import shutil

import cv2
vidcap = cv2.VideoCapture('media/git.mp4')
success,image = vidcap.read()
count = 0
if success:
  cv2.imwrite("frame%d.jpg" % count, image)


def frame_extraction(video):
  clean_tmp()
  if not os.path.exists("data/tmp"):
    os.makedirs("tmp")
  temp_folder = "data/tmp"
  print("[INFO] tmp directory is created")

  vidcap = cv2.VideoCapture(video)
  count = 0

  while True:
    success, image = vidcap.read()
    if not success:
      break
    cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
    count += 1

def clean_tmp(path="data/tmp"):
  if os.path.exists(path):
    shutil.rmtree(path)
    print("[INFO] tmp files are cleaned up")