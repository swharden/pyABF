using System;
using System.Linq;
using System.IO;
using System.Collections.Generic;

namespace firstValues
{
    class Program
    {
        static void Main(string[] args)
        {
            string thisFolder = Path.GetDirectoryName(System.Reflection.Assembly.GetAssembly(typeof(Program)).Location);
            Console.WriteLine(thisFolder);
            string abfFolder = Path.GetFullPath(thisFolder + "/../../../../../data/abfs");
            string[] abfPaths = Directory.GetFiles(abfFolder, "*.*").Where(x => x.EndsWith(".abf")).ToArray();
            foreach (string abfPath in abfPaths)
            {
                var abf = new AbfSharp.ABFFIO.ABF(abfPath);
                double[] firstValues = new double[abf.Header.nADCNumChannels];
                for (int i = 0; i < abf.Header.nADCNumChannels; i++)
                {
                    double[] sweep = abf.GetSweep(sweepIndex: 0, channelIndex: i);
                    firstValues[i] = sweep[0];
                }
                string values = string.Join(", ", firstValues.Select(x=>$"{x:0.00000}"));
                string abfid = Path.GetFileNameWithoutExtension(abfPath);
                string line = $"FIRSTVALUES['{abfid}'] = [{values}]";
                Console.WriteLine(line);
            }
        }
    }
}
