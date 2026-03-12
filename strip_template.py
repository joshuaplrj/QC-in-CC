import re
import os

filepath = r"c:\Users\John Jacob\Desktop\Desktop\QC in CC\QB in CC\quantum_systems\generate_remaining.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# We want to remove everything from '    def execute_classical(self):' to just before '    def verify_results(self) -> bool:'
pattern = re.compile(r'    def execute_classical\(self\):.*?    def verify_results\(self\) -> bool:', re.DOTALL)

new_content = pattern.sub('    def verify_results(self) -> bool:', content)

if new_content != content:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully removed dummy execution and visualization overrides.")
else:
    print("Pattern not found!")
