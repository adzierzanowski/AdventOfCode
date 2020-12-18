import sys

from timeit import timeit
import subprocess

def run_(day):
  subprocess.call(('python3', f'day{day}.py'))

if __name__ == "__main__":
  print(timeit(lambda : run_(sys.argv[1]), number=1))
