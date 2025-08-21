import ijson
from tqdm import tqdm
import os
import sys

if len(sys.argv) < 2:
    print("Usage: VIC2TXT.py VIC_US_****_**_FS.json")
    sys.exit(1)

filename = sys.argv[1]
open_files_md5 = {}
open_files_pdna = {}

written_header_md5 = set()
written_header_pdna = set()

def get_file_md5(cat):
    fname = f'MD5-Category-{cat}.txt'
    if cat not in open_files_md5:
        is_new = not os.path.exists(fname)
        f = open(fname, 'a')
        if is_new:
            f.write('MD5\n')
            written_header_md5.add(cat)
        open_files_md5[cat] = f
    return open_files_md5[cat]

def get_file_pdna(cat):
    fname = f'PhotoDNA-Category-{cat}.txt'
    if cat not in open_files_pdna:
        is_new = not os.path.exists(fname)
        f = open(fname, 'a')
        if is_new:
            f.write('PhotoDNA\n')
            written_header_pdna.add(cat)
        open_files_pdna[cat] = f
    return open_files_pdna[cat]

with open(filename, 'r', encoding='utf-8') as f:
    items = ijson.items(f, 'value.item')
    for entry in tqdm(items, desc='Processing records'):
        cat = entry.get('Category')
        md5 = entry.get('MD5')
        pdna = entry.get('PhotoDNA')
        if md5:
            file_md5 = get_file_md5(cat)
            file_md5.write(md5 + '\n')
        if pdna:
            file_pdna = get_file_pdna(cat)
            file_pdna.write(pdna + '\n')

for f in open_files_md5.values():
    f.close()
for f in open_files_pdna.values():
    f.close()

print('I’m done. Now, it’s time for action!')
