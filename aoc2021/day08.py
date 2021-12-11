from util.helpers import readlines, rpath, tpath


digcnt = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]

def part1(data):
  outputs = [[len(x) for x in line.split(' | ')[1].split(' ')] for line in data]
  return len([x for x in sum(outputs, []) if x in (2,3,4,7)])

def part2(data):
  outsum = 0
  '''
        s1
     s2    s3
        s4
     s5    s6
        s7
  '''
  for line in data:
    digits = [''.join(sorted(x)) for x in line.replace(' | ', ' ').split(' ')]
    one = [d for d in digits if len(d) == 2][0]
    four = [d for d in digits if len(d) == 4][0]
    seven = [d for d in digits if len(d) == 3][0]

    s1 = ''.join([x for x in seven if x not in one])
    s24 = ''.join([x for x in four if x not in one])
    s2, s4 = s24 # not in order
    five = [d for d in digits if len(d) == 5 and s2 in d and s4 in d][0]
    s7 = [x for x in five if x not in seven and x not in four][0]
    s6 = [x for x in five if x in one][0]
    s3 = [x for x in one if x not in five][0]
    two = [d for d in digits if len(d) == 5 and s6 not in d][0]
    s5 = [x for x in two if x not in seven and x not in four and x not in five][0]
    s2 = [x for x in four if x not in two and x not in one][0]
    s4 = [x for x in s24 if x != s2][0]

    three = ''.join(sorted([s1, s3, s4, s6, s7]))
    six = ''.join(sorted([s1, s2, s4, s5, s6, s7]))
    eight = 'abcdefg'
    nine = ''.join(sorted([s1, s2, s3, s4, s6, s7]))
    zero = ''.join(sorted([s1, s2, s3, s5, s6, s7]))

    digs = [zero, one, two, three, four, five, six, seven, eight, nine]

    _, outputs = line.split(' | ')
    outval = int(''.join([str(digs.index(''.join(sorted(d)))) for d in outputs.split(' ')]))
    outsum += outval
  return outsum

def get_data():
  return readlines(rpath('day08.txt', 'aoc2021'))


if __name__ == '__main__':
  data = get_data()
  print(part1(data))
  print(part2(data))
