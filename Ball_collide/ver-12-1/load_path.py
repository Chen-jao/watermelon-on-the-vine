#!/usr/bin/env python
#-*- coding: utf-8 -*-

from stdafx import os

#路径获取统一格式
def load_path(root, name):
    root_path = os.path.join(root, name)
    if not root_path:
        print 'not find.'
    return root_path
