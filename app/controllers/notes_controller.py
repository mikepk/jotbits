from pybald.core.controllers import action, BaseController

from jotbits.app.models import JotBit

import re
TITLE_PATTERN = re.compile(r'(.{0,120})')
def get_title(text):
    match = TITLE_PATTERN.match(text)
    if match:
        return match.group(0)
    else:
        return ''

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
        self.template_id = "note"

    # $.ajax({type:'POST', data:{'_method':'PUT', 'text':$('#note').val()}});
    @action
    def update(self, req):
        self.url_slug = self.url_slug[:40]
        text = req.POST.get('text', '')
        title = get_title(text)
        try:
            jb = JotBit.get(url_slug=self.url_slug)
        except JotBit.NotFound:
            jb = JotBit(url_slug=self.url_slug, title=title, text=text)
            jb.save()
        else:
            jb.title=title
            jb.text=text
        # print str(filter(None, [self.jb.title, self.jb.text]))
        self.text = jb.text or ''
        self.template_id = "note"