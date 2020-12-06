def identity(x):
  return x

def readlines(filename, sep='\n', conv=identity):
  with open(filename, 'r') as f:
    data = [conv(l.strip()) for l in f.read().split(sep) if l.strip() != '']
  return data
