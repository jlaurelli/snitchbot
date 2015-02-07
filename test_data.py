#! BAD: Script syntax check
#!    

"""Do not collect this module docstring."""

# Basic line check

"Do not collect this string"

s = "Do not collect this variable initialization"

line = ["test line"]
for l in line:
    """Do not collect this docstring."""
    # For loop check
    # line = None

#### Multiple hash check

#No preceding whitespace check

#     Proceeding whitespace check

# \n Newline check

# \t Tab check
