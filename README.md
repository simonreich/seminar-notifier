# seminar-notifier

This is a seminar notifier written in Python. It will send mails to students and supervisors before and after a session.


# Installation notices

You need to install the following packages: `pyaml` and `jinja2`. For mail sending `sendmail` must be installed.


# Installation

1. Copy the folder `seminar.example` to a more meaningful name, e.g. `seminar.journalclub`.
2. Open the file `globalconfig.yaml` and change the path in `seminars` to the full path of `seminar.journalclub`. Multiple seminars are comma separated.
2. If necessary, change the path to the sendmail binary in `sendmail`.


# Setting up one seminar

## Seminar configuration

There is the file `config.yaml` In your `seminar.journalclub` folder. It contains the following options:

```yaml
active: false
```

If this is set to false, no mails are sent, except error reports to the addresses listed in `mailadmin` (see below).

```yaml
student-event: [03.11.2018, 20.12.2018]
```

All students listed in the file file `config/talks.csv` will receive an email on this date. As template the files `template/student-event-03.11.2018.txt.jinja` and `template/student-event-20.12.2018.txt.jinja` are used. They must exist and be readable, otherwise an error is thrown.

```yaml
supervisor-event: [05.11.2018]
```

Similar to student-event, but mails are sent to people listed as supervisor in `config/talks.csv`.

```yaml
student-pre: [0, 1]
```

All students will receive an email 0 days (one the same day as the talk) and 1 day prior a talk a mail. Integer values `>=0` are allowed. As templates `template/student-pre-0.txt.jinja` and `template/student-pre-1.txt.jinja` are used (and must exist and be readable).

```yaml
student-post: [1]
```

All students will receive 1 day after a talk - similar to `student-pre`. The file `template/student-post-`.txt.jinja` is used as template. Please note that `student-post: [0]` and `student-pre: [0]` will both send mails on the same day!

```yaml
supervisor-pre: [0, 1]
```

The supervisor of a talk will receive a reminder on the day of the talk and one day prior the talk. As template `template/supervisor-pre-0.txt.jinja` and `template/supervisor-pre-1.txt.jinja` is used and must exist and be readable.

```yaml
supervisor-post: [1]
```

The supervisor of a talk will receive a mail ` day after ther talk imilar to `student-post`. The files `template/supervisor-post-1.txt.jinja` must exist and be readable.

```yaml
seminarname: "Journal Club"
```

This is the name of your seminar. The string is used in mail templates.

```yaml
mailsubject: "Research Seminar"
```

This is the subject line of all mails.

```yaml
mailcopy: [prof@example.com]
```

All mails except error reports will be BCC'ed to this addresses. Multiple addresses are comma separated.

```yaml
mailadmin: [admin@example.com]
```

All error reports are sent to this addresses. Multiple addresses are comma separated.


## Talks configuration

All talks are configured using the file `config/talks.csv`. It is a comma-separtated-file where the first line contains the header (which is not parsed):

Date	|	Firstname	|	Lastname	|	Mail	|	Title	|	Abstract	|	Supervisor	|	Supervisormail
---	|	---	|	---	|	---	|	---	|	---	|	---	|	---
06.11.2018	|	NameA	|	AA	|	a@example.com	|	Title A	|	Yes! Abstract	|	Supervisor A	|	sa@example.com
13.11.2018	|	NameB	|	BB	|	b@example.com	|	Title B	|	Yes! Abstract	|	Supervisor B	|	sb@example.com
20.11.2018	|	NameC	|	CC	|	c@example.com	|	Title C	|	Yes! Abstract	|	Supervisor C	|	sc@example.com
27.11.2018	|	NameD	|	DD	|	d@example.com	|	Title D	|	Yes! Abstract	|	Supervisor D	|	sd@example.com
04.12.2018	|     	|	  	|	             	|	       	|	             	|	             	|	              

The above above example holds four talks and one session, without any talks on December 04th.


## Template configuration

The following jinja2 short codes can be used in all templates, except the admin template:

`{{ student_firstname|escape }}` lists a student's first name.

`{{ student_lastname|escape }}` lists a student's last name.

`{{ supervisor_name|escape }}` lists a student's supervisor name.

`{{ talk[]|escape }}` lists a student's talk as python list in the format from `config/talks.csv` (date, first name, last name, mail, ...): i.e. `{{ talk[0]|escape }}` will be replaced with the date of the student's talk.

`{{ seminar_name|escape }}` will be replaced with the seminar name.

`{{ schedule|escape }}` will be replaced with a schedule of all upcoming talks.

`{{ talk_list[[]]|escape }}` holds a python list of all talks identified important for that template. One talk is a python list in the same format as `config/talks.csv` (date, first name, last name, mail, ...): i.e. `{{ talk[0]|escape }}` will be replaced with the date of the talk.


The following jinja2 short codes can be used in the admin template:

`{{ seminar_name|escape }}` will be replaced with the seminar name.

`{{ problem_list[]|escape }}` lists all errors as python list.
