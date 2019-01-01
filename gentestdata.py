import os
import sys
import cv2
import json
import random
import shutil
import numpy as np

from settings import ROOT_SAMPLES_PATH
from settings import MIN_TEST_SAMPLE_WIDTH
from settings import MIN_TEST_SAMPLE_HEIGHT
from settings import MAX_TEST_SAMPLE_WIDTH_RATIO
from settings import MAX_TEST_SAMPLE_HEIGHT_RATIO


def get_image_path(testcase_path):
    image_path = [p for p in os.listdir(testcase_path) if p.startswith('image.')][0]
    return os.path.join(testcase_path, image_path)


def generate_samples(image_path, num_samples=100, samples_folder='samples', positive=True):
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
                        'image_path': image_path})
        cv2.imwrite(sample_path, sample)

    return samples


if __name__ == '__main__':
    print('Starting\n')

    # TODO: convert to command line

    # initialization
    root_path = ROOT_SAMPLES_PATH
    positive_samples = []
    negative_samples = []

    # generate samples
    for testcase in os.listdir(root_path):
        testcase_path = os.path.join(root_path, testcase)
        if not os.path.isdir(testcase_path):
            continue
        image_path = get_image_path(testcase_path)
        positive_samples += generate_samples(
            image_path, num_samples=2, samples_folder='positive_samples', positive=True)
        negative_samples += generate_samples(
            image_path, num_samples=2, samples_folder='negative_samples', positive=False)
        # TODO: generate negative samples

    # write samples meta data to disk
    with open(os.path.join(root_path, 'positive_samples.json'), 'w') as f:
        json.dump(positive_samples, f, indent=4, sort_keys=True)
    with open(os.path.join(root_path, 'negative_samples.json'), 'w') as f:
        json.dump(negative_samples, f, indent=4, sort_keys=True)

    cv2.destroyAllWindows()

    print('\nDone.')


# end of file
