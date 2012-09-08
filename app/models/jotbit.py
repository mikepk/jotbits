from pybald.db import models

import base64
import uuid

def gen_name():
    return base64.urlsafe_b64encode(uuid.uuid4().hex).lower().rstrip("=")[:10]

# sphinx search requires numeric document id's rather than strings
class JotBit(models.Model):
    url_slug = models.Column(models.Unicode(40), index=True, unique=True)
    title = models.Column(models.Unicode(120), default=u'')
    text = models.Column(models.UnicodeText, default=u'')
    date_created = models.Column(models.DateTime, default="now()")

    def __init__(self, *pargs, **kargs):
        if 'name' not in kargs:
            self.url_slug = gen_name()
        super(JotBit, self).__init__(*pargs, **kargs)

