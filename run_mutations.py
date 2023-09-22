from os import listdir, chdir, path, remove
import subprocess
import argparse
import shutil

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

    test_folder = 'test'
    if not path.exists('test'):
        test_folder = 'tests'
    test_files = listdir(test_folder)
    for test in test_files:
        if not test.endswith('.py') or test.startswith('__'):
            continue
        py_file = py_file.replace(".py", "")
        test = test.replace(".py", "")
        cmd = ["mut.py", "--target", f"{proj}.{py_file}", "--unit-test", f"test.{test}", "--debug"]
        print(" ".join(cmd))
        try:
            process = subprocess.run(cmd, check=True, capture_output=False)
            if path.isfile("/temp/mutations/mutations.pickle"): 
                shutil.move("/temp/mutations/mutations.pickle", f"/temp/mutations/mutations_{proj}_{py_file}_{test}.pickle")
                remove("/temp/mutations/mutations.pickle")
        except:
            continue
        
