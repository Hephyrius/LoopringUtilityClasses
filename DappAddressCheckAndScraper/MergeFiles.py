# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 17:52:30 2017

@author: Khera
"""

import pandas as pd

repo=pd.read_csv("data/tokens.txt",delimiter=",")
output=pd.read_csv("data/output",delimiter=",")
megalist=pd.read_csv("MegaListOfTokens.csv",delimiter=",")

frames = [repo, megalist]

result = pd.concat(frames)

r1 = result.drop_duplicates(subset='Address', keep="last")

