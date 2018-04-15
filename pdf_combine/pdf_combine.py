from PyPDF2 import PdfFileMerger
import natsort
import os

DIR = os.getcwd() # dir is current working directory
OUTPUT = "output.pdf"

file_list = filter(lambda f: f.endswith('.pdf'), os.listdir(DIR))
file_list = natsort.natsorted(file_list)

merger = PdfFileMerger(strict=False)

for f_name in file_list:
  f = open(os.path.join(DIR, f_name), "rb")
  merger.append(f)

output = open(OUTPUT, "wb")
merger.write(output)
