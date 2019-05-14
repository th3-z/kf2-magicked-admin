Contributing
============

I'm currently accepting contributions to this project. 

The codebase on GitHub is a mirror of the version on my 
[VCS](https://git.th3-z.xyz/kf2-magicked-admin). Please clone the version from
my VCS, instructions in `README.md`, as this is the cannonical version.

The `ISSUES.md` file contains an incomplete list of know issues, this includes
planned features and bugs.

I can be contacted by [email](mailto:the_z@znel.org) or on
[Steam](https://steamcommunity.com/id/th3-z), either is fine.

How can I contribute?
---------------------

Clone the current master branch and gave a go at some of the following tasks.
The binaries on the release page are not useful to contributors, they are out
of date. Tasks, in order of increasing complexity.

- Bug reports are needed right now. There are no plans to add new features 
until master is stable. 
    * You will need a Killing Floor 2 server for testing.
    * Testing on multiple servers. This tools can manage multiple servers at
    once, I only have one.
    * Please don't send me bug reports for the releases (0.0.7). These are out
    of date.
- Linting. I have added a make target that runs a linter, `make lint`. Running 
this will give you a huge list (200+) of minor code style errors. I want this 
to return no issues.
- Debugging. Check the bugs in `ISSUES.md`, see if you can replicate them, and
fix them. Send me patches via email. If you find an issue you can't correct, 
please add it to the `ISSUES.md` and send me a patch.
- Feature additions. I'm not focussing on new features right now, but if you 
can't help yourself, see `ISSUES.md`.

Code
----

If you wish to contribute code, please see `ISSUES.md` for the current task
list. Once you've completed a task, update the `ISSUES.md` file and send me a
[patch](https://git-scm.com/docs/git-format-patch) with your changes by 
[email](mailto:the\_z@znel.org).

The `README.md` file has further details about dependencies and configuring
your environment.

N.b. all contributions will be released under the MIT license.

Bug Reports
-----------

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

If you could include a patch that appends your issue to `ISSUES.md`, that would
be helpful too, otherwise I can add it.

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

