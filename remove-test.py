import os

curr_dir = os.getcwd()
cache_dir = curr_dir + "/__pycache__"

for file in os.listdir(cache_dir):
    os.remove(os.path.join(cache_dir, file))

os.rmdir(cache_dir)
