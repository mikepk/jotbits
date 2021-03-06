#!/usr/bin/env python
# encoding: utf-8
from pybald.core.controllers import BaseController
from pybald.core import pybald_class_loader
controllers_path = __path__[0]
__all__ = pybald_class_loader(controllers_path, (BaseController,), globals(), locals())