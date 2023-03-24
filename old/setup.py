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
    "Kivy==1.11.1",
    "Kivy-Garden==0.1.4",
    'docutils;platform_system == "Windows"',
    'pygments;platform_system == "Windows"',
    'pypiwin32;platform_system == "Windows"',
    'kivy_deps.sdl2==0.1.22;platform_system == "Windows"',
    'kivy_deps.glew==0.1.12;platform_system == "Windows"',
    'kivy_deps.angle==0.1.9;platform_system == "Windows"',
]

extras_require = {
    'tests': [
        'pytest',
        'pytest-cov',
        'pytest-random-order>=1.0.0',
        'pytest-faulthandler',
        'coverage',
        'pycodestyle',
        'pyflakes',
        'black',
    ],
    'docs': [
        'sphinx',
    ],
    'package': [
        # Wheel building and PyPI uploading
        'wheel',
        'twine',
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
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__url__'],
    license=about['__license__'],
    packages=['pypercard', ],
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Android",
        "Operating System :: iOS",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Education",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Widget Sets",
        "Topic :: System :: Software Distribution",
    ]
)
