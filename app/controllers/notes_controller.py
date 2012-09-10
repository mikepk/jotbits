from pybald.core.controllers import action, BaseController, render_view

from jotbits.app.models import JotBit
from diff_match_patch import diff_match_patch

dmp = diff_match_patch()

import re
TITLE_PATTERN = re.compile(r'(.{0,140})')
def get_title(text):
    match = TITLE_PATTERN.match(text)
    if match:
        return match.group(0)
    else:
        return ''

def diff(text1, text2):
    return dmp.diff_main(text1, text2)

def delta(diff):
    return dmp.diff_toDelta(diff)

class NotesController(BaseController):
    '''The Notes Controller.'''

    @action
    def new(self, req):
        jb = JotBit()
        return self._redirect_to('note_show', url_slug=jb.url_slug)

    @action
    def show(self, req):
        self.url_slug = self.url_slug[:40]
        try:
            jb = JotBit.get(url_slug=self.url_slug)
        except JotBit.NotFound:
            jb = JotBit(url_slug=self.url_slug)
        self.text = jb.text or ''

        return render_view(template="note", data=self.__dict__)

    @action
    def update(self, req):
        # only take the first 40 chars
        self.url_slug = self.url_slug[:40]
        text = req.POST.get('text', u'')
        # the first line of text is special.
        title = get_title(text)

        try:
            jb = JotBit.get(url_slug=self.url_slug)
        except JotBit.NotFound:
            jb = JotBit(url_slug=self.url_slug, title=title, text=text)
            jb.save()
        else:
            print delta(diff(jb.text, text))
            jb.title=title
            jb.text=text

        self.text = jb.text or ''
        self.template_id = "note"
