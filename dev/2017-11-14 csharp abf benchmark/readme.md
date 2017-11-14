# ABF Reading Benchmark Tool in C#

### Usage
```bash
ABFbenchmark.exe "C:\path\to\file.abf"
```

### Example Output
_note: these values were captured from the debug version, not the release version. They are slightly slower._
```
Reading Header ...
 byte location of data: 5632
 data point byte size : 2
 number of data points: 7480000
 data scale factor: 0.032768

Test file open/read/close speed (10000 repetitions) ...
 file signature: ABF2
 completed in 504.724 ms (50.472 us each)

Test loading all ABF data (100 repetitions)
 read 7480000 data points
 completed in 648.929 ms (6.489 ms each)

Test loading all ABF data (100 repetitions)
 read 7480000 data points
 scaling was applied: 0.032768
 completed in 3,190.290 ms (31.903 ms each)

Test loading all ABF data (100 repetitions)
 read 7480000 data points
 scaling was applied: 0.032768
 average was calculated: 7.806527
 completed in 6,813.350 ms (68.134 ms each)
```

### Process Time Comparisons

Test|Python|C# (Scott's home)|C# (Scott's work)|C# (Network drive)
---|---|---|---|---
open/close|35.130 us|49.840 us|1,025.697 us|339.553 us
raw read|7.154 ms|6.403 ms|4.719 ms|5.968 ms
with scaling|20.040 ms|21.376 ms|15.900 ms|15.992 ms
with averaging|25.169 ms|58.260 ms|46.866 ms|46.927 ms

**Why is compiled C# slower than Python?** Because the differences are in floating point math, I wonder if it is because precision is increased in C# somehow (i.e,. the multiplication between the scaling factor and the float array has more precision and takes more CPU cycles)... not sure though.

