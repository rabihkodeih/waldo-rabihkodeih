import cv2
from utils import subimage
from utils import plot_recantgles


if __name__ == '__main__':
    print('Starting\n')

    image_path = './images/image1/image.jpg'
    template_path = './images/image1/sample1.jpg'
    match = subimage(image_path, template_path)
    plot_recantgles(image_path, [match])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print('\nDone.')


# end of file
