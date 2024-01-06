# Custom stub files

This directory contains custom stub files for *mypy*.

These have been created using `stubgen`. `brother_ql.labels` required two changes for this as *stubgen* would complain otherwise. Additionally, some general *mypy* conflicts have been resolved, mostly about duplicate definitions.

The current type hints are kept as basic as possible to let *mypy* strict mode pass on the *brother_ql_web* code itself. Not used features of the third-party libraries might have appropriate type hints, but this is not guaranteed.
