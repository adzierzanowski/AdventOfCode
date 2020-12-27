from helpers import readlines, rpath, tpath

def parse(line):
  ings, algs = line.split(' (contains ')
  ings = ings.split(' ')
  algs = algs[:-1].split(', ')
  return ings, algs

def get_mapping(data):
  amap = {}
  for ings, algs in data:
    for a in algs:
      if a in amap:
        amap[a] &= set(ings)
      else:
        amap[a] = set(ings)
  return amap

def part1(data):
  all_ings_list = sum([d[0] for d in data],[])
  all_ings = set(all_ings_list)
  unsafe_ings = set.union(*get_mapping(data).values())
  safe_ings = all_ings - unsafe_ings
  return sum([all_ings_list.count(i) for i in safe_ings])

def part2(data):
  mapping = get_mapping(data)

  identified = {}
  while len(identified) != len(mapping.keys()):
    for agen, ings in mapping.items():
      if len(ings) == 1:
        ing = ings.pop()
        identified[agen] = ing
        for a, i in mapping.items():
          mapping[a] -= {ing}
        break

  return ','.join([x[1] for x in sorted(identified.items(), key=lambda m: m[0])])


if __name__ == '__main__':
  data = readlines(rpath('day21.txt'), conv=parse)

  print(part1(data))
  print(part2(data))
