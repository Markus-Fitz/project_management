# test manually in a python shell or a scratch file
from vault import read_file, write_file, update_frontmatter
from pathlib import Path

p = Path("test.md")

# create a test file
write_file(p, {"id": "test", "status": "todo"}, "hello world")

# read it back
meta, body = read_file(p)
print(meta)   # {"id": "test", "status": "todo"}
print(body)   # "hello world"

# update one field
update_frontmatter(p, {"status": "done"})
meta, body = read_file(p)
print(meta)   # {"id": "test", "status": "done", ...}