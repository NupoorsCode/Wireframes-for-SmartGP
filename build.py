#!/usr/bin/env python3
"""Inline every asset into one HTML file — handy for emailing a build to
stakeholders who will not clone a repo. Run: python3 build.py"""
import re, pathlib

root = pathlib.Path(__file__).parent
html = (root / 'index.html').read_text()

css = (root / 'assets/css/styles.css').read_text()
html = html.replace('<link rel="stylesheet" href="assets/css/styles.css">',
                    '<style>\n' + css + '\n</style>')

def js(name):
    return (root / 'assets/js' / (name + '.js')).read_text()

bundle = '\n;\n'.join(js(n) for n in
                      ['data', 'core', 'site', 'journey', 'account', 'admin', 'app'])
html = re.sub(r'<script src="assets/js/[a-z]+\.js"></script>\s*', '', html)
html = html.replace('</body>', '<script>\n' + bundle + '\n</script>\n</body>')

out = root / 'SmartGP-preview.html'
out.write_text(html)
print('Wrote', out, f'({len(html)//1024} KB)')
