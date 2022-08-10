import sys
import math


def read_TGA(filename):
    with open(filename, "rb") as f:
        byte = f.read()
        data = [int(x) for x in byte]
        image_width = data[13] * 256 + data[12]
        image_height = data[15] * 256 + data[14]
        header = byte[:18]
        source = data[18:18 + (3 * image_height * image_width)]
        footer = byte[18 + (3 * image_height * image_width):]
        source.reverse()
        pixels_list = []
        for i in range(image_height):
            for j in range(image_width):
                index = (image_width * i + j) * 3
                pixels_list.append((source[index],
                                    source[index + 1],
                                    source[index + 2])
                                   )
        return header, footer, pixels_list, image_width, image_height


def write_TGA(header, source_to_bytes, footer, filename):
    with open(filename, "wb") as out:
        out.write(header)
        out.write(source_to_bytes)
        out.write(footer)


def pixels_to_bytes(pixels):
    pixels.reverse()
    pixels_bytes = []
    for pixel in pixels:
        for color in reversed(pixel):
            pixels_bytes.append(color)

    return bytes(pixels_bytes)


def distance_euclid(source, variable):
    return sum((sourceElement - variableElement) ** 2
               for sourceElement, variableElement
               in zip(source, variable))


def diff_encoding_color(pixels, bits):
    prev = 0
    max_value = 2 ** bits
    min_value = -2 ** bits
    diffs = []
    M = list(range(min_value, max_value + 1))
    for item in pixels:
        temp = item - prev
        current = min(M, key=lambda x: abs(x - temp))
        diffs.append(current)
        prev = sum(diffs)

    return diffs


def diff_encoding(pixels, bits):
    result = []
    result_blue = []
    result_green = []
    result_red = []
    for item in pixels:
        result_blue.append(item[0])
        result_green.append(item[1])
        result_red.append(item[2])
    result_blue = diff_encoding_color(result_blue, bits)
    result_green = diff_encoding_color(result_green, bits)
    result_red = diff_encoding_color(result_red, bits)

    for i in range(len(result_blue)):
        result.append((result_blue[i], result_green[i], result_red[i]))
    return result


def diff_decoding_color(diffs):
    result = []
    for i in range(len(diffs)):
        result.append(sum(diffs[:i + 1]))
    return result


def diff_decoding(diffs):
    result = []
    result_blue = []
    result_green = []
    result_red = []
    for item in diffs:
        result_blue.append(item[0])
        result_green.append(item[1])
        result_red.append(item[2])
    result_blue = diff_decoding_color(result_blue)
    result_green = diff_decoding_color(result_green)
    result_red = diff_decoding_color(result_red)

    for i in range(len(result_blue)):
        result.append((result_blue[i], result_green[i], result_red[i]))
    return result


def msr_result(original, new):
    return (1 / len(original)) * sum([distance_euclid(original[i], new[i]) for i in range(len(original))])


def msr_color(original, new, i):
    result = 0
    for j in range(len(original)):
        result += (original[j][i] - new[j][i]) ** 2
    return result / len(original)


def msr_snr(original):
    ref = [0, 0, 0]
    return (1 / len(original)) * sum([distance_euclid(original[i], ref) for i in range(len(original))])


def msr_snr_color(original, i):
    result = 0
    for j in range(len(original)):
        result += (original[j][i] - 0) ** 2
    return result / len(original)


def main():
    file = sys.argv[1]
    out = sys.argv[2]
    bits = int(sys.argv[3])
    header, footer, pixels, image_width, image_height = read_TGA(file)
    diffs = diff_encoding(pixels, bits)
    result = diff_decoding(diffs)
    msr = msr_result(pixels, result) / 3
    msr_r = msr_color(pixels, result, 2)
    msr_g = msr_color(pixels, result, 1)
    msr_b = msr_color(pixels, result, 0)
    msr_snr_res = msr_snr(pixels) / 3
    msr_snr_r = msr_snr_color(pixels, 2)
    msr_snr_g = msr_snr_color(pixels, 1)
    msr_snr_b = msr_snr_color(pixels, 0)
    print("MSE= ", msr)
    print("MSE (R)= ", msr_r)
    print("MSE (G)= ", msr_g)
    print("MSE (B)= ", msr_b)
    print("SNR= ", 10 * math.log10(msr_snr_res))
    print("SNR (R)= ", 10 * math.log10(msr_snr_r))
    print("SNR (G)= ", 10 * math.log10(msr_snr_g))
    print("SNR (B)= ", 10 * math.log10(msr_snr_b))
    write_TGA(header, pixels_to_bytes(result), footer, out)


if __name__ == '__main__':
    main()
