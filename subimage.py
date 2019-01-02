import sys
from settings import CONFIDENCE_THRESHOLD
from common.utils import cropped
from common.utils import UnsupportedFormatOrMissingFile


if __name__ == '__main__':
    sys.stdout.write('\n')

    image_1 = './unit_tests/images/test1.jpg'
    image_2 = './unit_tests/images/test4.jpg'
    confidence_threshold = CONFIDENCE_THRESHOLD
    # TODO: args, image1 and image2 and cutoff_confidence (optional, defaults to the value in settings)

    try:
        match, index, confidence = cropped(image_1, image_2, confidence_threshold)
    except UnsupportedFormatOrMissingFile:
        sys.stdout.write('Error: One or both of input images is missing or has an unsupported format.\n')
    else:
        if match is None:
            sys.stdout.write('No image appears to be cropped.\n')
        else:
            cropped_image = [image_1, image_2][index]
            sys.stdout.write('Image "{}" appears to be cropped.\n'.format(cropped_image))
            sys.stdout.write('Top left corner (x-horizontal, y-vertical) : {}\n'.format(match[0]))
        if confidence > 0.0:
            sys.stdout.write('Confidence score : {}\n'.format(confidence))
        else:
            sys.stdout.write('Incompatible dimenssions\n')

    sys.stdout.write('\n')


# end of file
