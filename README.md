# specl

[![Build Status](https://travis-ci.com/tgdolan/specl.svg?branch=master)](https://travis-ci.com/tgdolan/specl)
[![Maintainability](https://api.codeclimate.com/v1/badges/ec16086625f4fa28cd90/maintainability)](https://codeclimate.com/github/tgdolan/specl/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ec16086625f4fa28cd90/test_coverage)](https://codeclimate.com/github/tgdolan/specl/test_coverage)

A spec-driven data cleanup library
---

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Overview](#overview)
  - [Features](#features)
      - [Up Next](#up-next)
    - [File Types Supported:](#file-types-supported)
  - [Running Samples](#running-samples)
  - [Running Tests](#running-tests)
- [Anatomy of a specl spec](#anatomy-of-a-specl-spec)
    - [Reading Data](#reading-data)
    - [Transforming Data](#transforming-data)
    - [Writing Data](#writing-data)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
---

## Overview

specl is a library of functions for cleaning data based on information in a 'spec' file. specl wraps a subset of methods in the Pandas DataFrame API,
supplying those methods with arguments from a YAML spec file. The intent is to
isolate the data cleanup requirements from the code and make it easier to perform common data cleanup tasks.

### Features

specl currently supports the following data cleanup tasks:

* Removing columns from source data
* Renaming columns
* Dropping rows with empty values
* Adding new columns based on values from existing columns

##### Up Next

* Re-introduce previously implemented tests
* Add tests for cli and tasks modules
* Filter columns based on values
* Test utilizing Dask vs. Pandas for the backend data manipulation


#### Code Overview

The entry point for specl implmentation is in `specl.specl.py`.
See the 'execute' function.

The entry point for specl tests is in `tests/test_specl.py`.

#### File Types Supported:

.csv, .xls, .xlsx, .parquet

### Running Samples

There is a sample spec and data file in the `samples/specs` and `samples/data` directories, respectively.
You can clean the sample data based on the sample spec in two ways:

* via standalone Luigi task: `python -m specl.tasks`

  View output in `samples/output/out.csv`
* via command line: `python -m specl.cli --spec 'samples/specs/sample_spec.yml' --log INFO`

  View output in terminal.

### Running Tests

To run pytest with coverage:

`pytest --cov=specl --cov-report html`

Running tests and displaying Hypothesis stats:

`pytest --hypothesis-show-statistics`

## Anatomy of a specl spec

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

#### Reading Data
Reading of data is controlled with the input section of the spec.
The source file(s) are determined by the value of the 'file' key in the input section.

Only columns included in the spec will be included in the resulting data frame. You can define new names for
columns by including an optional 'name' key with a value of the new name for the column.

#### Transforming Data
Once read, the data can be manipulate by defining transforms in the transform
section of the spec. In the case of the example, a new column, 'COLUMN_D' is defined
as being the product of the COLUMN_A and COLUMN_B values. Note that the transform spec
uses the altered column names not the 'source' column names. When creating a new
column, based on other columns, you can specify an operation that will return the value for the column.
This operation can be one of your own or a standard (as in the case of the example) Python
method. The value of the operation key should be in the format of <module>.<method_name>.
The specl functions will dynamically import that module and function at runtime.

#### Writing Data
The output section of the spec defines how the data will be written. The following
output file types are supported
* .csv
* .xls
* .xlsx
* .parquet

### Credits

CSCI-E 29: Thanks, all! I feel like this class plunged me into the deep end of Python. (A good thing.)

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


