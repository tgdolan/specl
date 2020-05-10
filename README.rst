=====
specl
=====


.. image:: https://travis-ci.com/tgdolan/specl.svg?branch=master
    :target: https://travis-ci.com/tgdolan/specl

Python utility for declarative data cleanup.


* Free software: MIT license

Overview
--------
specl is a library of functions that wrap common methods in the Pandas DataFrame API,
supplying those methods with arguments from a YAML spec file. The intent is to
isolate the data cleanup requirements from the code.

Anatomy of a specl spec
~~~~~~~~~~~~~~~~~~~~~~~
The following is the sample spec used for running specl out of the box. This
file is parsed into a Python dictionary and passed to the specl functions. Those
functions pull data from the relevant parts of the spec to build arguments to the
various Pandas DataFrame method calls::

    input:
      # the input section defines how the source data should be read
      # into a Pandas dataframe.
      columns:
        # only columns defined here will be read into the DataFrame.
        column_a:
          data_type: int
          # optionally, rename source columns to a new name in the DataFrame
          name: COLUMN_A
        column_b:
          data_type: int
          name: COLUMN_B
        column_c:
          data_type: int
          name: COLUMN_C
      # the file key defines the location of the source data
      # file types supported: .csv, .xls, .xlsx, .parquet
      file: samples/data/sample1.csv
    transform:
      rows:
          dropna: any
      columns:
        COLUMN_A:
          dropna: all
        COLUMN_B:
          dropna: all
        COLUMN_C:
          dropna: any
        COLUMN_D:
          composed_of:
            - COLUMN_A
            - COLUMN_B
          operation: operator.mul
    output:
      columns:
        COLUMN_C:
          data_type: int
        COLUMN_D:
          data_type: int
      # file types supported: .csv, .xls, .xlsx, .parquet
      file: samples/output/out.csv

Reading Data
~~~~~~~~~~~~
Reading of data is controlled with the input section of the spec.
The source file(s) are determined by the value of the 'file' key in the input section.

Only columns included in the spec will be included in the resulting data frame. You can define new names for
columns by including an optional 'name' key with a value of the new name for the column.

Transforming Data
~~~~~~~~~~~~~~~~~
Once read, the data can be manipulate by defining transforms in the transform
section of the spec. In the case of the example, a new column, 'COLUMN_D' is defined
as being the product of the COLUMN_A and COLUMN_B values. Note that the transform spec
uses the altered column names not the 'source' column names. When creating a new
column, based on other columns, you can specify an operation that will return the value for the column.
This operation can be one of your own or a standard (as in the case of the example) Python
method. The value of the operation key should be in the format of <module>.<method_name>.
The specl functions will dynamically import that module and function at runtime.

Writing Data
~~~~~~~~~~~~
The output section of the spec defines how the data will be written. The following
output file types are supported
* .csv
* .xls
* .xlsx
* .parquet

Running specl
---------------
specl applies data from a YAML file to drive data cleanup. You can run specl with the following command:

``python -m specl.cli --spec samples/specs/sample_spec.yml --log INFO``

where 'sample/specs/sample_spec.yml' is the path to the YAML file that defines how you want the data to be cleaned.

There is also a tasks module that contains a Luigi task to call into specl. You can run it with the following command:

``python -m specl.tasks``

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
