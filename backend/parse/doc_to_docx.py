import subprocess
import sys
import os

if os.name == "nt":

       if len(sys.argv) < 2:
              sys.stderr.write("SYNOPSIS: %s file1 [file2] ...\n"%sys.argv[0])

       for doc in sys.argv[1:]:
              subprocess.call(['C:/Program Files/LibreOffice/program/soffice.exe', '--headless', '--convert-to', 'docx', '--outdir', './data/docx', doc])

elif os.name == "":

       if len(sys.argv) < 2:
              sys.stderr.write("SYNOPSIS: %s file1 [file2] ...\n"%sys.argv[0])

       for doc in sys.argv[1:]:
              subprocess.call(['soffice', '--headless', '--convert-to', 'docx', '--outdir', './data/docx', doc])