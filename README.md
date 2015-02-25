# sota/lang
The implementation of the sota programming language

# Getting Started
The sota build system uses doit (http://pydoit.org) for compiling and running tests.  One can install it from mulitple locations:
- https://pypi.python.org/pypi/doit
- https://github.com/pydoit/doit

# Pip Dependencies
Sota uses pyflakes and pytest.  You can install them individually or use the pipdeps.py file to do it for you.

doit -f pipdeps.py

# Git Submodules
The sota/lang repo contains several git submodule pointers located in the repos/ directory.  You can manipulate these with git commands, but the dodo.py file has tasks to ensure the repos are updated and init'd.

# Compiling
Running the doit command in the root of the sota/lang repo should run the tasks listed in dodo.py to run some prebuild actions, the bulid itself and some postbuild actions.  The doit infrastructure tracks when files are modified and only runs tasks that have been affected by these changes.  Running the doit command multiple times after the inital run should finish quickly, not changing anything.

# Build Results
After a successful build there should be 2 test results files, sota.pre-tests and sota.post-tests and the sota executable.
