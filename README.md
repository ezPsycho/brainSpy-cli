# brainSpy-cli

Transform MNI coordinate to AAL and BA structural names.

usage: `brainSpy.py [-h] [-r radius] [-t threshold]`

optional arguments:
```
  -h, --help            show this help message and exit
  -r radius, --radius radius
                        the radius of fuzzy query, if provided, brainSpy will
                        not only query the coordinate, but also voxels around
                        the coordinate
  -t threshold, --threshold threshold
                        the threshold of fuzzy query, incorporate unlabeled
                        voxels from specific anatomical structures into data
                        queries, default value is 0
```