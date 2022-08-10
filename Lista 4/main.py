import math


class Pixel:
    red = 0
    green = 0
    blue = 0

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __sub__(self, other):
        return Pixel((self.red - other.red) % 256, (self.green - other.green) % 256, (self.blue - other.blue) % 256)

    def __add__(self, other):
        return Pixel((self.red + other.red) % 256, (self.green + other.green) % 256, (self.blue + other.blue) % 256)

    def __floordiv__(self, other):
        return Pixel(self.red // other, self.green // other, self.blue // other)


def newStandard(a, b, c):
    if c >= max(a, b):
        return min(a, b)
    if c <= min(a, b):
        return max(a, b)
    return a + b - c


def predictionMode(mode, a, b, c):
    return {
        0: Pixel(0, 0, 0),
        1: a,
        2: b,
        3: c,
        4: a + b - c,
        5: a + ((b - c) // 2),
        6: b + ((a - c) // 2),
        7: (a + b) // 2,
        8: Pixel(newStandard(a.red, b.red, c.red), newStandard(a.green, b.green, c.green),
                 newStandard(a.blue, b.blue, c.blue))
    }[mode]


def encode(pixels, width, height, mode):
    encoded = []
    for i in range(width):
        for j in range(height):
            if j == 0:
                a = Pixel(0, 0, 0)
            else:
                a = pixels[width * i + j - 1]
            if i == 0:
                b = Pixel(0, 0, 0)
            else:
                b = pixels[width * (i - 1) + j]
            if i == 0 and j == 0:
                c = Pixel(0, 0, 0)
            else:
                c = pixels[width * (i - 1) + (j - 1)]
            encoded.append(pixels[width * i + j] - predictionMode(mode, a, b, c))

    return encoded


def entropy(pixels, TYPE):
    result = {}
    size = 0
    ent = 0
    for i in range(256):
        result[i] = 0
    if TYPE == 'all':
        for pixel in pixels:
            result[pixel.red] += 1
            result[pixel.green] += 1
            result[pixel.blue] += 1
            size += 3
    else:
        for pixel in pixels:
            result[getattr(pixel, TYPE)] += 1
            size += 1
    for value in result.values():
        if value == 0:
            continue
        ent = ent + value * (-math.log2(value))
    ent = ent / size + math.log2(size)
    return ent


def TGA(file):
    with open(file, "rb") as f:
        byte = f.read()
        data = [int(x) for x in byte]
        width = data[13] * 256 + data[12]
        height = data[15] * 256 + data[14]
        source = data[18:]
        pixelsList = []
        for i in range(height):
            for j in range(width):
                index = (width * i + j) * 3
                pixelsList.append(Pixel(source[index], source[index + 1], source[index + 2]))
        return pixelsList, width, height


def main():
    pred = {
        0: 'No prediction',
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'A+B-C',
        5: 'A+(B-C)/2',
        6: 'B+(A-C)/2',
        7: '(A+B)/2',
        8: 'New Standard'
    }
    file = 'example0.tga'
    pixels, width, height = TGA(file)
    types = ['all', 'red', 'green', 'blue']
    modes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    outcome = []
    print('\033[92m' + "Starting entropy:"+'\033[0m')
    for TYPE in types:

        print(TYPE, (entropy(pixels, TYPE)))
        for mode in modes:
            outcome.append((mode, TYPE, entropy(encode(pixels, width, height, mode), TYPE)))
    print('\033[92m'+"Encoded entropy:"+'\033[0m')
    for item in outcome:
        print(pred[item[0]], item[1], "||", item[2])


if __name__ == '__main__':
    main()
