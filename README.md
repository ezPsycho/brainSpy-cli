# brainSpy-cli

Transform MNI coordinate to AAL and BA structural names.

**Please notice the program is too beta to be used for production purpose, code review and further checks are necessary.**

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

## Tutorial

### Installing

#### Windows

Checkout this page: https://github.com/ezPsycho/brainSpy-cli/releases/tag/0.0.1

#### Linux

WIP.

### Using

#### Precise query

query brain structure **of** specific MNI coordinate, or its nearest structure.

![Screen record of precise query](https://github.com/ezPsycho/brainSpy-cli/blob/master/docs/assets/precise_query.gif?raw=true)

#### Fuzzy query

query brain structure **around** specifc MNI coordinate, or its nearset structure.

![Screen record of fuzzy query](https://github.com/ezPsycho/brainSpy-cli/blob/master/docs/assets/fuzzy_query.gif?raw=true)
