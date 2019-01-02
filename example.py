import sys
import cv2
from common.utils import subimage
from common.utils import plot_recantgles


if __name__ == '__main__':

    image1 = './images/image1.jpg'
    image2 = './images/image2.jpg'
    match, _ = subimage(image1, image2)
    result = plot_recantgles(image1, [match])
    cv2.imwrite('./images/result.jpg', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    sys.stdout.write('\n')


# end of file
