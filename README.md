# Waldo Subimage Test Project


## Summary

This is the waldo-subimage test project. Technologies used are [Python 3.6](https://www.python.org/downloads/release/python-360/), [numpy](http://www.numpy.org) and [OpenCV](https://opencv.org). 
The main purpose of the project is to decide wether an image has been cropped from another image.
The project is emplemented as a command line tool with the following points:
  * algorithm used is normalized correlation coefficient with sliding window
  * scaling and rotations are not accounted for, only translations
  * most image formats are supported including jpeg with lossy compression
  * a normalized confidence score is used to decide on positives or negatives

See below for a more detailed explanation.


## Installation (Ubuntu)

First make sure that `Python3`, `pip3` and `virtualenv` are all installed and working fine:

    sudo apt-get update
    sudo apt-get dist-upgrade
    sudo apt-get install -y python3-dev virtualenv gcc 

Clone the repository into a destination directory, cd into it then create your virtual env using

    virtualenv -p python3 env
    
and activate it by

    . env/bin/activate
    
Now you can install the requirements by

    pip3 install -r requirements.txt

Run the application:

    python subimage.py --help
    
You should get the following help message:

    usage: subimage.py [-h] [--confidence_threshold CONFIDENCE_THRESHOLD]
                       image1 image2

    positional arguments:
      image1                Full or relative path of the first image
      image2                Full or relative path of the second image

    optional arguments:
      -h, --help            show this help message and exit
      --confidence_threshold CONFIDENCE_THRESHOLD
                            Threshold of confidence level to decide
                            cropping,should be between 0.0 and 1.0, defaults to
                            0.95

    The output will be JSON formatted:
    {
      "status": <"OK", "ERROR">,
      "message": <null, error-message>,
      "cropped": <null, image1, image2>,
      "top-left": <null, {"x": x-value, "y": y-value}>,
      "confidence": <null, confidence-score>,
      "execution-time": <null, execution-time-in-seconds>
    }


## Unit Tests

From the project main folder:

    python -m unit_tests.run


## Example Usage        

From the project main folder:

    python subimage.py ./images/image1.jpg ./images/image2.jpg

should output:

    {
      "status": "OK",
      "message": null,
      "cropped": "./images/image1.jpg",
      "top-left": {
        "x": 467,
        "y": 41
      },
      "confidence": 0.9972856640815735,
      "execution-time": 0.04637265205383301
    }

Image 1:

<img src="https://github.com/rabihkodeih/waldo-rabihkodeih/blob/master/images/image1.jpg" alt="image1" width="720">


Image 2:

<img src="https://github.com/rabihkodeih/waldo-rabihkodeih/blob/master/images/image2.jpg" alt="image2">


Result:

<img src="https://github.com/rabihkodeih/waldo-rabihkodeih/blob/master/images/result.jpg" alt="result" width="720">


## Algorithm and Run-time Complexity

The algorithm used is a sweeping window normalized cross-correlation variant of the popular [template matching algorithms](https://en.wikipedia.org/wiki/Template_matching) used in computer vision and digital image processing.

We've used OpenCV's ready made implementation (check [tutorial 1](https://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/template_matching/template_matching.html) and [tutlrial 2](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html?highlight=template%20matching)).

The algorithm parameter is ```CV_TM_CCOEFF_NORMED``` which is based on the following formula to compute the correlation coefficient between the image and the template at a specific location:


![formula](https://github.com/rabihkodeih/waldo-rabihkodeih/blob/master/formula.png)


A template window is sweeped across the source image and the above formula is applied at each (x, y) location. If the maximum normalized correlation coeffiecient surpasses a given threshold (typically 0.95) then a positive match is decied upon with the location corresponding to this maximum value.

The run time complexity is super-quadratic. If we assume ```R``` to be the width of the source image and ```T``` to be the width of the template then the number of operations is given by: ```(R - T)^2 x T^2```. In practice, performance is good because of CPU caching, and multi-core threading.

In our implementation we rescale images that have a width larger than 1500 pixels to a width of 1024 pixels to control the execution time. We've found that results are of the same quality before and after rescaling.


## Performance Test

First we need to generate a number of sample templates for a given set of images in ```./images``` folder in the project root:

    python gentestdata.py --help
    python gentestdata.py 100
    
This will generate 100 positive and negative template samples for each image. To run the performance test, issue:

    python performance.py --help
    python performance.py
    
A typical output:

    --------------------------------------------------
    Sample Size : 900
    Execution Time Average (secs) : 0.06600021574232313
    Execution Time Std. Dev. (secs) : 0.07631216832661365
    Displacement Average (pixels) : 0.24444444444444444
    Displacement Std. Dev. (pixels) : 0.5759571249783901
    False Negatives : 0
    False Positives : 1
    --------------------------------------------------
    
Note that the average execution time is below 100 milliseconds for most cases.


## Future Directions

There are a possible number of ways this work could evolve:

1. Using the [fast template matching](http://scribblethink.org/Work/nvisionInterface/vi95_lewis.pdf) algorithm.
2. Using [fast normalized cross correlation](http://i81pc23.itec.uni-karlsruhe.de/Publikationen/SPIE01_BriechleHanebeck_CrossCorr.pdf).
3. Using [integral image based weak classifiers](http://i81pc23.itec.uni-karlsruhe.de/Publikationen/SPIE01_BriechleHanebeck_CrossCorr.pdf).
4. Using any of [scalable reverse image search algorithms](https://www.quora.com/What-is-the-algorithm-used-by-Googles-reverse-image-search-i-e-search-by-image-What-algorithms-would-I-need-to-understand-to-create-similar-functionality-on-a-small-scale?redirected_qid=828413).
5. Using [large scale reverse image search](https://www.quora.com/What-is-the-algorithm-used-by-Googles-reverse-image-search-i-e-search-by-image-What-algorithms-would-I-need-to-understand-to-create-similar-functionality-on-a-small-scale?redirected_qid=828413).
6. Using [feature matching and homography](https://www.quora.com/What-is-the-algorithm-used-by-Googles-reverse-image-search-i-e-search-by-image-What-algorithms-would-I-need-to-understand-to-create-similar-functionality-on-a-small-scale?redirected_qid=828413).

<hr>
