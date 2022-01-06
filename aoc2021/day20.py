from util.helpers import readlines, rpath, tpath


def frameval(img, x, y, even):
  val = 0
  i = 8
  for p in ((x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y),   (x, y),   (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1)):
    val |= (1 << i) if img.get(p, ('.' if even else '#')) == '#' else 0
    i -= 1
  return val

def enhance(image, enhancement, even, minbound, maxbound):
  newpic = {}
  for y in range(minbound, maxbound):
    for x in range(minbound, maxbound):
      newpic[x, y] = enhancement[frameval(image, x, y, even)]
  return newpic

def part1(image, enhancement, imgsz):
  minbound, maxbound = 0, imgsz+1
  for i in range(2):
    minbound -= 1
    maxbound += 1
    image = enhance(image, enhancement, i%2==0, minbound, maxbound)
  return tuple(image.values()).count('#')

def part2(image, enhancement, imgsz):
  minbound, maxbound = 0, imgsz+1
  for i in range(50):
    minbound -= 1
    maxbound += 1
    image = enhance(image, enhancement, i%2==0, minbound, maxbound)
  return tuple(image.values()).count('#')

def get_data():
  data = readlines(rpath('day20.txt', 'aoc2021'), sep='\n\n')
  enhancement, image = data
  image = image.strip().split('\n')
  imgsz = len(image)
  image = {
    (x, y): c
    for y, line in enumerate(image)
    for x, c in enumerate(line)}
  return image, enhancement, imgsz

if __name__ == '__main__':
  data = get_data()
  print(part1(*data))
  print(part2(*data))
