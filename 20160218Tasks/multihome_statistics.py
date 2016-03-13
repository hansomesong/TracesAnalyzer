# -*- coding: utf-8 -*-
__author__ = 'yueli'

from config.config import *

if __name__ == '__main__':

    for vp in VP_LIST:
        # input file
        result_txt_file = os.path.join(CSV_FILE_DESTDIR, 'loc2AS_dynamic_{0}.txt'.format(vp))
        print result_txt_file
        with open(result_txt_file) as f_handler:
            file_str = f_handler.read()

            pass

