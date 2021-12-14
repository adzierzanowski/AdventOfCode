from util.helpers import readlines, rpath, tpath


def polymerize(template, chars, rules):
  temp, chrs = {**template}, {**chars}
  for chunk, cnt in template.items():
    c = rules[chunk]
    c0, c1 = chunk[0] + c, c + chunk[1]
    chrs[c] += cnt
    temp[chunk] -= cnt
    temp[c0] += cnt
    temp[c1] += cnt
  return temp, chrs

def poly_char_diff(count, template, chars, rules):
  for _ in range(count):
    template, chars = polymerize(template, chars, rules)
  return max(chars.values()) - min(chars.values())


def part1(template, chars, rules):
  return poly_char_diff(10, template, chars, rules)

def part2(template, chars, rules):
  return poly_char_diff(40, template, chars, rules)

def get_data():
  data = readlines(rpath('day14.txt', 'aoc2021'))
  template = data[0]
  rules = {k: v for k, v in [d.split(' -> ') for d in data[1:]]}
  chunks = tuple((template[i] + template[i+1] for i in range(len(template)-1)))
  chars = {k: template.count(k) for k in ''.join(rules.values())}
  template = {
    **{k: 0 for k in rules},
    **{chunk: chunks.count(chunk) for chunk in rules}
  }
  return template, chars, rules


if __name__ == '__main__':
  data = get_data()
  print(part1(*data))
  print(part2(*data))
