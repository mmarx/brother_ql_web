# Development version

* Fix printing of umlauts and special characters which would previously fail due to *bottle* oddities.

# Version 0.2.0 - 2023-11-23

* Fix undefined variables introduced due to the migration.
* Add tests.
* Add type hints, including *mypy*.
* Ignore the annoying `brother_ql.devicedependent` message which only has been fixed in Git, but not on PyPI.
* Patch *brother_ql* itself to ensure compatibility with `Pillow>=10`.
* Avoid defaulting to high quality output for now, as there is no proper implementation for it yet and this would raise errors for die cut labels and lead to downscaling followed by upscaling for endless labels.

# Version 0.1.0 - 2023-08-13

* First packaged version.
