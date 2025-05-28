import PyInstaller.__main__
import os

def build_exe():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--windowed',
        '--name=SmartMart',
        '--add-data=data;data',
        '--icon=assets/icon.ico',
        '--clean',
        '--distpath=dist',
        '--workpath=build'
    ])

if __name__ == "__main__":
    build_exe() 