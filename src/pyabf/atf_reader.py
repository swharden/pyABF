import re
import pprint
import numpy as np
import os.path

# File format description taken from
# https://mdc.custhelp.com/app/answers/detail/a_id/18883/~/genepix%C2%AE-file-formats
#
# An ATF text file consists of records. Each line in the text file is a record.
# Each record may consist of several fields, separated by a field separator
# (column delimiter). The tab and comma characters are field separators. Space
# characters around a tab or comma are ignored and considered part of the field
# separator. Text strings are enclosed in quotation marks to ensure that any
# embedded spaces, commas and tabs are not mistaken for field separators.
#
# The group of records at the beginning of the file is called the file header.
# The file header describes the file structure and includes column titles,
# units, and comments.
#
# ATF File Structure
#  First header record 	 Format: ATF (all caps), Version number
#  Second header record 	 Number of optional header records n,
#   	 Number of data columns (fields) m
#  1st optional record 	 ...
#  2nd optional record 	 ...
#  nth optional record
#  (n+3)th record 	 Required record containing m fields.
#   	 Each field contains a column title
#  DATA RECORDS 	 Arranged in m columns (fields) of data


class ATFReader():
    """
    ATFReader allows to parse ATF files from Axon.
    """

    def __init__(self, file_path):
        """
        Read the file in file_path and parse it as ATF.
        """

        if not os.path.isfile(file_path):
            raise ValueError(f"The file path {file_path} does not refer to an existing file.")

        with open(file_path, 'r') as fh:
            signature, file_version = fh.readline().rstrip().split()

            if signature != 'ATF':
                raise ValueError(f"Unexpected file signature {signature}")

            self._file_path = file_path
            self._file_version = file_version

            elems = fh.readline().rstrip().split()

            num_optional_records = int(elems[0])
            assert num_optional_records >= 0, "Invalid number of optional records"

            num_data_columns = int(elems[1])

            self._num_sweeps = num_data_columns - 1
            assert self.num_sweeps >= 1, "Expected at least one sweep"

            self._header = {}

            for _ in range(num_optional_records):
                _, key, value, _ = re.split(r'^"([^=]+)=(.*)"$', fh.readline().rstrip())

                if key == "SignalsExported":
                    self._header[key] = value.split(",")
                elif key == "Signals":
                    self._header[key] = re.split(r'"\t+"', value)[1:]
                else:
                    self._header[key] = value

            def unquote(x):
                if x[0] == '"' and x[-1] == '"':
                    return x[1:-1]
                else:
                    return x

            # column names with quotes removed
            self._column_names = [unquote(x) for x in re.split(r"\t+", fh.readline().rstrip())]

            data = np.genfromtxt(file_path, dtype=np.float64,
                                 skip_header=3 + num_optional_records,
                                 invalid_raise=True,
                                 usecols=range(0, num_data_columns))

            self._raw_data = data[:, 1:]
            self._time = data[:, 0]

            self._sampling_interval = np.mean(np.diff(self._time))
            assert self._sampling_interval >= 0, "Invalid sampling interval"

            self._num_points = len(self._time)
            assert self._num_points >= 1, "Expected at least one point"

        return

    def __str__(self):
        return ("File {file_path} using ATF version {file_version} has {num_sweeps} Sweeps, "
                "each with {num_points} points and a sampling interval of "
                "{sampling_interval:.6g}s\n"
                "Column names: {column_names}\n"
                "Optional header entries: {header}"
                ).format(file_path=self._file_path, file_version=self._file_version,
                         num_sweeps=self._num_sweeps, num_points=self._num_points,
                         sampling_interval=self._sampling_interval,
                         column_names=pprint.pformat(self._column_names),
                         header=pprint.pformat(self._header))

    @property
    def file_version(self):
        """Return the file version"""
        return self._file_version

    @property
    def file_path(self):
        """Return the file path"""
        return self._file_path

    @property
    def num_sweeps(self):
        """Return the number of sweeps"""
        return self._num_sweeps

    @property
    def num_points(self):
        """Return the number of sampling points"""
        return self._num_points

    @property
    def header(self):
        """Return a dictionary of all header entries"""
        return self._header

    @property
    def sampling_interval(self):
        """Return the sampling interval in seconds"""
        return self._sampling_interval

    @property
    def time(self):
        """Return the array with signal times in ms"""
        return self._time

    @property
    def signal(self):
        """Return the array with signal data, one column per sweep/repetition"""
        return self._raw_data
