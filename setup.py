from distutils.core import setup

setup(
    name='sphinx_auto_embed',
    version='0.1',
    description="A utility for generating rst files with automatically embedded code, code output, and other data for documentation.",
    license='Apache-2.0',
    install_requires=[
        'six',
    ],
    packages=[
        'sphinx_auto_embed',
        'sphinx_auto_embed.directives',
    ],
    entry_points="""
        [console_scripts]
        sphinx_auto_embed=sphinx_auto_embed.main:main
    """,
    url = 'https://github.com/hwangjt/sphinx_auto_embed',
    download_url = 'https://github.com/hwangjt/sphinx_auto_embed/archive/v0.1.1-alpha.tar.gz',
)
