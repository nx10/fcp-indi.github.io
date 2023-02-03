# -*- coding: utf-8 -*-
#
# C-PAC documentation build configuration file, created by
# sphinx-quickstart on Fri Jul 20 16:32:55 2012.
#
# This file is execfile()d with the current directory set to its containing
# dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import m2r
import os
import re
import semver
import sys

from CPAC import __version__
from dateutil import parser as dparser
from github import Github
from github.GithubException import RateLimitExceededException, \
    UnknownObjectException
from pybtex.plugin import register_plugin

sys.path.append(os.path.dirname(__file__))

from references import CPAC_DocsStyle  # noqa: E402

register_plugin('pybtex.style.formatting', 'cpac_docs_style', CPAC_DocsStyle)

# "Dealing with Invalid Versions" from
# https://python-semver.readthedocs.io/en/latest/usage.html


def coerce(version):
    """
    Convert an incomplete version string into a semver-compatible VersionInfo
    object

    * Tries to detect a "basic" version string (``major.minor.patch``).
    * If not enough components can be found, missing components are
        set to zero to obtain a valid semver version.

    :param str version: the version string to convert
    :return: a tuple with a :class:`VersionInfo` instance (or ``None``
        if it's not a version) and the rest of the string which doesn't
        belong to a basic version.
    :rtype: tuple(:class:`VersionInfo` | None, str)
    """
    BASEVERSION = re.compile(
        r"""[vV]?
            (?P<major>0|[1-9]\d*)
            (\.
            (?P<minor>0|[1-9]\d*)
            (\.
                (?P<patch>0|[1-9]\d*)
            )?
            )?
        """,
        re.VERBOSE,
    )

    match = BASEVERSION.search(version)
    if not match:
        return (None, version)

    ver = {
        key: 0 if value is None else value for key, value
        in match.groupdict().items()
    }
    ver = semver.VersionInfo(**ver)
    rest = match.string[match.end() :]  # noqa:E203
    return ver, rest


def compare_versions(new, old):
    """
    Function to compare two versions.

    Parameters
    ----------
    new: str

    old: str

    Returns
    -------
    bool
        Is the "new" at least as new as "old"?
    """
    comparisons = list(zip(coerce(new), coerce(old)))
    if any([v is None for v in comparisons[0]]):
        return(False)
    outright = semver.compare(str(comparisons[0][0]), str(comparisons[0][1]))
    return (
        bool(outright == 1) or bool(
            (outright == 0) and comparisons[1][0] >= comparisons[1][1]
        )
    )


# prepare nested pipeline upgrade documentation
def yaml_to_rst(path):
    '''Function to convert a YAML list to RST

    Parameters
    ----------
    path: str

    Returns
    -------
    None
    '''
    lines = open(path, 'r').readlines()
    lines = [
        f'{line[:2]}``{line.rstrip()[2:]}``\n' if line.startswith('- ') else
        f"\n{line.lstrip('# ')}\n" for line in lines
    ]
    path = f'{path[:-4]}.rst'
    open(path, 'w').write(''.join(lines))


yaml_to_rst('references/1.7-1.8-deprecations.yml')

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'
#
# Add any Sphinx extension module names here, as strings. They can be
# extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.bibtex',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinxcontrib.programoutput',
    'exec',
    'nbsphinx',
    'numpydoc']

bibtex_bibfiles = [f'references/{bib}' for bib in os.listdir('references') if
                   bib.endswith('.bib')]
bibtex_default_style = 'cpac_docs_style'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The main toctree document.
master_doc = 'index'

# A list of warning types to suppress arbitrary warning messages.
suppress_warnings = ['autosectionlabel.*']

# General information about the project.
project = 'C-PAC'
copyright = '2012‒2022, C-PAC Developers. C-PAC is licensed under LGPL-3' \
            '.0-or-later'
# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = __version__


