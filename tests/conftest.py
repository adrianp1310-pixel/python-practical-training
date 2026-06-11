import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture
def empty_html():
    return """
        <html>
        <body>
          None
        </body>
        </html>
        """