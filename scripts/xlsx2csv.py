#!/usr/bin/python3 -O
# -*- coding: utf-8 -*-

"""
把 xlsx 格式的方言字音数据转换成 CSV 格式.
"""

__author__ = '黄艺华 <lernanto@foxmail.com>'


import argparse
import logging
import os
import pandas as pd


parser = argparse.ArgumentParser(__doc__)
parser.add_argument('indir', nargs='?', default='.', help='原始文件所在目录')
parser.add_argument('outdir', nargs='?', default='.', help='转化后文件保存目录')
args = parser.parse_args()

logging.getLogger().setLevel(logging.INFO)
logging.info(f'convert from xlsx to CSV: {args.indir} -> {args.outdir}')

os.makedirs(args.outdir, exist_ok=True)

for e in os.scandir(args.indir):
    if e.is_file():
        root, ext = os.path.splitext(e.name)
        if ext == '.xlsx':
            out_path = os.path.join(args.outdir, f'{root.partition(" ")[0]}.csv')
            logging.info(f'{e.path} -> {out_path}')

            data = pd.read_excel(e.path, dtype=str)

            # 少数文件列的命名和其他文件不一致，统一成最常用的
            data.rename(columns={
                'Order': '字號',
                'Char': '字',
                'ShengMu': '聲母',
                'YunMu': '韻母',
                'DiaoZhi': '調值',
                'DiaoLei': '調類',
                'Comment': '備註'
            }, inplace=True)

            # 多音字每个读音为一行，但有些多音字声韵调部分相同的，只有其中一行标了数据，
            # 其他行为空。对于这些空缺，使用同字第一个非空的的读音填充
            data.fillna(
                data.groupby('字號')[['聲母', '韻母', '調值', '調類']].transform('first'),
                inplace=True
            )
            data.to_csv(
                out_path,
                index=False,
                encoding='utf-8',
                lineterminator='\n'
            )