import PyInstaller.__main__
import os.path
PyInstaller.__main__.run([
    '--name=%s' % "rp_collector",
    '--onefile',
#    '--add-binary=%s' % './drivers/chromedriver.exe',
#    '--manifest=%s' % 'wrac_classes.exe.manifest',
#    '--icon=%s' % os.path.join('.', 'resources', 'favicon-1.ico'),
    'main.py'
])