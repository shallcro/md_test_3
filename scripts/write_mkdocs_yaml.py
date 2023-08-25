import os
import shutil
import subprocess

mkdocs_yaml = 'C:/icpsr-gitlab/current-schema/docs/mkdocs.yaml'
html_dir = 'C:/icpsr-gitlab/current-schema/docs/html'

# if os.path.exists(mkdocs_yaml):
#     print('Removing old config...')
#     os.remove(mkdocs_yaml)

for theme in ['readthedocs']: #, 'mkdocs', 'bootstrap', 'ivory', 'gitbook', 'bootstrap4']:
    print(f'Working on {theme}...\n')
    out_dir = os.path.join(html_dir, theme)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    info = ["site_name: ICPSR Curated Study Metadata Schema\n",
    "docs_dir: markdown\n",
    "site_dir: html\\{}\n".format(theme),
    "markdown_extensions:\n"
    "  - tables\n"
    "  - markdown.extensions.smarty\n"
    "plugins: []\n"
    "theme:\n",
    "  name: {}\n".format(theme)
    ]

    with open(mkdocs_yaml, 'w', encoding='utf-8') as fo:
        for line in info:
            fo.write(line)
        if theme=='readthedocs':
            fo.write('    prev_next_buttons_location: none\n')

    cmd = 'mkdocs build --verbose'

    subprocess.run(cmd, shell=True)

    # if theme=='readthedocs':
    #     if not os.path.exists('C:/icpsr-gitlab/current-schema/docs/html/readthedocs/css'):
    #         os.makedirs('C:/icpsr-gitlab/current-schema/docs/html/readthedocs/css')
    #     shutil.copy('C:/icpsr-gitlab/current-schema/docs/readthedocs_theme.css', 'C:/icpsr-gitlab/current-schema/docs/html/readthedocs/css/theme.css')

    