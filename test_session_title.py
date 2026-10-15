import json
import os
import tempfile

from session_title import latest_title


def test_latest_title_reads_incrementally():
    path = os.path.join(tempfile.mkdtemp(), "s.jsonl")
    title = lambda t: json.dumps({"type": "custom-title", "customTitle": t}) + "\n"
    state = {}
    with open(path, "w") as f:
        f.write('{"type":"user"}\n' + title("first"))
    assert latest_title(path, state) == "first"
    with open(path, "a") as f:
        f.write(title("second")[:10])  # half-written line is not read yet
    assert latest_title(path, state) == "first"
    with open(path, "a") as f:
        f.write(title("second")[10:] + '{"type":"assistant"}\n')
    assert latest_title(path, state) == "second"
    assert latest_title(path, state) == "second"  # nothing new, keeps the title


if __name__ == "__main__":
    test_latest_title_reads_incrementally()
    print("ok")
