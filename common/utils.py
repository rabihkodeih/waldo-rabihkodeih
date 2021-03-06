import sys
import time
import cv2

from functools import wraps
from settings import CONFIDENCE_THRESHOLD
from settings import RESAMPLE_WIDTH
from settings import MIN_TEMPLATE_RESCALE_WIDTH
from settings import MIN_IMAGE_RESCALE_WIDTH


def profile_execution_time(func):
    '''
    This decorator helps identify slow code sections by
    profiling the execution time of the decorated function.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        sys.stdout.write('"%s" (%s secs)\n' % (func.__name__, elapsed_time))
        return result
    return wrapper


class UnsupportedFormatOrMissingFile(Exception):
    '''
    Excpetion to be raised in case of a missing image file
    or unsupported image format.
    '''
    pass


def subimage(image_path, template_path,
             resample_width=RESAMPLE_WIDTH,
             min_image_rescale_width=MIN_IMAGE_RESCALE_WIDTH,
             min_template_rescale_width=MIN_TEMPLATE_RESCALE_WIDTH,
             confidence_threshold=CONFIDENCE_THRESHOLD):
    '''
    This function abstracts away the main logic of doing the cropping analysis
    through a template matching algorithm. It decideds wether template image
    is contained within the source image.

    @param image_path:
        the relative or full path of the source image

    @param template_path:
        the relative or full path of the template image

    @param resample_width:
        the width in pixels to resample the source image to, in order to speedup
        template matching

    @param min_image_rescale_width:
        minimum width in pixels of the image required to apply rescaling

    @param min_template_rescale_width:
        minimum width in pixels of the template required to carry on with rescaling,
        tested after applying rescaling to the template

    @param confidence_threshold:
        the minimum level of confidence score required to decide positively

    @return:
        <two-points match tuple>, <confidence-score floating value>
    '''
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    try:
        img_height, img_width = img.shape
        tmpl_height, tmpl_width = template.shape
    except Exception:
        raise UnsupportedFormatOrMissingFile()
    match, confidence = None, 0.0
    if tmpl_height <= img_height and tmpl_width <= img_width:
        scale = 1.0
        if max(img_height, img_width) > min_image_rescale_width:
            scale = resample_width / img_width
            scaled_img_height = int(img_height*scale)
            scaled_img_width = int(img_width*scale)
            scaled_tmpl_height = int(tmpl_height*scale)
            scaled_tmpl_width = int(tmpl_width*scale)
            if max(scaled_tmpl_width, scaled_tmpl_height) >= min_template_rescale_width:
                intermethod = cv2.INTER_AREA
                img = cv2.resize(img, (scaled_img_width, scaled_img_height), interpolation=intermethod)
                template = cv2.resize(template, (scaled_tmpl_width, scaled_tmpl_height), interpolation=intermethod)
            else:
                scale = 1.0
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, confidence, _, match_location = cv2.minMaxLoc(result)
        if confidence >= confidence_threshold:
            x, y = match_location
            x, y = int(x/scale), int(y/scale)
            match = ((x, y), (x + tmpl_width, y + tmpl_height))
    return match, confidence


def cropped(image_path_1, image_path_2, confidence_threshold):
    '''
    This functions applies the main matching algorithm to its
    inputs in the appropriate order.
    '''
    args = [(image_path_1, image_path_2),
            (image_path_2, image_path_1)]
    confidence = 0.0
    for i, (path1, path2) in enumerate(args):
        match, tmp_confidence = subimage(path1, path2, confidence_threshold=confidence_threshold)
        confidence = max(confidence, tmp_confidence)
        if match is not None:
            break
    return match, i, confidence


def plot_recantgles(image_path, rectangles, title='Image', color=(0, 0, 255)):
    '''
    Convinience function used for debugging by plotting a list
    of rectangles onto an image.
    '''
    img = cv2.imread(image_path)
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    for rect in rectangles:
        if rect:
            p1, p2 = rect
            cv2.rectangle(img, p1, p2, color, thickness=2)
    cv2.imshow(title, img)
    return img


# end of file
