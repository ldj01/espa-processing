
# This code is just a concept implementation to see if it is worthwhile to
# pursue

import os
import sys
from argparse import ArgumentParser


# NOTE - TODO - I am not following proper class names in this example
class process_app(object):

    def __init__(self):
        super(process_app, self).__init__()
        self._execution_required = False

    def configure(self, options):
        # The idea for this would be to make the determination if the specific
        # application needs to be executed, regardless if it was requested or
        # not because it may be required input for another app.
        # This method would also configure any internal properties required
        # to accomplish executing the application.

        # NOTE - TODO - Since order of applications is required outside of
        #               this method, maybe this method, only needs to do
        #               configuration.  And the execution_required property
        #               and concept goes away.
        raise NotImplementedError('Not Implemented')

    # TODO - Maybe try the proerty setter getter stuff from the mistakes book
    #        for some of the items
    @property
    def execution_required(self):
        return self._execution_required

    @execution_required.setter
    def execution_required(self, value):
        self._execution_required = bool(value)

    @execution_required.deleter
    def execution_required(self):
        del self._execution_required

    def execute(self):
        # This idea for this is as expected.  Execute the specific application.
        # Or in some cases, such as cleanup, it could be the implementation.
        raise NotImplementedError('Not Implemented')


class ls_app(process_app):

    def __init__(self):
        super(ls_app, self).__init__()

    def configure(self, options):
        if options['include_ls']:
            # TODO - Maybe we don't need to set this property, and could just
            #        return True or False, to make the decision wether or not
            #        to add it to the processing list.
            self.execution_required = True

    def execute(self):
        print 'executing --- ls_app'


class ps_app(process_app):

    def __init__(self):
        super(ps_app, self).__init__()

    def configure(self, options):
        if options['include_ps']:
            self.execution_required = True

    def execute(self):
        print 'executing --- ps_app'


class hh_app(process_app):

    def __init__(self):
        super(hh_app, self).__init__()

    def configure(self, options):
        if options['include_hh']:
            self.execution_required = True

    def execute(self):
        print 'executing --- hh_app'


class cleanup(process_app):

    def __init__(self):
        super(cleanup, self).__init__()

    def configure(self, options):
        if options['keep_intermediate_data']:
            self.execution_required = True

    def execute(self):
        print 'executing --- cleanup'


class warping(process_app):

    def __init__(self):
        super(warping, self).__init__()

    def configure(self, options):
        if options['include_warp']:
            self.execution_required = True

    def execute(self):
        print 'executing --- warping'


class convert(process_app):

    def __init__(self):
        super(convert, self).__init__()

    def configure(self, options):
        if options['include_convert']:
            self.execution_required = True

    def execute(self):
        print 'executing --- convert'


def initialize(options):
    # TODO - The smarts to decide what processing steps are required and
    #        a list of them is returned
    # TODO - Return them already configured

    # TODO - This is not the smarts required and needs much more work
    processing_steps = list()
    app = ls_app()
    app.configure(options)
    if app.execution_required:
        processing_steps.append(app)
    app = ps_app()
    app.configure(options)
    if app.execution_required:
        processing_steps.append(app)
    app = hh_app()
    app.configure(options)
    if app.execution_required:
        processing_steps.append(app)
    app = cleanup()
    app.configure(options)
    if app.execution_required:
        processing_steps.append(app)
    app = warping()
    app.configure(options)
    if app.execution_required:
        processing_steps.append(app)
    app = convert()
    app.configure(options)
    if app.execution_required:
        processing_steps.append(app)

    return processing_steps


if __name__ == '__main__':
    options = {
        'include_ls': True,
        'include_ps': False,
        'include_hh': True,
        'keep_intermediate_data': True,
        'include_warp': True,
        'include_convert': False
    }

    print options

    processing_steps = initialize(options)

    for p_step in processing_steps:
        p_step.execute()
