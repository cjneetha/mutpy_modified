from os import listdir, chdir, path, remove
import subprocess
import argparse
import shutil

argparser = argparse.ArgumentParser()
argparser.add_argument("--proj-folder", type=str, default='')
argparser.add_argument("--test-framework", type=str, default='')

arguments = argparser.parse_args()

chdir(arguments.proj_folder)
test_framework = arguments.test_framework

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
        if not path.exists(test_folder):
            test_folder = path.join(proj,'test')
            if not path.exists(test_folder):
                test_folder = path.join(proj,'tests')
                if not path.exists(test_folder):
                    print('test folder not found')
            
    test_folder = test_folder.replace('/', '.')
    print(test_folder)
    
    test_files = listdir(test_folder)
    for test in test_files:
        if not test.endswith('.py') or test.startswith('__'):
            continue
        py_file = py_file.replace(".py", "")
        test = test.replace(".py", "")
        cmd = ["mut.py", "--target", f"{proj}.{py_file}", "--unit-test", f"{test_folder}.{test}", "--debug", "--runner", test_framework]
        print(" ".join(cmd))
        try:
            process = subprocess.run(cmd, check=True, capture_output=False)
            if path.isfile("/temp/mutations/mutations.pickle"): 
                shutil.move("/temp/mutations/mutations.pickle", f"/temp/mutations/mutations_{proj}_{py_file}_{test}.pickle")
                remove("/temp/mutations/mutations.pickle")
        except:
            continue
        
