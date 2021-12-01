from util.helpers import readlines, rpath, tpath
from intcode import Intcode


def part1(data):
  cpu = Intcode()
  cpu.load_program(data)
  cpu.run()
  scaf = ''.join([chr(c) for c in cpu.read_output()]).strip().split('\n')

  scafpts = [(x, y) for y, line in enumerate(scaf) for x, c in enumerate(line) if c == '#']
  isect = []
  for pt in scafpts:
    ptx, pty = pt
    if all([(x, y) in scafpts for x, y in ((ptx+1,pty), (ptx-1,pty), (ptx,pty-1), (ptx,pty+1))]):
      isect.append((ptx, pty))
  return sum((x*y for x, y in isect))



def part2(data):
  cpu = Intcode(wfi_mode=True)
  cpu.set_ascii_mode(True)
  cpu.load_program(data)
  cpu.ram[0] = 2
  cpu.run()

  cpu.feed_inputs(*'A,B,A,B,C,C,B,A,C,A\nL,10,R,8,R,6,R,10\nL,12,R,8,L,12\nL,10,R,8,R,8\nn\n')
  cpu.run()

  #cam = ''.join([chr(x) if chr(x).isprintable() or x == 10 and x < 0x110000 else str(x) for x in cpu.read_output() ]).strip().split('\n')
  cam = cpu.read_output()
  print(cam)


  '''
  from PIL import Image
  img = Image.new('RGB', (len(cam[0]), len(cam)), 'black')
  pix = img.load()
  for y, line in enumerate(cam):
    print(line)

    for x, char in enumerate(line):
      if char == '#':
        pix[x,y] = (0, 255, 128)

  img.save('day17.bmp')
  '''

# L10 R8 R6 R10 L12 R8 L12 L10 R8 R6 R10 L12 R8 L12 L10 R8 R8 L10 R8 R8 L12 R8 L12 L10 R8 R6 R10 L10 R8 R8 L10 R8 R6 R10
# L10 R8 R6 R10  = A
# L12 R8 L12 = B
# L10 R8 R8 = C
# A B A B C C B A C A


  print(cpu.outputs)






if __name__ == '__main__':
  data = readlines(rpath('day17.txt', 'aoc2019'), conv=int, sep=',')
  print(part1(data))
  print(part2(data))
