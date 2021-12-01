from util.helpers import readlines, rpath, tpath


def get_layers(data, w, h):
  return [data[i:i+w*h] for i in range(0, len(data), w*h)]

def part1(layers):
  min0layer = min(layers, key=lambda m: m.count('0'))
  return min0layer.count('1') * min0layer.count('2')

def part2(layers, w, h):
  img = layers[0]
  for layer in layers[1:]:
    new_img = ''
    for i, l in zip(img, layer):
      new_img += l if i == '2' else i
    img = new_img

  img = [img[i:i+w] for i in range(0, len(img), w)]
  for line in img:
    print(line.replace('0', ' ').replace('1', '#'))


if __name__ == '__main__':
  data = readlines(rpath('day08.txt', 'aoc2019'))[0]
  w, h = 25, 6
  layers = get_layers(data, w, h)

  print(part1(layers))
  part2(layers, w, h)
