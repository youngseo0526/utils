# file, directory compare
import filecmp

fd = filecmp.dircmp('a', 'b')

for a in fd.right_only:
  print("a only: %s" %a)