import sys
import json
import time
import argparse
import textwrap
from settings import CONFIDENCE_THRESHOLD
from common.utils import cropped
from common.utils import UnsupportedFormatOrMissingFile


if __name__ == '__main__':

    # define command line parser and add arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
        The output will be JSON formatted:
        {
          "status": <"OK", "ERROR">,
          "message": <null, error-message>,
          "cropped": <null, image1, image2>,
          "top-left": <null, {"x": x-value, "y": y-value}>,
          "confidence": <null, confidence-score>,
          "execution-time": <null, execution-time-in-seconds>
        }
        ''')
    )
    image1_help_text = 'Full or relative path of the first image'
    parser.add_argument('image1', help=image1_help_text, type=str)
    image2_help_text = 'Full or relative path of the second image'
    parser.add_argument('image2', help=image2_help_text, type=str)
    confidence_threshold_help_text = ('Threshold of confidence level to decide cropping,'
                                      'should be between 0.0 and 1.0, defaults to '
                                      '{}'.format(CONFIDENCE_THRESHOLD))
    parser.add_argument('--confidence_threshold',
                        help=confidence_threshold_help_text,
                        type=float)

    # parse command line arguments
    args = parser.parse_args()
    image1 = args.image1
    image2 = args.image2
    confidence_threshold = args.confidence_threshold
    if confidence_threshold is None:
        confidence_threshold = CONFIDENCE_THRESHOLD

    try:
        start_time = time.time()
        match, index, confidence = cropped(image1, image2, confidence_threshold)
        elapsed_time = time.time() - start_time
    except UnsupportedFormatOrMissingFile:
        result = {'status': 'ERROR',
                  'message': 'One or both of input images is either missing or has an unsupported format.',
                  'cropped': None,
                  'top-left': None,
                  'confidence': None,
                  'execution-time': None}
    else:
        if match is None:
            result = {'status': 'OK',
                      'message': None,
                      'cropped': None,
                      'top-left': None,
                      'confidence': confidence,
                      'execution-time': elapsed_time}
        else:
            result = {'status': 'OK',
                      'message': None,
                      'cropped': [image1, image2][index],
                      'top-left': {'x': match[0][0], 'y': match[0][1]},
                      'confidence': confidence,
                      'execution-time': elapsed_time}
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write('\n')


# end of file
