from os import listdir, chdir
import subprocess
import argparse


argparser = argparse.ArgumentParser()
argparser.add_argument("--proj-folder", type=str, default='')
arguments = argparser.parse_args()

chdir(arguments.proj_folder)

proj = arguments.proj_folder.split('/')[-1]
if proj == 'youtube-dl':
    proj = 'youtube_dl'
    
py_files = listdir(proj)

for py_file in py_files:
    if not py_file.endswith('.py') or py_file.startswith('__'):
        continue
    test_files = listdir('test')
    for test in test_files:
        if not test.endswith('.py') or test.startswith('__'):
            continue
        py_file = py_file.replace(".py", "")
        test = test.replace(".py", "")
        cmd = ["mut.py", "--target", f"{proj}.{py_file}", "--unit-test", f"test.{test}", "--debug", "--quiet"]
        try:
            process = subprocess.run(cmd, check=True, capture_output=False)

        except:
            continue
        
