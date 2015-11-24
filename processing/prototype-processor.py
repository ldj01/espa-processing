
#This code is just a concept implementation to see if it is worthwhile to pursue

import os
import sys
from argparse import ArgumentParser


class process_app(object):

    def __init__(self):
        super(process_app, self).__init__()

        self.execute_app = False

    def configure(self, options):
        pass

    def execute(self):
        pass


class ls_app(process_app):

    def __init__(self):
        super(ls_app, self).__init__()

    def configure(self, options):
        if options['include_ls']:
            self.execute_app = True

    def execute(self):
        if self.execute_app:
            print 'executing --- ls_app'


class ps_app(process_app):

    def __init__(self):
        super(ps_app, self).__init__()

    def configure(self, options):
        if options['include_ps']:
            self.execute_app = True

    def execute(self):
        if self.execute_app:
            print 'executing --- ps_app'


class hh_app(process_app):

    def __init__(self):
        super(hh_app, self).__init__()

    def configure(self, options):
        if options['include_hh']:
            self.execute_app = True

    def execute(self):
        if self.execute_app:
            print 'executing --- hh_app'


class cleanup(process_app):

    def __init__(self):
        super(cleanup, self).__init__()

    def configure(self, options):
        if options['keep_intermediate_data']:
            self.execute_app = True

    def execute(self):
        if self.execute_app:
            print 'executing --- cleanup'


class warping(process_app):

    def __init__(self):
        super(warping, self).__init__()

    def configure(self, options):
        if options['include_warp']:
            self.execute_app = True

    def execute(self):
        if self.execute_app:
            print 'executing --- warping'


class convert(process_app):

    def __init__(self):
        super(convert, self).__init__()

    def configure(self, options):
        if options['include_convert']:
            self.execute_app = True

    def execute(self):
        if self.execute_app:
            print 'executing --- convert'


if __name__ == '__main__':
    options = {
        'include_ls': True,
        'include_ps': False,
        'include_hh': True,
        'keep_intermediate_data': True,
        'include_warp': True,
        'include_convert': True
    }

    print options

    # TODO TODO TODO - instead of hardcoding a list here, maybe call some method that just returns the things to execute already configured
    apps = [ls_app(),
            ps_app(),
            hh_app(),
            cleanup(),
            warping(),
            convert()
           ]

    for app in apps:
        app.configure(options)
        app.execute()
