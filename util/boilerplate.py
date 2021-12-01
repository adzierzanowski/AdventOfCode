import os
import sys


def day_scaffold(year, day):
  path = os.path.join(f'aoc{year}', f'day{day:02}.py')
  datapath = os.path.join(f'aoc{year}', 'data', 'real', f'day{day:02}.txt')
  testpath = os.path.join(f'aoc{year}', 'data', 'test', f'day{day:02}.txt')


  if os.path.exists(path):
    print(f'{path} already exists', file=sys.stderr)
    return

  with open(path, 'w') as f:
    f.write('\n'.join((
      'from util.helpers import readlines, rpath, tpath',
      '',
      '',
      'def part1(data):',
      '  pass',
      '',
      'def part2(data):',
      '  pass',
      '',
      '',
      'if __name__ == \'__main__\':',
      f'  data = readlines(rpath(\'day{day:02}.txt\', \'aoc{year}\'))',
      '  print(part1(data))',
      '  print(part2(data))',
      ''
    )))

  with open(datapath, 'w') as f:
    pass
  with open(testpath, 'w') as f:
    pass
