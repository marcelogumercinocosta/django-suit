import sys
import os
import time

class LessCompiler():

    def __init__(self, source):
        self.source = source

    def compile_css(self):
        destination = self.source.replace('less', 'css')
        cmd = 'lessc %s > %s --clean-css="--s1 --advanced --compatibility=ie8"' % (self.source, os.path.abspath(destination))
        os.system(cmd)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write(
            'Usage: %s LessCompiler\n' % sys.argv[0])
        sys.exit(1)

    source = os.path.abspath("static/suit/less/suit.less")
    event_handler = LessCompiler(source)
    # # Run once at startup
    event_handler.compile_css()
