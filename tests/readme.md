# Automated Testing

Execution of [runTests.py](runTests.py) does a lot of things, including deleting and re-generating all [demo ABF header pages and thumbnails](/data/) and fully re-generating the [getting started guide](/docs/getting-started). If a core code change produces no change in the output text or figures (recognized by git), the code change was effectively invisible.

Execution of [runTests.py](runTests.py) is recommended before issuing releases.
