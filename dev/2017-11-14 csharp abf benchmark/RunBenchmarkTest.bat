@ echo off
cd "ABFbenchmark\bin\Release"
echo 
echo DATA ON LOCAL DRIVE
ABFbenchmark.exe "C:\Users\swharden\Documents\GitHub\pyABF\data\16d05007_vc_tags.abf"

echo
echo DATA ON NETWORK DRIVE
ABFbenchmark.exe "X:\Software\Data\16d05007_vc_tags.abf"
