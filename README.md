# seminar-notifier

This is a seminar notifier written in Python. It will send mails to students and supervisors before and after a session, or on specific dates.


# Installation notices

You need to install the following packages: `pyaml` and `jinja2`. To set up a virtual environment:

```bash
virtualenv -p python3 ./
source bin/activate
pip install pyaml jinja2
```

For mail sending `sendmail` must be installed. If no mail server is available, [ssmtp](https://linux.die.net/man/8/ssmtp) can be a good alternative.

Installation steps that worked for me:

1.  Install to `/opt/seminar-notifier` on server with `sendmail`.
2.  Create git repository for organizer holding seminar config files and templates on (git-)server. Organizer now can edit files without breaking anything.
3.  Every morning copy config files and templates via cronjob from (git-)server to `/opt/seminar-notifier`.
4.  Run `/opt/seminar-notifier/seminar-notifier.py` via cronjob.


# Setup

1.  Copy the folder `seminar.example` to a more meaningful name, e.g. `seminar.journalclub`.
2.  Open the file `globalconfig.yaml` and change the path in `seminars` to the full path of `seminar.journalclub`. Multiple seminars are comma separated.
2.  If necessary, change the path to the sendmail binary in `sendmail`.


# Setting up one seminar

## Seminar configuration

The file `config.yaml` in the folder `seminar.journalclub` contains the following options:

```yaml
active: false
```

If this is set to false, no mails are sent, except error reports to the addresses listed in `mailadmin` (see below).

```yaml
student-event: [03.11.2018, 20.12.2018]
```

All students listed in the file file `config/talks.csv` will receive an email on these dates. As template the files `template/student-event-03.11.2018.txt.jinja` and `template/student-event-20.12.2018.txt.jinja` are used. They must exist and be readable, otherwise an error is thrown.

Example: "Dear All, this semester our Journal Club will start on ..."

```yaml
supervisor-event: [05.11.2018]
```

Similar to student-event, but mails are sent to people listed as supervisor in `config/talks.csv`.

Example: "Dear Supervisors, on ... our Journal Club is finally over. Please hand in the grading sheets of your students until ..."

```yaml
student-pre: [0, 1]
```

All students will receive an email 0 days (one the same day as the talk) and 1 day prior a talk a mail. Integer values `>=0` are allowed. As templates `template/student-pre-0.txt.jinja` and `template/student-pre-1.txt.jinja` are used (and must exist and be readable).

Example: "Dear Firstname Lastname, tomorrow will be the next session of our Journal Club ..."

```yaml
student-post: [1]
```

All students will receive 1 day after a talk - similar to `student-pre`. The file `template/student-post-1.txt.jinja` is used as template. Please note that `student-post: [0]` and `student-pre: [0]` will both send mails on the same day!

Example: "Dear Firstname Lastname, after yesterday's session please hand in ..."

```yaml
supervisor-pre: [0, 1]
```

The supervisor of a talk will receive a reminder on the day of the talk and one day prior the talk. As template `template/supervisor-pre-0.txt.jinja` and `template/supervisor-pre-1.txt.jinja` is used and must exist and be readable.

Example: "Dear Supervisor, please remember that tomorrow your student Firstname Lastname is giving a presentation on ..."

```yaml
supervisor-post: [1]
```

The supervisor of a talk will receive a mail 1 day after ther talk, similar to `student-post`. The files `template/supervisor-post-1.txt.jinja` must exist and be readable.

Example: "Dear Supervisor, please remember to upload the slides of your student's talk and hand in your grading sheet until ..."

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
07.01.2020 | FirstnameA | LastnameA | a@example.com | Title A | Short Abstract A | Supervisor A | sa@example.com
07.01.2020 | FirstnameB | LastnameB | b@example.com | Title B | Short Abstract B | Supervisor B | sb@example.com
14.01.2020 | FirstnameC | LastnameC | c@example.com | Title C | Short Abstract C | Supervisor C | sc@example.com
           | FirstnameD | LastnameD | d@example.com |         |                  |              | 
21.01.2020 |            |           |               |         |                  |              | 

The above above example holds five entries for three sessions

1.  The first session takes place on 07.01.2020 with two talks from A and B. Mails will be send to A, B, C, D, Supvervisor A, and Supvervisor B.
2.  The second session takes place on 14.01.2020 with one talk from C. Mails will be send to A, B, C, D, and Supvervisor C.
3.  The third session takes place on 21.01.2020. There are no talks on this day. Mails will be send to A, B, C, and D informing them that the Journal Club does not take place.

Entry D does not have a talk attached. D will not appear in the schedule, however D will receive all mails.


## Template configuration

All mails are personalized. This means they are addressed to one specific person. The following jinja2 short codes can be used in all templates, except the admin template:

`{{ student_firstname|escape }}` is replaced with the recipient's first name.

`{{ student_lastname|escape }}` is replaced with the recipient's last name.

`{{ supervisor_name|escape }}` is replaced with the recipient's supervisor name.

`{{ talk[]|escape }}` lists the recipient's talk as python list in the format from `config/talks.csv` (date, first name, last name, mail, ...): i.e. `{{ talk[0]|escape }}` will be replaced with the date of the student's talk.

`{{ seminar_name|escape }}` will be replaced with the seminar name.

`{{ schedule|escape }}` will be replaced with the schedule of all upcoming talks.

`{{ talk_list[[]]|escape }}` holds a python list of all talks identified as important for that template. If this is used in the template `pre-1`, than important refers to all talks, which will take place tomorrow. One talk is a python list in the same format as `config/talks.csv` (date, first name, last name, mail, ...): i.e. `{{ talk[0]|escape }}` will be replaced with the date of the talk. 


The following jinja2 short codes can be used in the admin template:

`{{ seminar_name|escape }}` will be replaced with the seminar name.

`{{ problem_list[]|escape }}` lists all errors as python list.
