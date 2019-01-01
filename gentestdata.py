import os
import sys
import cv2
import json
import random
import shutil
import argparse
import numpy as np


MAX_TEST_SAMPLE_WIDTH_RATIO = 0.9
MAX_TEST_SAMPLE_HEIGHT_RATIO = 0.9
MIN_TEST_SAMPLE_WIDTH = 100
MIN_TEST_SAMPLE_HEIGHT = 50


def get_image_path(testcase_path):
    image_path = [p for p in os.listdir(testcase_path) if p.startswith('image.')][0]
    return os.path.join(testcase_path, image_path)


def generate_samples(image_path,
                     num_samples=10,
                     samples_folder='samples',
                     positive=True):
    label = 'positive' if positive else 'negative'
    sys.stdout.write('generating {} samples for "{}"\n'.format(label, image_path))
    base_image_path = os.path.split(image_path)[-2]
    _, extension = os.path.splitext(image_path)
    samples_root_path = os.path.join(base_image_path, samples_folder)
    if os.path.exists(samples_root_path):
        shutil.rmtree(samples_root_path, ignore_errors=True)
    os.makedirs(samples_root_path)
    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    # calculate sample width interval
    max_sample_width = int(MAX_TEST_SAMPLE_WIDTH_RATIO * width)
    min_sample_width = int(MIN_TEST_SAMPLE_WIDTH)
    assert min_sample_width <= max_sample_width

    # calculate sample height interval
    max_sample_height = int(MAX_TEST_SAMPLE_HEIGHT_RATIO * height)
    min_sample_height = int(MIN_TEST_SAMPLE_HEIGHT)
    assert min_sample_height <= max_sample_height

    # generate samples
    samples = []
    for i in range(num_samples):
        sys.stdout.write('sample {} of {}\n'.format(i + 1, num_samples))
        sample_width = random.randint(min_sample_width, max_sample_width)
        sample_height = random.randint(min_sample_height, max_sample_height)
        x = random.randint(0, width - sample_width)
        y = random.randint(0, height - sample_height)
        assert x >= 0
        assert y >= 0
        sample_name = 'sample{}{}'.format(i + 1, extension)
        sample_path = os.path.join(samples_root_path, sample_name)
        sample = img[y:y + sample_height, x:x + sample_width]
        if not positive:
            sample = cv2.flip(sample, -1)
            noise = np.zeros(sample.shape)
            cv2.randn(noise, 0, 500)
            sample = sample + noise
        samples.append({'x': x,
                        'y': y,
                        'width': sample_width,
                        'height': sample_height,
                        'name': sample_name,
                        'path': sample_path,
                        'source_image_path': image_path})
        cv2.imwrite(sample_path, sample)

    return samples


if __name__ == '__main__':

    # define command line parser and add arguments
    parser = argparse.ArgumentParser()
    num_samples_help_text = ('Number of samples per input image, applies'
                             ' to both positive and negative samples')
    parser.add_argument('num_samples', help=num_samples_help_text, type=int)
    root_images_path_help_text = ('This is the root path of all root images '
                                  'that will be used to generate positive and '
                                  'negative samples.')
    parser.add_argument('--root_images_path', help=root_images_path_help_text, type=str)

    # parse command line arguments
    args = parser.parse_args()
    num_samples = args.num_samples
    root_images_path = args.root_images_path
    if root_images_path is None:
        root_images_path = 'images'
    sys.stdout.write('num_samples : {}\n'.format(num_samples))
    sys.stdout.write('root_images_path : {}\n'.format(root_images_path))

    # initialize samples data structures
    positive_samples = []
    negative_samples = []

    # generate samples
    for testcase in os.listdir(root_images_path):
        testcase_path = os.path.join(root_images_path, testcase)
        if not os.path.isdir(testcase_path):
            continue
        image_path = get_image_path(testcase_path)
        positive_samples += generate_samples(
            image_path, num_samples=num_samples, samples_folder='positive_samples', positive=True)
        negative_samples += generate_samples(
            image_path, num_samples=num_samples, samples_folder='negative_samples', positive=False)

    # write samples meta data to disk
    with open(os.path.join(root_images_path, 'positive_samples.json'), 'w') as f:
        json.dump(positive_samples, f, indent=4, sort_keys=True)
    with open(os.path.join(root_images_path, 'negative_samples.json'), 'w') as f:
        json.dump(negative_samples, f, indent=4, sort_keys=True)

    sys.stdout.write('\nDone.')


# end of file
