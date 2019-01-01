import sys
import cv2
from common.utils import subimage
from common.utils import cropped
from common.utils import plot_recantgles
from common.utils import UnsupportedFormatOrMissingFile


if __name__ == '__main__':
    sys.stdout.write('\n')

    # TODO: state assumptions:
    #    - no scaling is allowed
    #    - based on normed correlation formula
    #    - sweeping window and runtime
    #    - resamples to fixed size in case sample size allows it
    #    - etc...
    #    - write README file
    # TODO: implement the general case with all necessary checks:
    #        one image must be completely within another one
    # TODO: implement as a command line

#     image_path = './images/image1/image.jpg'
#     template_path = './images/image1/positive_samples/sample1.jpg'

    image_1 = './unit_tests/images/test1.jpg'
    image_2 = './unit_tests/images/test2.jpg'
    # TODO: assert both files exists

    try:
        match = cropped(image_1, image_2)
#         args = [(image_path, template_path),
#                 (template_path, image_path)]
#         for path1, path2 in args:
#             match = subimage(path1, path2)
#             if match is not None:
#                 break
    except UnsupportedFormatOrMissingFile:
        sys.stdout.write("Error: One or both of your input images is missing or has an unsupported image format.\n")
    else:
        print()
        print('=' * 70)
        print();print();print()
        from pprint import pprint
        print(match)
        print();print();print()
        print('=' * 70)
        print()

    # plot_recantgles(image_path, [match])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    sys.stdout.write('\n')


# end of file
