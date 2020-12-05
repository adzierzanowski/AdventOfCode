def readlines(filename, separator='\n'):
  with open(filename, 'r') as f:
    data = [l.strip() for l in f.read().split(separator) if l.strip() != '']
  return data
