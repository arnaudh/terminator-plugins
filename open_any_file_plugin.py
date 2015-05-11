import inspect
import os
import re
from terminatorlib import plugin, config

AVAILABLE = ['OpenAnyFile']

class OpenAnyFile(plugin.URLHandler):
    capabilities = ['url_handler']
    handler_name = 'openfile'
    nameopen = "Open the file"
    namecopy = "Copy file path"
    match = '[^ \t\n\r\f:]+(:[0-9]+)?'

    def callback(self, url):
        m = re.match(r'([^ \t\n\r\f:]+)(?::([0-9]+))?', url)
        if m and m.group(2):
            url = m.group(1)

        # HACK (from https://github.com/mchelem/terminator-editor-plugin)
        # Because the current working directory is not available to
        # plugins, we need to use the inspect module to climb up the stack to
        # the Terminal object and call get_cwd() from there.
        for frameinfo in inspect.stack():
            frameobj = frameinfo[0].f_locals.get('self')
            if frameobj and frameobj.__class__.__name__ == 'Terminal':
                cwd = frameobj.get_cwd()

        path = os.path.join(cwd, url)
        if os.path.exists(path):
            return path

