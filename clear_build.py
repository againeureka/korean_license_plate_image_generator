import os
import shutil
import glob

def remove_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"🧹 Removed directory: {path}")
    elif os.path.isfile(path):
        os.remove(path)
        print(f"🧹 Removed file: {path}")

def clean():
    remove_path('build')
    remove_path('dist')
    remove_path('outputs')
    
    # *.egg-info 폴더 제거
    for egg_info in glob.glob('*.egg-info'):
        remove_path(egg_info)

    # __pycache__ 모든 하위 폴더에서 제거
    for root, dirs, files in os.walk('.'):
        for d in dirs:
            if d == '__pycache__':
                remove_path(os.path.join(root, d))

if __name__ == "__main__":
    clean()
