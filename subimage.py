import sys
import json
import time
from settings import CONFIDENCE_THRESHOLD
from common.utils import cropped
from common.utils import UnsupportedFormatOrMissingFile


if __name__ == '__main__':

    image_1 = './unit_tests/images/test1.jpg'
    image_2 = './unit_tests/images/test2.jpg'
    confidence_threshold = CONFIDENCE_THRESHOLD
    # TODO: args, image1 and image2 and cutoff_confidence (optional, defaults to the value in settings)
    # TODO: add help text explaining the output format and interpretation

    try:
        start_time = time.time()
        match, index, confidence = cropped(image_1, image_2, confidence_threshold)
        elapsed_time = time.time() - start_time
    except UnsupportedFormatOrMissingFile:
        result = {'status': 'ERROR',
                  'message': 'One or both of input images is either missing or has an unsupported format.'}
    else:
        if match is None:
            result = {'status': 'OK',
                      'cropped': None,
                      'top-left': None,
                      'confidence': confidence,
                      'execution-time': elapsed_time}
        else:
            result = {'status': 'OK',
                      'cropped': [image_1, image_2][index],
                      'top-left': {'x': match[0][0], 'y': match[0][1]},
                      'confidence': confidence,
                      'execution-time': elapsed_time}
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write('\n')


# end of file
