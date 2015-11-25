
# This code is just a concept implementation to see if it is worthwhile to
# pursue

import os
import sys
from argparse import ArgumentParser


class process_app(object):

    def __init__(self):
        super(process_app, self).__init__()

        self.execute_app = False

    def configure(self, options):
        raise NotImplementedError('Not Implemented')

    def execute(self):
        raise NotImplementedError('Not Implemented')


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


def initialize(options):
    # TODO - The smarts to decide what processing steps are required and
    #        a list of them is returned
    # TODO - Return them already configured

    # TODO - This is not the smarts required
    processing_steps = list()
    processing_steps.append(ls_app())
    processing_steps.append(ps_app())
    processing_steps.append(hh_app())
    processing_steps.append(cleanup())
    processing_steps.append(warping())
    processing_steps.append(convert())

    return processing_steps


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

    processing_steps = initialize(options)

    for p_step in processing_steps:
        p_step.configure(options)
        p_step.execute()
