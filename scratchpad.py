
s = 'abcd'

def all_(ls):
  for c in ls:
    if not c:
      return False
  return True

for i in range(5):
  if all_((i < len(s), s[i] == 'a')):
    print(s[i])
