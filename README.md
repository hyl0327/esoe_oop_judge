esoe_oop_judge
==============

ESOE OOP Judge is the judge system used by the Object-Oriented Programming
course at NTU ESOE. Written in Django and Bootstrap, it aims to be a judge
system that is safe, easy-to-use, and easy-to-administrate.

The judge system reads Java code. Students are asked to upload their code to
Bitbucket, where the judge system will then grab the code and check their
correctness. This way, students are expected to learn the idea of version
control via Git.

What makes ESOE OOP Judge most valuable is that it allows a problem to be
separated into multiple compilation units (.java files), some of which might
be provided by the problem itself, and the others should be implemented by
the students. This makes it easy for students to understand the idea of OOP
by obligating them to separate their code logics into reasonable smaller parts.


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
guide (credits to Yun-Tao Chen (陳雲濤) and Sher-Win Chen (陳善文)).


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
   corresponding to this problem into that directory (see
   `<JUDGE_PROBLEMS_DIR>/sample/` for sample).
3. If there are any required files marked provided, then you should also create
   a new directory in `<JUDGE_STATIC_PROBLEMS_DIR>` named `PK`, and then put
   them into that directory. After that, you should run `python
   <WEB_DIR>/manage.py collectstatic`.

### Utilities
Utilities are located in `<UTILITIES_DIR>`. Before you use them, make sure you
have activated virtualenv.

- `add_users.py`: Add new users. It takes input from `stdin`, where each line
  should be in the form of `student_id, name`.
- `stats.py`: User statistics. See `python <UTILITIES_DIR>/stats.py -h` for more
  details.


## Credits

Credits to [ADA2015](http://ada2015.csie.org) for inspiration.
