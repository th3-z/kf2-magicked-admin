Contributing
============

I'm currently accepting contributions to this project. 

I can be contacted by [email](mailto:the_z@znel.org) or on
[Steam](https://steamcommunity.com/id/th3-z), either is fine.

We have a Steam group chat for contributors to discuss development,
an invite will be provided.

How can I contribute?
---------------------

- Bug reports.
    * You will need a Killing Floor 2 server for testing.
    * Raise bug reports on the issue tracker, a template is provided.
- Translations.
    * Translations are done via [Crowdin](https://crowdin.com/project/kf2-magicked-admin)
    * Anyone is welcome to make contributions to the translations.
- Debugging. Check the bugs on the issue tracker, see if you can replicate them, and
try to fix them.
- Features. Desired features are listed on the issue tracker, implement and raise a
pull request.

There are templates for feature requests, bug reports, and pull requests to help you
get started.

Code
----

If you wish to contribute code, please see the issue tracker for the current 
task list. Once you've completed a task, raise a pull request.

The `README.md` file has further details about dependencies and configuring
your environment.

N.b. all contributions will be released under the MIT license.

Bug Reports
-----------

All issues, including bugs, are tracked in the issues tab. Good bug reports 
should include the following.

* Clear and descriptive title.
* Exact steps to reproduce the bug.
* What is observed after following the steps.
    - Pastes of output or screenshots are helpful.
* Description of expected behaviour.
* Environment details.
    - Python version.
    - Operating system.
    - Configuration file, please censor any credentials.

Style
-----

### Commit messages
* Imperative present tense.
* 50 character first line.
    - Capitalise first character, no period.
* Further details in commit description.

### Python
Python has well defined standards for code style, 
see [PEP8](https://www.python.org/dev/peps/pep-0008/). Please Use `make lint` 
to check for style issues, this will use `flake8` to test compliance.

### Documents
Documents are all written in GitHub flavoured markdown.

* Maximum line length of 79 characters.

