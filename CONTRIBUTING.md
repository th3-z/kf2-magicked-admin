Contributing
============

I'm currently accepting contributions to this project. 

I can be contacted by [email](mailto:the_z@znel.org) or on
[Steam](https://steamcommunity.com/id/th3-z), either is fine.

How can I contribute?
---------------------

- Bug reports are needed right now. There are no plans to add new features 
until master is stable. 
    * You will need a Killing Floor 2 server for testing.
    * Testing on multiple servers. This tools can manage multiple servers at
    once, I only have one.
    * Please don't raise issues for release 0.0.7. This release is out
    of date.
- Translations. The project needs translators, please contact me if you can
help with this.
- Linting. I have added a make target that runs a linter, `make lint`. Running 
this will give you a huge list (200+) of minor code style errors. I want this 
to return no issues.
- Debugging. Check the bugs on the issue tracker, see if you can replicate them, and
try to fix them.

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

