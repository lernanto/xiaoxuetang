#!/usr/bin/python3 -O
# -*- coding: utf-8 -*-

"""
从小学堂的 HTML 表格中提取方言点信息.
"""

__author__ = '黄艺华 <lernanto@foxmail.com>'


import argparse
import logging
import os
import pandas as pd
import operator


parser = argparse.ArgumentParser(__doc__)
parser.add_argument('-o', '--output', default='dialect.csv', help='输出文件')
parser.add_argument('indir', nargs='?', default='.', help='输入文件目录')
args = parser.parse_args()

logging.getLogger().setLevel(logging.INFO)
logging.info(f'extract dialect information: {args.indir} -> {args.output}')

dialects = [
    '官話',
    '晉語',
    '吳語',
    '徽語',
    '贛語',
    '湘語',
    '閩語',
    '粵語',
    '平話',
    '客語',
    '其他土話'
]

# 提取方言信息
data = []
for d in dialects:
    fname = os.path.join(args.indir, 'html', f'{d}.html')
    logging.info(f'parsing {fname} ...')

    table = pd.read_html(fname, match='方言點', extract_links='body')[0]
    df = table.applymap(operator.itemgetter(0))
    df.insert(0, '方言', d)

    # 从超链接中提取方言点经纬度
    df[['緯度', '經度']] = table['方言點'].str[1] \
        .str.extract(r'http://maps\.google\.com/\?q=([0-9.]+)\s*,(?:\s|%20)*([0-9.]+)')

    data.append(df)

dialect_info = pd.concat(data, axis=0, ignore_index=True)

# 方言信息和方言文件名中的编号拼接
# 从方言文件名中提取编号、方言、方言点
name = pd.Series(os.listdir(os.path.join(args.indir, 'xlsx', 'modern_chinese')))
dialect_name = pd.DataFrame()
dialect_name[['編號', '方言', '方言點']] = name.str.extract(r'([0-9]+)\s+(.+)_(.+).xlsx')

# 一些方言命名不一致或有错别字，统一一下
dialect_name.loc[dialect_name['方言'].str.endswith('官話'), '方言'] = '官話'
dialect_name['方言'].replace('閔語', '閩語', inplace=True)

# 拼接方言信息和编号
dialect = pd.merge(dialect_info, dialect_name, how='outer', on=['方言', '方言點'])
dialect.to_csv(args.output, encoding='utf-8', index=False, lineterminator='\n')
