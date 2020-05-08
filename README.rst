=====
specl
=====


.. image:: https://travis-ci.com/tgdolan/specl.svg?branch=master
    :target: https://travis-ci.com/tgdolan/specl

Python utility for declarative data cleanup.


* Free software: MIT license

Getting Started
---------------
specl applies data from a YAML file to drive data cleanup. You can run specl with the following command:

``python -m specl.cli --spec samples/specs/sample_spec.yml --log INFO``

where 'sample/specs/sample_spec.yml' is the path to the YAML file that defines how you want the data to be cleaned.

Running Tests
-------------
To run pytest with coverage:

``pytest --cov=specl --cov-report html``

Running tests and displaying Hypothesis stats:

``pytest --hypothesis-show-statistics``



Features
--------

* Drive data cleanup with a spec.

Code Overview
-------------
Implementation for specl is in a few different modules:

* specl/cli.py -- command line entry point
* specl/specl.py -- core functions
* specl/specl_decorators.py -- logging and function registry decorators

Tests for specl also span a few modules:

* tests/test_specl.py
* tests/test_cli.py
* tests/test_specl_decorators.py
* fixtures.py -- Pytest fixtures
* strategies.py -- Module containing the Hypothesis strategies used to generate random data frames.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
