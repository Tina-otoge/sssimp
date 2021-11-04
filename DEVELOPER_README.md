# Developer information

## Files breakdown

The module `__init__.py` contains variables and functions that we want to be
available in all files.

The `__main__.py` serves as an entry point for the module and will call the
functions responsible for generating and copying the assets.

The `generators/` folder contains processors for each kind of generatable assets
such as the markdown -> html generator.

Each .py file in the generators folder is imported as a module in no specific
order, if it exists, the `prepare()` function is first called, then once every
file that has a prepare function has been called, the `main()` function is then
called, also only if it exists.
