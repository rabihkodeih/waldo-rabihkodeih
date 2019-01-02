import os
import sys
import json
import time
import argparse
import statistics
from common.utils import subimage

BASE_DIR = os.path.dirname(__file__)


if __name__ == '__main__':
    # define command line parser and add arguments
    parser = argparse.ArgumentParser()
    root_images_path_help_text = ('This is the root path of all root images '
                                  'that will be used to measure performance '
                                  'for positive and negative samples.')
    parser.add_argument('--root_images_path', help=root_images_path_help_text, type=str)

    # parse command line arguments
    args = parser.parse_args()
    root_images_path = args.root_images_path
    if root_images_path is None:
        root_images_path = 'images'
    sys.stdout.write('root_images_path : {}\n'.format(root_images_path))

    # initialize performance metrics
    false_negatives, false_positives = 0, 0
    displacements = []
    execution_times = []

    # measure performance
    with open(os.path.join(BASE_DIR, root_images_path, 'positive_samples.json')) as f:
        positive_samples = json.load(f)
    for sample in positive_samples:
        image1_path = sample['source_image_path']
        image2_path = sample['path']
        start_time = time.time()
        match, confidence = subimage(image1_path, image2_path)
        elapsed_time = time.time() - start_time
        execution_times.append(elapsed_time)
        sample_rect = (sample['x'], sample['y'], sample['x'] + sample['width'], sample['y'] + sample['height'])
        displacement = 0
        if match is not None:
            match_rect = [match[0][0], match[0][1], match[1][0], match[1][1]]
            displacement = (max(abs(y - x) for x, y in zip(sample_rect, match_rect)))
        displacements.append(displacement)
        if match is None:
            false_negatives += 1
        sys.stdout.write('{}  {}  {}  {}\n'.format(image2_path, displacement, match, confidence))
    with open(os.path.join(BASE_DIR, root_images_path, 'negative_samples.json')) as f:
        negative_samples = json.load(f)
    for sample in negative_samples:
        image1_path = sample['source_image_path']
        image2_path = sample['path']
        start_time = time.time()
        match, confidence = subimage(image1_path, image2_path)
        elapsed_time = time.time() - start_time
        execution_times.append(elapsed_time)
        if match:
            false_positives += 1
        sys.stdout.write('{}  {}  {}\n'.format(image2_path, match, confidence))
    et_mean = statistics.mean(execution_times)
    et_stddev = statistics.stdev(execution_times)
    disp_mean = statistics.mean(displacements)
    disp_stddev = statistics.stdev(displacements)

    # report performance metrics
    sys.stdout.write('-'*50 + '\n')
    sys.stdout.write('Sample Size : {}\n'.format(len(positive_samples)))
    sys.stdout.write('Execution Time Average (secs) : {}\n'.format(et_mean))
    sys.stdout.write('Execution Time Std. Dev. (secs) : {}\n'.format(et_stddev))
    sys.stdout.write('Displacement Average (pixels) : {}\n'.format(disp_mean))
    sys.stdout.write('Displacement Std. Dev. (pixels) : {}\n'.format(disp_stddev))
    sys.stdout.write('False Negatives : {}\n'.format(false_negatives))
    sys.stdout.write('False Positives : {}\n'.format(false_positives))
    sys.stdout.write('-'*50 + '\n')


# end of file
