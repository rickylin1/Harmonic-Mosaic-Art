# Extracts post images from instagram posts folder.
# @see: https://discovery.cs.illinois.edu/guides/project-mosaic/instagram/
# @author: Wade Fagen-Ulmschneider and Michelle Jun

from os import listdir, makedirs
from os.path import isfile, join, isdir
from shutil import copyfile

if not isdir("posts"):
  print("No `posts` directory found.")
  exit(1)

# Make the destination folder:
DEST_PATH = "insta-tiles"
makedirs(DEST_PATH, exist_ok=True)

# Find all instagram images:
dirs = [f for f in listdir("posts") if isdir(join("posts", f))]
for d in dirs:
  d2 = join("posts", d)
  files = [f for f in listdir(d2) if isfile(join(d2, f))]

  for f in files:
    if f.endswith(".jpg"):
      src = join(d2, f)
      dest = join(DEST_PATH, f)
      copyfile(src, dest)
      print(f"{src} -> {dest}")
