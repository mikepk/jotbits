import project
import sys

def map(urls):
    '''
    Defines the url to controller mapping for the application. A 
    routes mapper or submapper object must be passed in.
    '''
    urls.connect('home', r'/', controller="home")

    urls.connect('notes', r'/notes', controller="notes", action="new")
    urls.connect('note_update', r'/notes/{url_slug}', controller="notes",
                                                action="update",
                                                conditions=dict(method=["PUT"]))
    urls.connect('note_show', r'/notes/{url_slug}', controller="notes", action="show",
                                                conditions=dict(method=["GET"]))


    # generic pattern
    # urls.connect('base', r'/{controller}/{action}/{id}')
    # urls.connect(r'/{controller}/{action}')
    # urls.connect(r'/{controller}')



    # REDIRECT ALL URLS TERMINATING IN a slash, '/', to no slash
    # the opposite is also valid, all urls can be forced to have a slash
    # depends on your preference
    urls.redirect('{url:.*}/', '{url}',
                  _redirect_code='301 Moved Permanently')


    # when in debug mode, print the whole URL mapping
    if project.debug:
        sys.stderr.write(str(urls)+"\n")