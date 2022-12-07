from aoc_util import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  7   00:25:13    1374      0   00:43:47    2695      0
"""

day = 7

class File():
    def __init__(self, name, parent, size=0):
        assert(isinstance(size, int))
        self.name = name
        self.parent = parent
        self.children = []
        # Files are "directories" if they have size == 0.
        self.size = size
        self.total = size

    def isDir(self):
        return self.size == 0

    def addChild(self, child):
        self.children.append(child)

    def getChild(self, name):
        for c in self.children:
            if c.name == name:
                return c
        return None

    def totalSize(self):
        # If this is a dir, total will be initialized to 0.
        if self.total == 0:
            self.total = sum([c.totalSize() for c in self.children])
        return self.total

    def printDir(self, depth=0):
        spec = "dir" if self.isDir() else "file, size={}".format(self.size)
        print("{}- {} ({})".format("  " * depth, self.name, spec))
        for c in self.children:
            c.printDir(depth + 1)

    def constructFs(lines):
        root = File("/", None)
        current = root
        for l in lines:
            if l == "$ cd /" or l == "$ ls":
                continue
            elif l == "$ cd ..":
                current = current.parent
            elif l.startswith("$ cd "):
                # If the child doesn't exist already, then get rekt
                dest = l.split()[2]
                current = current.getChild(dest)
            elif l.startswith("dir"):
                # directory name (ex. "dir <some name>")
                current.addChild(File(l.split()[1], current))
            else:
                # file name with size (ex. "103661 lgt.swt")
                fileSize, fileName = l.split()
                current.addChild(File(fileName, current, int(fileSize)))
        return root

def solveA(lines):
    # Helper function that adds up all directories of total size < 100,000.
    def hundos(file):
        if not file.isDir():
            return 0
        cumul = sum([hundos(c) for c in file.children])
        s = file.totalSize()
        return cumul + (s if s <= 100_000 else 0)

    root = File.constructFs(lines)
    return hundos(root)

def solveB(lines):
    # Helper fn that identifies the smallest dir that is larger than minSize.
    def smallestRemoveable(current, minSize, smallest):
        for c in current.children:
            if not c.isDir():
                continue
            if c.totalSize() >= minSize and c.totalSize() < smallest:
                smallest = c.totalSize()
            smallest = smallestRemoveable(c, minSize, smallest)
        return smallest

    root = File.constructFs(lines)
    maxSize = 70_000_000
    needed = 30_000_000
    minSize = needed - (maxSize - root.totalSize())
    return smallestRemoveable(root, minSize, maxSize)

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 95437, 24933642)
