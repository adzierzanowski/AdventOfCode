solvePart1 ← {≢⍸(((1↓⍵)-¯1↓⍵)>0)}
solvePart2 ← {solvePart1 ((2↓⍵)+(1↓(¯1↓⍵))+(¯2↓⍵))}
