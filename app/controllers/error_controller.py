#!/usr/bin/env python
# encoding: utf-8
"""
ErrorController.py

Created by mikepk on 2012-09-06.
Copyright (c) 2012 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest
from pybald.core.controllers import action, BaseController
from webob import Response
from mako import exceptions
from pybald.core.errors import pybald_error_template
import re
import project
from pybald.db import models
from collections import defaultdict

from functools import update_wrapper, wraps

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# def send_error_email(host=None, html=None, text=None):


#     if host:
#         host = ': {0}'.format(host)
#     else:
#         host = ''

#     me = "sysadmin@smarterer.com"
#     you = "ops@smarterer.com"

#     msg = MIMEMultipart('alternative')
#     if text:
#         msg.attach(MIMEText(text, 'text'))

#     if html:
#         msg.attach(MIMEText(html, 'html'))

#     msg['Subject'] = '''Smarterer Exception'''.format(host)
#     msg['From'] = "System Error{0} <sysadmin@smarterer.com>".format(host)
#     msg['To'] = you

#     AuthUser="sysadmin@smarterer.com"
#     AuthPass="thej7oyct5yoarg5"

#     gmail = smtplib.SMTP('smtp.gmail.com',587)
#     gmail.ehlo()
#     gmail.starttls()
#     gmail.ehlo()
#     gmail.login(AuthUser, AuthPass) #'mike.pk@gmail.com','********')

#     # s = smtplib.SMTP()
#     gmail.sendmail(me, [you], msg.as_string())
#     gmail.close()

#     return True


class ErrorController(BaseController):
    '''Controller to handle error exceptions.'''
    # map status codes to error controller actions
    error_map = defaultdict(lambda:'general_error',
                                    {404:'not_found',
                                     410:'gone',
                                     401:'not_authorized',
                                     500:'general_error'})


    def __init__(self, *pargs, **kargs):
        '''Setup the error controller'''
        self.status_code = kargs.pop('status_code', 500)
        self.message = kargs.pop('message', None)
        super(ErrorController, self).__init__(*pargs, **kargs)


    def __getattr__(self, key):
        '''Override getattr for missing methods.'''
        # This is a bit hacky, all atributes of ErrorController return
        # this method?
        # TODO: fix this interaction between pybald and the error controller
        return self.http_client_error

    def _pre(self, req):
        self.format = "html"

    @action
    def http_client_error(self, req):
        '''A normal, non-code, http error'''
        try:
            self.template_id = os.path.join('error', self.error_map[self.status_code])
            return Response(body=self._view(), status=self.status_code)
        except Exception, err:
            self.template_id = os.path.join('error', 'general_error')
            return Response(body=self._view(), status=self.status_code)


    @action
    def __call__(self, req):
        '''
        The ErrorController will return a formatted stack trace if in debug
        mode, or point to the regular error page otherwise.
        '''
        if project.email_errors or project.debug:
            stack_trace = pybald_error_template().render(req=req)

        # if project.email_errors:
        #     send_error_email(host=req.host, html=stack_trace)

        if project.debug:
            return Response(body=stack_trace, status=self.status_code)
        else:
            self.template_id = os.path.join('error', self.error_map[self.status_code])
            return Response(body=self._view(), status=self.status_code)


class ErrorControllerTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()