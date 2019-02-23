#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Author: Micah Price (98mprice@gmail.com)
    Helper and wrapper functions.
"""

import re
import pandas as pd

def read_data(filename, x_colname, y_colname):
    """
    Reads data from filename and extracts features from x_colname and
    target classes from y_colname.

    Args:
        filename: String of dataset path (in csv format).
        x_colname: Column name of features.
        y_colname: Column name of targets.

    Returns:
        List of feature text, list of target text.
    """
    data = pd.read_csv(filename)

    import re
    pattern = re.compile("^[a-z]+$")

    # strips words containing non-alphabetic characters
    # from each string
    valid_x = list(map(lambda sentence: ' '.join(list(
        filter(lambda word: pattern.match(word),
        sentence.split(' ')))), data[x_colname].values))

    return valid_x, data[y_colname].values
