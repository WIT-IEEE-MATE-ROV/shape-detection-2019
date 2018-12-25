# What's this?
This is a set of files that are similar to what this code will be dealing with when in use.

There are two folders: `easyimages` and `realimages`. `easyimages` contains images that don't need any
processing or altering before they are ready to be interpreted-- they are already black and white, the shapes
have clean edges, etc. This allows them to be an easier place to start and may make things easier to debug in 
the future (eliminate the image manipulation as a potential source of error).

`realmages` contains images that are more realistic: They are photos, so they may have inconsistent lighting, 
they may not be directly overhead, color balance may be slightly off, and so on. Image manipulation will need
to take place before they can be used.

# The file names
There are several different shapes that need to be identified: Triangles, Squares, Lines, or Circles. The
file name is 4 digits, with each digit representing the amount of each shape found in the image. For example,
the file name "1230.png" indicates that the image has 1 triangle, 2 squares, 3 lines, and 0 circles.

# Generating more images
The job of `make-easyimages.py` is to generate some images for use in testing. It still needs to be done,
but when complete, will allow for nice automated testing.