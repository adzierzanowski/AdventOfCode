from util.helpers import readlines, rpath, tpath
from intcode import Intcode
from queue import Queue


def part1(data):
  cpus = [Intcode(wfi_mode=True) for _ in range(50)]
  for i, cpu in enumerate(cpus):
    cpu.load_program(data)
    cpu.run()
    cpu.feed_inputs(i)

  queues = {k: Queue() for k in range(50)}

  while True:
    for i, cpu in enumerate(cpus):
      q = queues[i]
      if cpu.wait_for_input:
        while not q.empty():
          cpu.feed_inputs(*q.get())
        cpu.feed_inputs(-1)

      cpu.run()
      while out := cpu.read_output(n=3):
        dst, x, y = out
        if dst == 255:
          return y
        queues[dst].put((x, y))

def part2(data):
  cpus = [Intcode(wfi_mode=True) for _ in range(50)]
  for i, cpu in enumerate(cpus):
    cpu.load_program(data)
    cpu.run()
    cpu.feed_inputs(i, -1)

  queues = {k: Queue() for k in range(50)}
  nat = None
  last_nat_tx = None

  while True:
    if nat is not None and all((q.empty() for q in queues.values())):
      cpus[0].feed_inputs(*nat)
      if last_nat_tx == nat:
        return nat[1]
      else:
        last_nat_tx = nat

    for i, cpu in enumerate(cpus):
      q = queues[i]
      if cpu.wait_for_input:
        while not q.empty():
          cpu.feed_inputs(*q.get())

      cpu.run()
      while out := cpu.read_output(n=3):
        dst, x, y = out
        if dst == 255:
          nat = x, y
        else:
          queues[dst].put((x, y))


if __name__ == '__main__':
  data = readlines(rpath('day23.txt', 'aoc2019'), conv=int, sep=',')
  print(part1(data))
  print(part2(data))
