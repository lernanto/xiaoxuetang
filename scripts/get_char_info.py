#!/usr/bin/python3 -O
# -*- coding: utf-8 -*-

"""
从 xlsx 格式的方言字音数据提取字信息.
"""

__author__ = '黄艺华 <lernanto@foxmail.com>'


import argparse
import logging
import os
import pandas as pd
from tqdm import tqdm


parser = argparse.ArgumentParser(__doc__)
parser.add_argument('indir', nargs='?', default='.', help='原始文件所在目录')
parser.add_argument('output', nargs='?', default='char.csv', help='输出文件路径')
args = parser.parse_args()

logging.getLogger().setLevel(logging.INFO)
logging.info(f'extracting character information from {args.indir} .')

outdir, _ = os.path.split(args.output)
if outdir != '':
    logging.debug(f'try creating directory {outdir}')
    os.makedirs(outdir, exist_ok=True)

data = []
for fname in tqdm(sorted(e.path for e in os.scandir(args.indir) \
    if e.is_file() and os.path.splitext(e.name)[1] == '.xlsx')):
    # 少数文件列的命名和其他文件不一致，统一成最常用的
    d = pd.read_excel(fname, dtype=str) \
        .rename(columns={'Order': '字號', 'Char': '字'})[['字號', '字']] \
        .drop_duplicates('字號')
    d['字號'] = d['字號'].astype(int)
    data.append(d)

data = pd.concat(data, axis=0, ignore_index=True) \
    .drop_duplicates('字號') \
    .sort_values('字號')
data.to_csv(args.output, index=False, encoding='utf-8', lineterminator='\n')

logging.info(f'{data.shape[0]} characters written to {args.output} .')
