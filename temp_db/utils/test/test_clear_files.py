from ..clear_old_files import get_files_to_clear
import datetime
import tempfile
import os

def test_clear_files():
    now = datetime.datetime.now()
    recent_time = now - datetime.timedelta(seconds=99)
    old_time = now - datetime.timedelta(seconds=101)
    with tempfile.TemporaryDirectory() as tmpdirname:
        with tempfile.NamedTemporaryFile(dir=tmpdirname) as new_file:
            with tempfile.NamedTemporaryFile(dir=tmpdirname) as old_file:
                os.utime(old_file.name, (old_time.timestamp(), old_time.timestamp()))
                os.utime(new_file.name, (recent_time.timestamp(), recent_time.timestamp()))
                files = get_files_to_clear(tmpdirname, 100)

                assert files == [old_file.name]
