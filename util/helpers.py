import math
import os


def rpath(path, prefix=''):
  return os.path.join(prefix, 'data', 'real', path)

def tpath(path, prefix=''):
  return os.path.join(prefix, 'data', 'test', path)

def identity(x):
  return x

def readlines(filename, sep='\n', conv=identity):
  with open(filename, 'r') as f:
    data = [conv(l.strip()) for l in f.read().split(sep) if l.strip() != '']
  return data

def readraw(filename, sep=None, conv=identity):
  with open(filename, 'r') as f:
    data = f.read()
    return [conv(x) for x in data.split(sep)] if sep else conv(data)

def tribonacci(n):
  # https://mathworld.wolfram.com/TribonacciNumber.html
  n1 = 1/3 * (19 + 3 * math.sqrt(33)) ** (1/3)
  n2 = 1/3 * (19 - 3 * math.sqrt(33)) ** (1/3)
  num1 = (n1 + n2 + (1/3)) ** (n+1)
  num2 = (586 + 102 * math.sqrt(33)) ** (1/3)
  num = num1 * num2

  den1 = (586 + 102 * math.sqrt(33)) ** (2/3)
  den2 = (586 + 102 * math.sqrt(33)) ** (1/3)
  den = den1 + 4 - 2 * den2

  return round(3 * (num / den))
