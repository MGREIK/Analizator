from collections import Counter
import cv2 as cv
import numpy as np

from .colors import color_ranges


BGR = np.array([191, 191, 191])
upper = BGR + 10
lower = BGR - 10


def read_image(path):
    return cv.imread(path)


def find_mask(image):
    return cv.inRange(image, lower, upper)


def find_contours(image):
    (cnts, hierarchy) = cv.findContours(
        image.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    print("Found %d black shapes" % (len(cnts)))
    return cnts


def show_contours(contours, image):
    cv.drawContours(image, contours, -1, (0, 0, 255), 2)

    cv.imshow("contours", image)


def get_main_contour(contours):
    sorted_contours = sorted(contours, key=len, reverse=True)
    return sorted_contours[0]


def find_red_contour(image):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    contour_mask = cv.inRange(hsv, lower_red, upper_red)
    contours, _ = cv.findContours(
        contour_mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    return contours


def find_mask_inside_contour(image, contour):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv.drawContours(mask, [contour[0]], 0, (255), -1)
    return mask


def find_pixel_ranges(image):
    image = read_image(image)
    contour = find_red_contour(image)
    mask = find_mask_inside_contour(image, contour)
    masked_pixels = image[mask == 255]
    arr = np.array(masked_pixels)
    test = np.array([x for x in color_ranges.keys()])
    matches = np.any(np.all(arr[:, np.newaxis, :] == test, axis=2), axis=1)
    matching_indices = np.where(matches)[0]
    colors = arr[matching_indices]
    ranges = [color_ranges[tuple(color)] for color in colors]
    ranges_repeat = Counter(ranges)
    return ranges_repeat


def boloto_percentage(ranges: dict[tuple, int], lower_bound: float = 0.1) -> float:
    total = sum(ranges.values())
    percents_of_shit = {key: value / total for key, value in ranges.items()}
    res = 0
    for [range, percent] in percents_of_shit.items():
        if range[0] >= lower_bound:
            res += percent
    return res


if __name__ == "__main__":
    aoao = find_pixel_ranges('./images/b.png')
    print(boloto_percentage(aoao))
