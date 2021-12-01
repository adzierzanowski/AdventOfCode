from util.helpers import readlines, rpath, tpath
from intcode import Intcode
from functools import reduce


def test_springscript(prog):
  def run(gnd, debug=False):
    if debug:
      print(len(prog.split('\n')))
    regs = {reg: False for reg in 'ABCDEFGHITJ'}

    pos = gnd.index('@')
    for offset, reg in enumerate('ABCDEFGHI'):
      if gnd[pos+offset+1] == '#':
        regs[reg] = True

    for line in prog.split('\n'):
      lsplit = line.split(' ')
      if 'WALK' in line or 'RUN' in line:
        break

      cmd, r1, r2 = lsplit
      if 'WALK' in prog:
        assert r1 in 'ABCDTJ'
      else:
        assert r1 in 'ABCDEFGHITJ'

      assert r2 in 'TJ'
      if cmd == 'AND':
        out = f'{r1 if regs[r1] else r1.lower()} && {r2 if regs[r2] else r2.lower()} == '
        regs[r2] = regs[r1] and regs[r2]
        out += f'{regs[r2]} -> {r2}'
      elif cmd == 'OR':
        out = f'{r1 if regs[r1] else r1.lower()} || {r2 if regs[r2] else r2.lower()} == '
        regs[r2] = regs[r1] or regs[r2]
        out += f'{regs[r2]} -> {r2}'
      elif cmd == 'NOT':
        out = f'!{r1 if regs[r1] else r1.lower()} == '
        regs[r2] = not regs[r1]
        out += f'{regs[r2]} -> {r2}'
      if debug:
        print(f'{out:40}', end='')
        for reg, val in regs.items():
          print(reg if val else reg.lower(), end='')
        print()

    print('jump!' if regs['J'] else 'stay')
    g0 = gnd[:pos+4]
    g1 = gnd[pos+4+1:]

    if regs['J']:
      if gnd[pos+4] == '#':
        g0 += '\x1b[38;5;2mX\x1b[0m'
      else:
        g0 += '\x1b[38;5;1mX\x1b[0m'
    else:
      g0 = gnd
      g1 = ''

    print('->', end='  ')
    for reg, val in regs.items():
      if reg not in 'TJ':
        print(reg if val else reg.lower(), end='')
    print()
    print('->', ''.join(g0+g1))
    if debug:
      print()

  #run('@#.##.########', debug=True)
  run('@#..###.#..###', debug=True)

def part1(data):
  prog = '\n'.join((
    'NOT C J',
    'AND D J',
    'NOT A T',
    'OR T J',
    'WALK\n',
  ))

  cpu = Intcode()
  cpu.load_program(data)
  cpu.set_ascii_mode(True)
  cpu.feed_inputs(*prog)
  cpu.run()
  out = cpu.read_output()

  try:
    print(''.join([chr(c) for c in out]))
  except ValueError:
    return(out[-1])


def part2(data):
  prog = '\n'.join((
    'NOT I J',
    'AND H J',
    'NOT F T',
    'AND G T',
    'OR T J',
    'AND D J',
    'AND H J',
    'NOT A T',
    'OR T J',
    'NOT C T',
    'AND D T',
    'OR T J',
#    'NOT C T',
#    'AND D T',
#    'OR T J',

    'RUN\n',
  ))

  prog = '\n'.join((
    'NOT A T',
    'OR T J',

    'AND G T',
    'AND D T',
    'AND H T',
    'OR T J',

    'NOT C T',
    'AND D T',
    'OR T J',

    'RUN\n'
  ))

  prog = '\n'.join((
    'NOT A J',

    'OR E T',
    'OR C T',
    'NOT T T',
    'AND D T',
    'OR T J',

    'OR B T',
    'OR E T',
    'NOT T T',
    'OR T J',

    'NOT I T',
    'AND D T',
    'OR T J',

    'RUN\n'
  ))

  cpu = Intcode()
  cpu.load_program(data)
  cpu.set_ascii_mode(True)
  cpu.feed_inputs(*prog)
  cpu.run()
  out = cpu.read_output()

  try:
    print(''.join([chr(c) for c in out]))
  except ValueError:
    return(out[-1])
  test_springscript(prog)



def truth_table():
  funcdef = (
    'aBCDEFGHI',
    'ABcDefGHI',
    'AbcDeFGHI',
    'abcDEFGHI',
    'AbCDeFGHI',
    'ABcDEfGHi',
    'ABcDefgHi',
  )

  def func(q):
    q = [bool(int(x)) for x in f'{q:09b}']
    print(''.join([str(int(x)) for x in q]), end=' ')

    sum_ = False
    for fd in funcdef:
      prod = True
      for i, c in enumerate(fd):
        if c.isupper():
          prod = prod and q[i]

        elif c.islower():
          prod = prod and not q[i]
      sum_ = sum_ or prod

    print(sum_)
    return sum_

  mterms = []
  dontcares = []
  for i in range(2**9):
    if func(i):
      mterms.append(str(i))
    else:
      dontcares.append(str(i))


  print(' '.join(mterms))
  print(' '.join(dontcares))

if __name__ == '__main__':
  data = readlines(rpath('day21.txt', 'aoc2019'), sep=',', conv=int)
  #print(part1(data))
  #print(part2(data))
  truth_table()
