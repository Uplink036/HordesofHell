import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import source.module as module


class TestModule:
    def test_sum_array():
        result = sum_array[1]
        assert result is not None
        assert result == 1
