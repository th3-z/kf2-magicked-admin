Contributing
============

Code
----

If you wish to contribute code, please see `ISSUES.md` for the current task
list. Once you've completed a task, update the `ISSUES.md` file and send me the 
[patches](https://git-scm.com/docs/git-format-patch) with your commits by 
[email](mailto:the\_z@znel.org).

The `README.md` file has further details about dependencies and configuring
your environment.

N.b., all contributions will be released under the MIT license.

Reporting bugs
--------------

All issues, including bugs, are tracked in the `ISSUES.md` file. Bug reports
can be submitted by email to the [author](mailto:the\_z@znel.org) or relevant 
contributor. Good bug reports should include the following.

* Clear and descriptive title.
* Version of the software you are using.
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
* Further details in description.
* No emoji.

### Python
Python has well defined standards for code style, 
see [PEP8](https://www.python.org/dev/peps/pep-0008/). Please Use `make lint` 
to check for style issues, this will use `flake8` to test compliance.

### Documents
Documents are all written in Markdown, to the 
[CommonMark](https://spec.commonmark.org/current/) specification. Use of GFM
and other extensions are erroneous, and should be raised as issues.

* Maximum line length of 79 characters.
* No emoji.

