# Automated Tests

Currently I'm testing pyABF by running [runTests.py](runTests.py) which 
regenerates the content (readme.md and all graphics) of the following pages:

* [ABF data index](/data)
* [getting started guide](/docs/getting-started)

If a code change produces no change in the output text or figures (recognized
bit git), the code change was effectively invisible.