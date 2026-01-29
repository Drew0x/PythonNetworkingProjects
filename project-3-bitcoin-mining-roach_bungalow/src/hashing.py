'''
CS 3700 - Networking & Distributed Computing - Fall 2025
Instructor: Thyago Mota
Student: Andrew Stephens, Oliver Yang
Description: Project 3 - Hashing Demonstration
'''

import hashlib

class HashMain:
    def hash(self, data: str) -> str:
        """Compute a fresh MD5 hash for the given string."""
        h = hashlib.md5()
        h.update(data.encode('utf-8'))
        return h.hexdigest()

if __name__ == "__main__":
    hash_main = HashMain()
    examples = ["Computer Science", "Computer SciencE", "Bitcoin"]
    for example in examples:
        print(f'Hash value of "{example}" is "{hash_main.hash(example)}"')