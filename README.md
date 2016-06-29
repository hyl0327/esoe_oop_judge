esoe_oop_judge
==============

The judge system used by the OOP course at NTU ESOE.

Written in Python/Django/Bootstrap, it offers a judge system that is safe,
easy-to-use, and easy-to-administrate.

It uses Java as its judging language (that is, users should submit Java code)
and Bitbucket as its judging platform (that is, users should submit code to
Bitbucket), so that users are expected to learn from using this system how to
code in Java as well as how to use Git.

As a judge system for an OOP course, it allows problems that require multiple
files (either submitted or provided) to be compiled together, which is different
from traditional judge systems that usually allow only problems that require a
single file to be compiled. In this way, users are able to further understand
the concept of OOP by being forced to separate their code logic into multiple
files, some of which might even be provided from the problem itself.


## Prerequisites

This system is assumed to be run on a Linux machine (Debian and CentOS have been
tested), and it requires the following packages or programs.

- Python (>= 3.5) (with virtualenv and pip)
- Apache HTTP Server (with mod_wsgi corresponding to Python's version)
- MySQL
- cURL
- JRE & JDK
- diff


## Directories

The following parts of this documentation use `<ROOT_DIR>` to refer to
the project root directory (that is, the directory in which you cloned this
project), and `<*_DIR>` to refer to some other directories based on
`<ROOT_DIR>`.

Generally speaking, `<FOO_BAR_DIR>` refers to the directory
`<ROOT_DIR>/foo/bar/`. For complete information on directories, see
`<ROOT_DIR>/config.py`.


## Installation

1. Clone this project.
2. Create a virtualenv at `<VIRTUALENV_DIR>` and then activate it.
3. Install required packages as listed in `<ROOT_DIR>/requirements.txt` via pip.
4. Create a MySQL database for this system.
5. Set up a WSGI application for this system, and make its document root be at
   `<WEB_HTDOCS_DIR>`.
6. Create a Bitbucket account for this system.
7. Set up `<ROOT_DIR>/config.py`.
8. Run `python <WEB_DIR>/manage.py migrate` and `python <WEB_DIR>/manage.py
   collectstatic`.
9. Make `<JUDGE_SUBMISSIONS_DIR>` writable for the WSGI application (either by
   `chown` or `chmod`).
10. Create a superuser by `python <WEB_DIR>/manage.py createsuperuser`.
11. Visit the admin page (see below for how to get to the admin page). Add a new
    profile for the superuser you just created, and then add the first problem
    (see below for how to add new problems).
12. Enjoy it!


## Usage

You may visit `/` (the index page) for a brief guide on using this system.

In case you find it not clear enough, you may further refer to
`<DOCS_DIR>/usage_windows.pdf` or `<DOCS_DIR>/usage_mac.pdf` for a step-by-step
guide (credits to Yun-Tao Chen (陳雲濤) and Shan-Wen Chen (陳善文)).


## Administration

### The Admin Page
You may visit `/admin/` for the admin page.

### Adding New Problems
1. Add a new problem in the admin page, and you will get its `PK`. Note that the
   problem detail page is rendered with MathJax, so you may use some LaTeX in
   the problem's description, input/output format, and sample input/output.
2. Create a new directory in `<JUDGE_PROBLEMS_DIR>` named `PK` (for example,
   if the problem you just added has a `PK` of `1`, then the directory should be
   named `1`), and then put the `Main.java`, `input.txt`, and `answer.txt`
   corresponding to this problem into that directory.
3. If there are any required files marked provided, then you should also create
   a new directory in `<JUDGE_STATIC_PROBLEMS_DIR>` named `PK`, and then put
   them into that directory. After that, you should run `python
   <WEB_DIR>/manage.py collectstatic`.

### Utilities
Utilities are located in `<UTILITIES_DIR>`. Before you use them, make sure you
have activated virtualenv.

- `add_users.py`: Add new users. It takes input from `stdin`, where each line
  should be in the form of `student_id,name`.
- `stats.py`: User statistics. See `python <UTILITIES_DIR>/stats.py -h` for more
  details.


## Credits

Credits to [ADA2015](http://ada2015.csie.org) for inspiration.
