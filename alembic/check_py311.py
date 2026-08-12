import glob, re

for f in sorted(glob.glob("alembic/versions/*.py")):
    src = open(f, encoding="utf-8").read()
    lines = src.splitlines()
    in_fstring = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if "op.execute(f" in stripped and ('"""' in stripped or "'''" in stripped):
            in_fstring = True
        if in_fstring:
            # backslash in a string literal inside f-string expression
            if re.search(r"['\"].*\\n.*['\"]", line):
                print(f"{f}:{i}: {stripped[:100]}")
        if in_fstring and stripped in ('""")','""")', "''')"):
            in_fstring = False
