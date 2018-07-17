import numpy as np
import functools
from operator import mul

from .namedFilter import namedFilter

class Pyramid:  # Pyramid base class

    def __init__(self, image, pyrType, edgeType):
        ''' - `edgeType` - specifies edge-handling.  Options are:
            * `'circular'` - circular convolution
            * `'reflect1'` - reflect about the edge pixels
            * `'reflect2'` - reflect, doubling the edge pixels
            * `'repeat'` - repeat the edge pixels
            * `'zero'` - assume values of zero outside image boundary
            * `'extend'` - reflect and invert
            * `'dont-compute'` - zero output when filter overhangs imput boundaries.
            '''
        self.image = np.array(image).astype(np.float)
        self.pyrType = pyrType
        self.edgeType = edgeType
        self.pyr = []
        self.pyrSize = []

    # methods
    def nbands(self):
        return len(self.pyr)

    def band(self, bandNum):
        assert bandNum < len(self.pyr), 'band number is out of range'
        return np.array(self.pyr[bandNum])

    # return concatenation of all levels of 1d pyramid / not used?
    def concatBands(self):
        outarray = np.array([]).reshape((1,0))
        for i in range(self.nbands()):
            tmp = self.band(i).T
            outarray = np.concatenate((outarray, tmp), axis=1)
        return outarray

    def setValue(self, band, location, value):
        """set a pyramid value
        location must be a tuple, others are single numbers
        """
        self.pyr[band][location[0],location[1]] = value

    def maxPyrHt(self, imsz, filtsz):
        ''' Compute maximum pyramid height for given image and filter sizes.
            Specifically: the number of corrDn operations that can be sequentially
            performed when subsampling by a factor of 2. '''
        # check if inputs are one of int, tuple and have consistent type
        assert (isinstance(imsz, int) and isinstance(filtsz, int)) or (
                isinstance(imsz, tuple) and isinstance(filtsz, tuple))
        # 1D image case: reduce to the integer case
        if isinstance(imsz, tuple) and (len(imsz) == 1 or 1 in imsz):
            imsz = functools.reduce(mul, imsz)
            filtsz = functools.reduce(mul, filtsz)
        # integer case
        if isinstance(imsz, int):
            if imsz < filtsz:
                return 0
            else:
                return 1 + self.maxPyrHt( imsz // 2, filtsz )
        # 2D image case
        if isinstance(imsz, tuple):
            if min(imsz) < max(filtsz):
                return 0
            else:
                return 1 + self.maxPyrHt( (imsz[0] // 2, imsz[1] // 2), filtsz )


# maxPyrHt
# showPyr