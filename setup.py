import os
import re
from setuptools import setup


base_dir = os.path.dirname(__file__)


DUNDER_ASSIGN_RE = re.compile(r"""^__\w+__\s*=\s*['"].+['"]$""")
about = {}
with open(os.path.join(base_dir, 'pypercard', '__init__.py'),
          encoding='utf8') as f:
    for line in f:
        if DUNDER_ASSIGN_RE.search(line):
            exec(line, about)

with open(os.path.join(base_dir, 'README.md'), encoding='utf8') as f:
    readme = f.read()

with open(os.path.join(base_dir, 'CHANGES.md'), encoding='utf8') as f:
    changes = f.read()


install_requires = [
    "Kivy==2.0.0.dev0",
    "Kivy-Garden==0.1.4",
]


extras_require = {
    'tests': [
        'pytest',
        'pytest-cov',
        'pytest-random-order>=1.0.0',
        'pytest-faulthandler',
        'coverage',
    ],
    'docs': [
        'sphinx',
    ],
    'package': [
        # Wheel building and PyPI uploading
        'wheel',
        'twine',
        # Windows native packaging (see win_installer.py).
    ],
}

extras_require['dev'] = (
    extras_require['tests'] +
    extras_require['docs'] +
    extras_require['package']
)

extras_require['all'] = list({
    req
    for extra, reqs in extras_require.items()
    for req in reqs
})


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description='{}\n\n{}'.format(readme, changes),
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__url__'],
    license=about['__license__'],
    packages=['pypercard', ],
    install_requires=install_requires,
    extras_requires=extras_requires,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
    ]
)
