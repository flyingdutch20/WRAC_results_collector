import PyInstaller.__main__
import os.path
PyInstaller.__main__.run([
    '--name=%s' % "WRAC_results_collector",
    '--distpath=%s' % "dist/WRAC_results_collector_v21.0.0",
    '--onefile',
#    '--add-binary=%s' % './drivers/chromedriver.exe',
#    '--manifest=%s' % 'wrac_classes.exe.manifest',
    '--icon=%s' % os.path.join('.', 'resources', 'favicon.ico'),
    'main.py'
])
