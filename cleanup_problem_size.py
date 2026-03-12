import os
import glob
import re

base_path = r"c:\Users\John Jacob\Desktop\Desktop\QC in CC\QB in CC\quantum_systems"

for filepath in glob.glob(os.path.join(base_path, "**", "*.py"), recursive=True):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # Remove self.problem_size = ...
    content = re.sub(r'^[ \t]*self\.problem_size\s*=\s*\d+.*\n', '', content, flags=re.MULTILINE)
    
    # Replace label Size: with Qubits (n):
    content = content.replace('text="Size:"', 'text="Qubits (n):"')
    
    # Replace size = self.size_var.get()... with n = ...
    content = content.replace("size = self.size_var.get() if hasattr(self, 'size_var') else 20", 
                              "n = self.size_var.get() if hasattr(self, 'size_var') else self.n_qubits")
    
    # Replace "size": size with "n": n
    content = content.replace('"size": size', '"n": n')
    
    # Replace np.random.randn(size) with np.random.randn(n)
    content = content.replace('np.random.randn(size)', 'np.random.randn(n)')
    
    # Replace Size: {result['size']} with Qubits (n): {result['n']}
    content = content.replace("Size: {result['size']}", "Qubits (n): {result['n']}")
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")
