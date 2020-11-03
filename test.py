import cv2
import sys
import numpy as np
import datetime
import os
import glob
from retinaface import RetinaFace
import argparse
import re
def main(input_dir,path,output_text,output_img):
  thresh = 0.8
  scales = [1024, 1980]

  count = 1

  gpuid = 0
  detector = RetinaFace('./model/R50', 0, gpuid, 'net3')

  img = cv2.imread(os.path.join(input_dir,path))
  im_shape = img.shape
  target_size = scales[0]
  max_size = scales[1]
  im_size_min = np.min(im_shape[0:2])
  im_size_max = np.max(im_shape[0:2])
  #im_scale = 1.0
  #if im_size_min>target_size or im_size_max>max_size:
  im_scale = float(target_size) / float(im_size_min)
  # prevent bigger axis from being more than max_size:
  if np.round(im_scale * im_size_max) > max_size:
      im_scale = float(max_size) / float(im_size_max)

  print('im_scale', im_scale)

  scales = [im_scale]
  flip = False

  for c in range(count):
    faces, landmarks = detector.detect(img, thresh, scales=scales, do_flip=flip)
    print(c, faces.shape, landmarks.shape)

  if faces is not None:
    print('find', faces.shape[0], 'faces')
    for i in range(faces.shape[0]):
      #print('score', faces[i][4])
      box = faces[i].astype(np.int)
      #color = (255,0,0)
      color = (0,0,255)
      cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 2)
      if landmarks is not None:
        landmark5 = landmarks[i].astype(np.int)
        #print(landmark.shape)
        for l in range(landmark5.shape[0]):
          color = (0,0,255)
          if l==0 or l==3:
            color = (0,255,0)
          cv2.circle(img, (landmark5[l][0], landmark5[l][1]), 1, color, 2)
    filename = re.findall('\w+.',path)[0]+'txt'
    filename = os.path.join(output_text,filename)
    with open(filename,'w') as f:
      f.write("%d\n"%(faces.shape[0]))
      for i in range(faces.shape[0]):
        box = faces[i].astype(np.int)
        f.write("%d %d %d %d\n"%(box[0], box[1], box[2]-box[0], box[3]-box[1]))
        #f.write('----------\n')
        #f.write("%d %d %d %d %g \n"%(box[0], box[1], box[2], box[3], box[4]))
    

  #filename = './detector_test_2.jpg'
  #print('writing', filename)
  #cv2.imwrite(filename, img)

  filename = os.path.join(output_img,path)
  print('writing', filename)
  cv2.imwrite(filename, img)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('indir', help='Directory of Image Files')
  parser.add_argument('outdir', help='Directory of Output Files')
  args = parser.parse_args()
  input_files = args.indir
  output = args.outdir
  output_text = os.path.join(output,'text')
  output_img = os.path.join(output,'img')

  if not os.path.exists(output):
    os.mkdir(output)
    os.mkdir(output_text)
    os.mkdir(output_img)
  elif not os.path.exists(output_img):
    os.mkdir(output_img)
  elif not os.path.exists(output_text):
    os.mkdir(output_text)
  
  for filename in os.listdir(input_files):
    main(input_files,filename,os.path.join(output,'text'),os.path.join(output,'img'))