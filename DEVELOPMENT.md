.. highlight:: shell

Development
===========

Get Started!
------------

Ready to contribute? Here's how to set up `labop_labware_ontology` for local development.

#. Clone the `labop_labware_ontology` repo from GitLab::

    $ git clone git@gitlab.com:opensourcelab/labop-labware-ontology.git

#. Ensure `poetry is installed`_.
#. Install dependencies and start your virtualenv::

    $ poetry install
    $ poetry shell

#. Create a branch for local development::

    $ git checkout -b feature/IssueNumber_name-of-your-bugfix-or-feature

    # please do not use the '#' in branch names !

Now you can make your changes locally.

#. When you're done making changes, check that your changes pass the
   tests, including testing other Python versions, with tox::

    $ tox

#. Commit your changes and push your branch to GitLab::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin feature/IssueNumber_name-of-your-bugfix-or-feature

#. Submit a merge request through GitLab

.. _poetry is installed: https://python-poetry.org/docs/

Merge Request Guidelines
-------------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should only include changes relating to one ticket.
2. The merge request should include tests to cover any added changes and 
   check that all existing and new tests pass.
3. If the merge request adds functionality, the docs should be updated.
   Put your new functionality into a function with a docstring, and add
   the feature to the list in README.rst.
4. The team should be informed of any impactful changes.

Documentation
--------------

The Sphinx Documentation Sytem is used, 

markdown is supported via the mystparser ( https://cerodell.github.io/sphinx-quickstart-guide/build/html/markdown.html )

To build the documentation, run

    $ invoke docs

Tips
----

#. To run a subset of tests::

    $ pytest tests.test_labop_labware_ontology

Deploying to PyPI
-----------------

For every release:

#. Update HISTORY.rst

#. Update version number (can also be patch or major)::

    bump2version minor

#. Run the static analysis and tests::

    tox

#. Commit the changes::

    git add HISTORY.rst
    git commit -m "Changelog for upcoming release <#.#.#>"

#. Push the commit::

    git push

#. Add the release tag (version) on GitLab: https://gitlab.com/opensourcelab/labop-labware-ontology/-/tags

The GitLab CI pipeline will then deploy to PyPI if tests pass.
