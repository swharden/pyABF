
using System;
using System.IO;

namespace Builder
{
    public static class Program
    {
        static void Main(string[] args)
        {
            string thisFile = System.Reflection.Assembly.GetExecutingAssembly().Location;
            string repoRoot = Path.GetFullPath(Path.Combine(thisFile, "../../../../../../"));
            string contentFolder = Path.Combine(repoRoot, "website/content/");
            string themeFolder = Path.Combine(repoRoot, "website/theme/");
            string sourceUrl = "https://github.com/swharden/pyABF/tree/master/website/content/";
            string rootUrl = (args.Length == 1) ? args[0] : "http://localhost:8080/pyabf/";

            Console.WriteLine($"Creating website with root URL: {rootUrl}");
            var gen = new Statix.Generator(contentFolder, themeFolder, rootUrl, sourceUrl);
            gen.HeaderRequirements.RequireDate = false;
            gen.Generate();
        }
    }
}