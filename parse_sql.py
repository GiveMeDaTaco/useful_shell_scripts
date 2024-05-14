import re

def is_valid_join_condition(condition):
    # Define the regular expression pattern for a complex JOIN condition
    pattern = re.compile(r'''
        ^\s*                                # Optional leading whitespace
        (                                   # Start of the first condition
            [a-zA-Z_]+\.[a-zA-Z_]+          # Column reference (e.g., a.some_column)
            \s*=\s*                         # Equal sign with optional whitespace
            ([a-zA-Z_]+\.[a-zA-Z_]+|'.*'|\d+)  # Column reference or a quoted string or a number
        )                                   # End of the first condition
        (\s*(AND|OR)\s*                     # Logical operator with optional whitespace
        (                                   # Start of the second condition
            [a-zA-Z_]+\.[a-zA-Z_]+          # Column reference (e.g., b.other_column)
            \s*=\s*                         # Equal sign with optional whitespace
            ([a-zA-Z_]+\.[a-zA-Z_]+|'.*'|\d+)  # Column reference or a quoted string or a number
        ))*                                 # End of the second condition, which can be repeated
        \s*$                                # Optional trailing whitespace
    ''', re.VERBOSE)
    
    # Use re.match to check if the condition matches the pattern
    if re.match(pattern, condition):
        return True
    else:
        return False

# Test the function
test_conditions = [
    "a.some_column = b.some_column AND b.other_column = 'Y'",
    "a.some_column = b.some_column",
    "(a.some_column = b.some_column OR b.other_column = 'Y') AND b.third_column = 'N'",
    "a.some_column = b.some_column OR b.other_column = 'Y'",
    "a.some_column = b.some_column AND (b.other_column = 'Y' OR b.third_column = 'N')",
    "a.some_column = b.some_column && b.other_column = 'Y'",
    "a.some_column = b.some_column AND b.other_column = 'Y' AND b.third_column = 1"
]

for condition in test_conditions:
    print(f"'{condition}' is valid: {is_valid_join_condition(condition)}")
