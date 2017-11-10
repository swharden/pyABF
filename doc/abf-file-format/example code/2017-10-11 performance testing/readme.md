**NOTES ABOUT EXAMPLE CODE:** This folder contains a standalone collection of code created from a snapshot of a work-in-progress project. It is meant for educational purposes only, and better code which does the same things may be found elsewhere
in this project.

## Notable Changes

---

# Faster data extraction with Numpy
The slowest part about working with ABFs is reading their signal data (tens to hundreds of MB) and scaling it. Data is stored as signed 16-bit integers and must be scaled by a scaling factor and provided to the end user as an array of floats. While there are many ways we could read data from ABFs, if one is not careful they will write code that runs slowly. This is an easy trap for young players.

## Python's integers are bigger than your ABF's

```python
fileBuffer = open("flename.abf", 'rb')
fileBuffer.seek(someBytePosition)
byteString = fileBuffer.read(numberOfPoints*2)
dataValues = struct.unpack("%dh"%(numberOfPoints), byteString)
fileBuffer.close()
```

This code works, but there's a problem. We use `struct.unpack()` and request to decode the bytestring in `h` format (16-bit signed integer) from the bytestring. Consider our signal is just 100 data points. A 16-bit (2-byte) format means 100 points occupies 200 bytes of memory. However, `dataValues` is a tuple of integers _in your Python platform's default integer size_. For me that's 64-bit integers. This means that one line of code quadrupled the size of data in memory from 200 bytes to 800 bytes. For this reason, it is a bad idea to store ABF signal data in Python's default integer size.

## Numpy's highly structured arrays support Int16

```python
fileBuffer = open("flename.abf", 'rb')
fileBuffer.seek(someBytePosition)
dataValues = numpy.fromfile(fileBuffer, dtype=np.int16, count=numberOfPoints)
fileBuffer.close()
```

This code is faster and four times smaller in memory. It also eliminates the need to _convert_ to a numpy array later for scaling. If numpy is available, use this method! using `sys.getsizeof(dataValues)` you will learn that the entire numpy object is about 100 bytes larger than the data itself.

## Scaling signal data (and floating point conversion)
As we saw earlier when we tried to plot the raw data (unsigned integers), values right out of the ABF are crazy-large numbers and need to be scaled down before they are meaningful. The scaling factor is a float, and the fastest way to do what we want is to let numpy handle the integer/float multiplication and return the result as a numpy float datatype. Be sure to set the dtype! If your system's default float is a 64-bit float, we quadrupled our memory requirement again.

```python
scaleFactor = lADCResolution / 1e6
scaledData=np.multiply(dataValues,scaleFactor,dtype='float32')
```

**Should we use 16-, 32-, or 64-bit floats for representing signals?** Although float16 _might_ be okay, it distorts the trace a wee little bit due to floating point errors counfounded by the division and multiplication operations. In my recording conditions (whole-cell patch-clamp in brain slices) I calculated that the average floating point error in 16-bit floats (compared to 64-bit precision) is only 0.0023 pA. This seems acceptable (and well below the RMS noise floor), but also consider that the _peak_ floating point error in these conditions is 0.329632 pA. Also future operations (like low-pass filtering and baseline subtraction) would aplify this error and introduce additional error. That's not acceptable to me so I'll double my memory usage and go with a 32-bit floating point precision. 0.3 pA seems like a lot of error to me, but I think it comes from _two_ floating point math operations: one for the scale factor (int16/float) and applying the scale factor (int16*float). With 32-bit floats our peak deviation (compared to 64-bit precision) is 0.0000160469 pA. If I reach a point where that is not enough precision, I will want to find a new job. For now I'm satisfied with float-32 because we know it's accurate and at 20kHz recording rate (40 kB raw data / sec) we produce 80 kB of scaled floating-point data per second (or 288 MB per hour of recording).


# Designing for Numpy as an option (not a requirement)
I want my ABFHeader class to be dependency-free. Buuuuuuut if numpy is around, let's use it. For all the reasons listed above, using numpy will massively improve performance. This is what I did to make Numpy optional:

### Optional import of Numpy

When importing the abf header module, try to import numpy. If it fails, that's fine!

```python
try:
    import numpy as np # use Numpy if we have it
except:
    np=False
```

### Optional use of Numpy

When sweeps are requested, use Numpy if we have it, and don't if we don't! Functionality is exactly the same if numpy is available or not. The difference is numpy is faster and will return a `ndarray` object if it's used. Otherwise you'll get a traditional python list. The values are the same!

```python
fb=open("someFile.abf",'rb')
fb.seek(firstBytePosition)
scaleFactor = self.header['lADCResolution'] / 1e6
if np:
	data = np.fromfile(fb, dtype=np.int16, count=pointCount)
	data = np.multiply(data,scaleFactor,dtype='float32')
else:
	print("WARNING: data is being retrieved without numpy (this is slow). See docs.")
	data = struct.unpack("%dh"%(pointCount), fb.read(pointCount*2)) # 64-bit int
	data = [point*scaleFactor for point in data] # 64-bit int * 64-bit floating point
fb.close()
```

# Performance Testing

## Numpy vs. Python: Sweep Hopping

I wrote a stress test that opens a 15 MB ABF file (about 6 minutes of data) and reads every sweep, and repeats this ten times. It then reports the total number of sweeps read, how long it took, and the average read time per sweep.

```
Without Numpy
read 1870 sweeps in 4.38152 sec (2.343 ms/sweep)
read 1870 sweeps in 4.37068 sec (2.337 ms/sweep)
read 1870 sweeps in 4.37608 sec (2.340 ms/sweep)
read 1870 sweeps in 4.37229 sec (2.338 ms/sweep)
read 1870 sweeps in 4.47250 sec (2.392 ms/sweep)
total 21.97307 sec

With Numpy
read 1870 sweeps in 0.34502 sec (0.185 ms/sweep)
read 1870 sweeps in 0.32036 sec (0.171 ms/sweep)
read 1870 sweeps in 0.31698 sec (0.170 ms/sweep)
read 1870 sweeps in 0.31709 sec (0.170 ms/sweep)
read 1870 sweeps in 0.32123 sec (0.172 ms/sweep)
total 1.62068 sec
```

**Conclusion:** Numpy is 13.56 times faster than pure python when loading sweeps

## Numpy vs. Python: Full File Reading

I was surprised to see performance goes in opposite directions when I load the full file in one block as compared to sweep by sweep. I think the weak point here is the `[x for x in y]` python code, and numpy shines. The performance _increase_ for numpy is probably the decrease in the need to `seek()` 1870 times.

```
without Numpy
read 1870 sweeps in 7.35235 sec (3.932 ms/sweep)
read 1870 sweeps in 7.30406 sec (3.906 ms/sweep)
read 1870 sweeps in 7.43636 sec (3.977 ms/sweep)
read 1870 sweeps in 7.32984 sec (3.920 ms/sweep)
read 1870 sweeps in 7.39116 sec (3.952 ms/sweep)
total 36.81377 sec

with Numpy
read 1870 sweeps in 0.23099 sec (0.124 ms/sweep)
read 1870 sweeps in 0.21806 sec (0.117 ms/sweep)
read 1870 sweeps in 0.21913 sec (0.117 ms/sweep)
read 1870 sweeps in 0.21845 sec (0.117 ms/sweep)
read 1870 sweeps in 0.21978 sec (0.118 ms/sweep)
total 1.10641 sec
```

**Conclusion:** Numpy is 33.27 times faster than pure python when loading a full file
























---


