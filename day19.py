from helpers import readlines, rpath, tpath


def parse_rules(rules):
  ruleset = {}
  for line in rules.split('\n'):
    rule_id, rule = line.split(': ')
    if rule == '"a"':
      ruleset[int(rule_id)] = 'a'
    elif rule == '"b"':
      ruleset[int(rule_id)] = 'b'
    else:
      ruleset[int(rule_id)] = [[int(x) for x in q.split(' ')] for q in rule.split(' | ')]
  return ruleset


def match(ruleset, rule, string):
  if not rule and not string:
    return True

  elif not rule or not string:
    return False

  first = ruleset[rule[0]]

  if isinstance(first, str):
    if first == string[0]:
      return match(ruleset, rule[1:], string[1:])
  elif isinstance(first, list):
    matches = []
    for subrule in first:
      matches.append(match(ruleset, subrule + rule[1:], string))
    return any(matches)


def part1(ruleset, strings):
  matches = [match(ruleset, [0], string) for string in strings]
  return len([m for m in matches if m is True])

def part2(ruleset, strings):
  ruleset[8] = [[42], [42, 8]]
  ruleset[11] = [[42, 31], [42, 11, 31]]
  matches = [match(ruleset, [0], string) for string in strings]
  return len([m for m in matches if m is True])


if __name__ == '__main__':
  data = readlines(rpath('day19.txt'), sep='\n\n')

  rules, strings = data[0], data[1]
  strings = strings.split('\n')
  ruleset = parse_rules(rules)

  print(part1(ruleset, strings))
  print(part2(ruleset, strings))
