import PyInstaller.__main__
import os.path
PyInstaller.__main__.run([
    '--name=%s' % "rp_collector",
    '--distpath=%s' % "dist/rp_collector_v21.0.0",
    '--onefile',
#    '--add-binary=%s' % './drivers/chromedriver.exe',
#    '--manifest=%s' % 'wrac_classes.exe.manifest',
    '--icon=%s' % os.path.join('.', 'resources', 'race-horse.ico'),
    'main.py'
])
