from PIL import Image
from math import sqrt


def normalize_array(normalize_num):
    """
    Функция - декоратор. Принимает число. Делит каждый элемент массива на заданное число
    """
    def decorator(function):
        def normalize(*args, **kwargs):
            normalized = map(lambda x: x / normalize_num, function(*args, **kwargs))
            return list(normalized)
        return normalize
    return decorator


@normalize_array(255)
def image_to_array(image, width=300, height=300):
    """
    Функция для обрезки и представления изображения в виде одномерного массива
    """
    # Обрезка изображения
    img = Image.open(image).resize((width, height))

    # Находим каждый пиксель
    pixels = [img.getpixel((x, y)) for x in range(width - 1) for y in range(height - 1)]

    # unpacking
    array = list()
    for pixel in pixels:
        array += [*pixel]

    return array


def euclidean(vector1, vector2):
    """
    Функция для поиска евклидового расстояния
    """
    result = float()
    for i in range(len(vector1)):
        result += (vector1[i] - vector2[i]) ** 2
    return sqrt(result)