# Get tags from GitHub
# Set GITHUBTOKEN to your API token in your environment to increase rate limit.
def _gh_rate_limit():
    print("""Release notes not updated due to GitHub API rate limit.

       MMM.           .MMM      __________________________________________
       MMMMMMMMMMMMMMMMMMM     |                                          |
       MMMMMMMMMMMMMMMMMMM     | Set GITHUBTOKEN to your API token in     |
      MMMMMMMMMMMMMMMMMMMMM    | your environment to increase rate limit. |
     MMMMMMMMMMMMMMMMMMMMMMM   | See CONTRIBUTING.md#environment-notes    |
    MMMMMMMMMMMMMMMMMMMMMMMM   |_   ______________________________________|
    MMMM::- -:::::::- -::MMMM    |/
     MM~:~ 00~:::::~ 00~:~MM
.. MMMMM::.00:::+:::.00::MMMMM ..
      .MM::::: ._. :::::MM.
         MMMM;:::::;MMMM
  -MM        MMMMMMM
  ^  M+     MMMMMMMMM
      MMMMMMM MM MM MM
           MM MM MM MM
           MM MM MM MM
        .~~MM~MM~MM~MM~~.
     ~~~~MM:~MM~~~MM~:MM~~~~
""")


def sort_tag(t):
    return(t[0:-4] if t[0].isdigit() else t[1:-4])


def _unireplace(release_note, unireplace):
    u = release_note.find('\\u')
    if (u != -1):
        e = release_note[u:u+6]
        e2 = str(e[2:])
        release_note = release_note.replace(
            e,
            f' |u{e2}| '
        )
        unireplace[e2] = e
        return(_unireplace(release_note, unireplace))
    return(
        release_note,
        '\n\n'.join([
            f'.. |u{u}| unicode:: {v}\n   :trim:'
            for u, v in list(unireplace.items())
        ])
    )


gh_tags = []
_gh_token = os.environ.get('GITHUBTOKEN')
if _gh_token is None:
    g = None
    _gh_rate_limit()