### Source Code
```C#

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Diagnostics;

namespace ABFbenchmark
{
    class Program
    {
        public static string abfFileName;

        static int Main(string[] args)
        {

            // if no argument is given, use this path as a default
            Program.abfFileName = @"C:\Users\scott\Documents\GitHub\pyABF\data\16d05007_vc_tags.abf";

            if (args.Length == 1)
            {
                System.Console.WriteLine("Analyzing {0}", args[0]);
                Program.abfFileName = args[0];
            }
            else 
            {
                System.Console.WriteLine("Must supply an ABF filename as an argument.");
                System.Console.WriteLine("  trying: {0}", Program.abfFileName);
            }

            // read the header to get all the data we are interested in
            System.Console.WriteLine("\nReading Header ...");
            ReadHeaderValues();
            System.Console.WriteLine(" byte location of data: {0}", Program.dataFirstByte);
            System.Console.WriteLine(" data point byte size : {0}", Program.dataPointByteSize);
            System.Console.WriteLine(" number of data points: {0}", Program.dataPointCount);
            System.Console.WriteLine(" data scale factor: {0}", Program.dataScaleFactor);

            // run the benchmark tests
            FileOpenClose();
            LoadData(100); // just load raw data
            LoadData(100, true); // with scaling
            LoadData(100, true, true); // with averaging

            // exit gracefully
            System.Console.WriteLine("\npress ENTER to exit...");
            System.Console.ReadLine();
            return 0;
        }

        /// <summary>
        /// Time how long it takes to open the file, read the first 4 bytes, then close it.
        /// </summary>
        public static void FileOpenClose(int repetitions=10000)
        {
            System.Console.WriteLine("\nTest file open/read/close speed ({0} repetitions) ...", repetitions);

            Stopwatch t1 = new Stopwatch();
            char[] fileSignature = new char[4];

            t1.Start();
            for (int i=0; i<repetitions; i++)
            {
                BinaryReader fb = new BinaryReader(File.Open(Program.abfFileName, FileMode.Open));
                fileSignature = fb.ReadChars(4);
                fb.Close();
            }
            t1.Stop();
            double timeTotal = (double)t1.ElapsedTicks / (double)System.Diagnostics.Stopwatch.Frequency;
            double timeEach = timeTotal / repetitions;

            System.Console.WriteLine(" file signature: {0}", new string(fileSignature));
            System.Console.WriteLine(" completed in {0:N3} ms ({1:N3} us each)", timeTotal * 1e3, timeEach * 1e6);
        }

        public static void LoadData(int repetitions = 100, bool scale=false, bool average=false)
        {
            System.Console.WriteLine("\nTest loading all ABF data ({0} repetitions)", repetitions);

            Stopwatch t1 = new Stopwatch();
            BinaryReader fb = new BinaryReader(File.Open(Program.abfFileName, FileMode.Open));

            int dataByteCount = (int)(Program.dataPointCount * Program.dataPointByteSize);

            byte[] dataBytes = new byte[dataByteCount];
            short[] dataRaw = new short[Program.dataPointCount];
            float[] dataScaled = new float[Program.dataPointCount];
            float averagePointValue=0;

            t1.Start();
            for (int repetitionNumber = 0; repetitionNumber < repetitions; repetitionNumber++)
            {
                fb.BaseStream.Seek(Program.dataFirstByte, SeekOrigin.Begin);
                fb.BaseStream.Read(dataBytes, 0, dataByteCount);
                Buffer.BlockCopy(dataBytes, 0, dataRaw, 0, dataByteCount);
                if (scale)
                {
                    for (long i = 0; i < Program.dataPointCount; i++)
                    {
                        dataScaled[i] = dataRaw[i] * Program.dataScaleFactor;
                    }
                }
                if (average)
                {
                    averagePointValue = dataScaled.Average();
                }
            }
            t1.Stop();
            fb.Close();
            double timeTotal = (double)t1.ElapsedTicks / (double)System.Diagnostics.Stopwatch.Frequency;
            double timeEach = timeTotal / repetitions;

            System.Console.WriteLine(" read {0} data points", Program.dataPointCount);
            if (scale)
            {
                System.Console.WriteLine(" scaling was applied: {0}", Program.dataScaleFactor);
            }
            if (average)
            {
                System.Console.WriteLine(" average was calculated: {0}", averagePointValue);
            }
            System.Console.WriteLine(" completed in {0:N3} ms ({1:N3} ms each)", timeTotal * 1e3, timeEach * 1e3);
        }

        public static long dataPointCount;
        public static long dataPointByteSize;
        public static long dataFirstByte;
        public static float dataScaleFactor;
        public static void ReadHeaderValues()
        {
            BinaryReader fb = new BinaryReader(File.Open(Program.abfFileName, FileMode.Open));
            if (new string(fb.ReadChars(4)) != "ABF2")
                throw new System.ArgumentException("The file is not a valid ABF2 file.");
            int BLOCKSIZE = 512; // blocks are a fixed size in ABF1 and ABF2 files
            fb.BaseStream.Seek(12, SeekOrigin.Begin); // this byte stores the number of sweeps
            long sweepCount = fb.ReadUInt32();
            fb.BaseStream.Seek(76, SeekOrigin.Begin); // this byte stores the ProtocolSection block number
            long posProtocolSection = fb.ReadUInt32() * BLOCKSIZE;
            long poslADCResolution = posProtocolSection + 118; // figure out where lADCResolution lives
            fb.BaseStream.Seek(poslADCResolution, SeekOrigin.Begin); // then go there
            long lADCResolution = fb.ReadInt32();
            Program.dataScaleFactor = lADCResolution / (float)1e6;
            fb.BaseStream.Seek(236, SeekOrigin.Begin); // this byte stores the DataSection block number
            Program.dataFirstByte = fb.ReadUInt32() * BLOCKSIZE;
            Program.dataPointByteSize = fb.ReadUInt32(); // this will always be 2 for a 16-bit DAC
            Program.dataPointCount = fb.ReadInt64();
            fb.Close(); // close and unlock the file ASAP
        }
    }
}

```