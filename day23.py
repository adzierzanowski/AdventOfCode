from helpers import readlines, rpath, tpath


class Node:
  def __init__(self, val, prev=None, next_=None):
    self.val = val
    self.prev = prev
    self.next = next_

  def __repr__(self):
    return f'<{self.val}>'

  @staticmethod
  def make_nodes(data):
    nodes = []
    for i, val in enumerate(data):
      p = i-1 if i > 0 else -1
      n = i+1 if i < len(data)-1 else 0
      nodes.append(Node(val, prev=p, next_=n))

    for n in nodes:
      n.prev = nodes[n.prev]
      n.next = nodes[n.next]
    return List(nodes)

class List:
  def __init__(self, nodes):
    self._nodes = nodes
    self.active = self._nodes[0]
    self.max = max(enumerate(self._nodes), key=lambda m: m[1].val)
    self.idxs = {n.val: i for i, n in enumerate(self._nodes)}

  def nodes(self):
    ns = []
    n = self.active.next
    ns.append(self.active)
    while n != self.active:
      ns.append(n)
      n = n.next
    return ns

  def __repr__(self):
    lsrepr = " ".join([f"({repr(n)})"
                       if n == self.active
                       else repr(n)
                       for n in self.nodes()])
    return f'<L:{lsrepr}>'

  def get(self, nodeval):
    return self._nodes[self.idxs[nodeval]]

  def take3(self):
    c1 = self.active.next
    c2 = self.active.next.next
    c3 = self.active.next.next.next
    c4 = self.active.next.next.next.next
    cups = c1, c2, c3
    self.active.next = c4
    c4.prev = self.active
    return cups

  def put(self, nodes, dst):
    n = dst.next
    dst.next = nodes[0]
    nodes[0].prev = dst
    n.prev = nodes[-1]
    nodes[-1].next = n
    self.active = self.active.next

  def dst(self, taken):
    i = self.active.val - 1
    if i < 1:
      i = self.max[1].val
    n = self._nodes[self.idxs[i]]

    while n in taken:
      i = n.val - 1
      if i < 1:
        i = self.max[1].val

      n = self._nodes[self.idxs[i]]

    return n

def part1(data):
  ls = Node.make_nodes(data)

  for i in range(100):
    cups = ls.take3()
    ls.put(cups, ls.dst(cups))

  ls.active = ls.get(1)
  return ''.join([str(n.val) for n in ls.nodes()[1:]])

def part2(data):
  data += list(range(max(data)+1, 1_000_001))
  assert len(data) == 1_000_000
  ls = Node.make_nodes(data)

  for i in range(10_000_000):
    cups = ls.take3()
    ls.put(cups, ls.dst(cups))

  one1 = ls.get(1).next
  one2 = one1.next
  return one1.val * one2.val


if __name__ == '__main__':
  data = readlines(rpath('day23.txt'), conv=lambda m: [int(x) for x in m])[0]

  print(part1(data))
  print(part2(data))
