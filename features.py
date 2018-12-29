import os
import random
import cv2
import numpy as np
import _pickle as pickle
from matplotlib import pyplot
from scipy.spatial.distance import cdist


def extract_features(image_path, vector_size=32):
    image = cv2.imread(image_path, mode="RGB")
    alg = cv2.KAZE_create()  # other algorithms can be used here
    keypoints = alg.detect(image)
    keypoints.sort(key=lambda x: -x.response)
    keypoints = keypoints[:vector_size]
    keypoints, descriptors = alg.compute(image, keypoints)
    descriptors = descriptors.flatten()
    needed_size = vector_size * 64
    if descriptors.size < needed_size:
        zeros = np.zeros(needed_size - descriptors.size)
        descriptors = np.concatenate([descriptors, zeros])
    return descriptors


def batch_extractor(images_path, pickled_db_path="features.pck"):
    filenames = os.listdir(images_path)
    filenames.sort()
    filepaths = [os.path.join(images_path, p) for p in filenames]
    images_features = {}
    for im_path in filepaths:
        print('Extracting features "%s"' % im_path)
        img_name = os.path.split(im_path)[-1].lower()
        images_features[img_name] = extract_features(im_path)
    with open(pickled_db_path, 'w') as fp:
        pickle.dump(images_features, fp)


class Matcher(object):

    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path) as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cosine_distance(self, vector):
        v = vector.reshape(1, -1)
        return cdist(self.matrix, v, 'cosine').reshape(-1)

    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        img_distances = self.cosine_distance(features)
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()
        return nearest_img_paths, img_distances[nearest_ids].tolist()


if __name__ == '__main__':
    print('Starting\n')

    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(base_dir)

    print('\nDone.')


# TODO: Create a file ~/.matplotlib/matplotlibrc there and add the following code: backend: TkAgg
# end of file