else:
    g = Github(os.environ.get('GITHUBTOKEN'))
    try:
        gh_cpac = g.get_user('FCP-INDI').get_repo('C-PAC')
        gh_tags = [t.name for t in gh_cpac.get_tags()]
    except RateLimitExceededException:
        _gh_rate_limit()
    gh_tags.sort(reverse=True)

    # don't build release notes for newer releases
    build_version = os.environ.get('CIRCLE_TAG', '').rstrip('-source')
    if len(build_version):
        gh_tags = [gh_tag for gh_tag in gh_tags if compare_versions(
            build_version, gh_tag
        )]

    # Try to get release notes from GitHub
    try:
        gh_releases = []
        for t in gh_tags:
            try:
                gh_releases.append(gh_cpac.get_release(t).raw_data)
            except (AttributeError, UnknownObjectException):
                print(f'No notes for {t}')
        gh_releaseNotes = {r['tag_name']: {
            'name': r['name'],
            'body': r['body'],
            'published_at': r['published_at']
        } for r in gh_releases}
    except RateLimitExceededException:
        _gh_rate_limit()
        gh_releaseNotes = {
            t: {
                'name': t,
                'body': ''.join([
                    'See https://github.com/FCP-INDI/C-PAC/releases/tag/',
                    t,
                    ' for release notes.'
                ]),
                'published_at': None
            } for t in gh_tags
        }

    this_dir = os.path.dirname(os.path.abspath(__file__))
    release_notes_dir = os.path.join(this_dir, 'user', 'release_notes')
    if not os.path.exists(release_notes_dir):
        os.makedirs(release_notes_dir)
    latest_path = os.path.join(release_notes_dir, 'latest.rst')
    # all_release_notes = ''
    for t in gh_tags:
        if t in gh_releaseNotes:
            tag_header = '{}{}{}'.format(
                'Latest Release: ' if t == gh_tags[0] else '',
                (
                    gh_releaseNotes[t]['name'][4:] if (
                        gh_releaseNotes[t]['name'].startswith('CPAC')
                    ) else gh_releaseNotes[t]['name'][5:] if (
                        gh_releaseNotes[t]['name'].startswith('C-PAC')
                    ) else gh_releaseNotes[t]['name']
                ).strip(),
                ' ({})'.format(
                    dparser.parse(gh_releaseNotes[t]['published_at']).date(
                    ).strftime('%b %d, %Y')
                ) if gh_releaseNotes[t]['published_at'] else ''
            )
            release_note = '\n'.join(_unireplace(
                "{}\n{}\n{}".format(
                    tag_header,
                    '^'*len(tag_header),
                    m2r.convert(gh_releaseNotes[t]['body'].encode(
                        'ascii',
                        errors='backslashreplace'
                    ).decode('utf-8'))
                ),
                {}
            ))

            release_notes_path = os.path.join(release_notes_dir, f'{t}.rst')
            if gh_releaseNotes[t]['published_at'] and not os.path.exists(
                release_notes_path
            ) and not os.path.exists(
                os.path.join(release_notes_dir, f'v{t}.rst')
            ):
                with open(release_notes_path, 'w+') as f:
                    f.write(release_note)
            else:
                print(release_notes_path)

            if (
                tag_header.startswith('Latest') and
                not os.path.exists(latest_path)
            ):
                with open(latest_path, 'w+') as f:
                    f.write(
                        """.. include:: /user/release_notes/{latest}.rst

.. toctree::
   :hidden:
   :titlesonly:
   :maxdepth: 1

   /user/release_notes/{latest}.rst
""".format(latest=str(t))
                    )

    rnd = [
        d for d in os.listdir(release_notes_dir) if d not in [
            'index.rst',
            'latest.rst'
        ]
    ]
    rnd.sort(key=sort_tag, reverse=True)

    all_release_notes = """
    {}

    .. toctree::
    :hidden:
    :titlesonly:
    :maxdepth: 1

    {}

    """.format(
        '\n'.join([f'.. include:: /user/release_notes/{fp}' for fp in rnd]),
        '\n   '.join([f'/user/release_notes/{d}' for d in rnd]))
    with open(os.path.join(release_notes_dir, 'index.rst'), 'w+') as f:
        f.write(all_release_notes.strip())

# The full version, including alpha/beta/rc tags.
release = f'{__version__} Beta'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['futuredocs/*']

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'furo'

# The name for this set of Sphinx documents.  If None, it defaults to
# '<project> v<release> documentation'.
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/cpac_logo_vertical.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {
#  '**': [
#    # 'localtoc.html',
#    # 'globaltoc.html',
#    'searchbox.html'
#  ]
# }

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, 'Created using Sphinx' is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, '(C) Copyright ...' is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. '.xhtml').
html_file_suffix = '.html'

# Suffix for generated links to HTML files
html_link_suffix = ''
link_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'C-PACdoc'

# -- Options for LaTeX output -------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    #
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    #
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
  ('index', 'C-PAC.tex', 'C-PAC Documentation',
   'C-PAC Team', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For 'manual' documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True

# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', 'c-pac', 'C-PAC Documentation', ['C-PAC Team'], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False

# -- Options for Texinfo output -----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
# dir menu entry, description, category)
texinfo_documents = [
  ('index', 'C-PAC', 'C-PAC Documentation',
   'C-PAC Team', 'C-PAC', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

rst_epilog = """

.. |Versions| replace:: {versions}

""".format(
    versions=', '.join(gh_tags[:5])
) if len(gh_tags) >= 5 else ""

def setup(app):
    from CPAC.utils.monitoring import custom_logging

    # initilaize class to make factory functions available to Sphinx
    ml = custom_logging.MockLogger('test', 'test.log', 0, '/tmp')
    for method in [
        method for method in
        set(dir(ml)) - set(dir(custom_logging.MockLogger)) if
        method not in ['name', 'handlers']
    ]:
        setattr(custom_logging.MockLogger, method, getattr(ml, method))
