#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of seminar-notifier.
seminar-notifier is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
seminar-notifier is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with seminar-notifier.    If not, see <http://www.gnu.org/licenses/>.
"""

# (c) Simon Reich 2018

######################################################



# Folder for config files
folderConfig = "/home/sreich/git/seminar-notifier/config"

# Folder for templates
folderTemplate = "/home/sreich/git/seminar-notifier/templates"

# Sendmail binary
sendmail = "/usr/bin/sendmail"



######################################################
## No Configuration after this
######################################################



from yaml import load
from jinja2 import Template
import csv
from datetime import datetime
from email.mime.text import MIMEText
from subprocess import Popen, PIPE



def computeSchedule (talks):
    schedule = ""
    for talk in talks:
        if talk[-1] <= 0:
            schedule += str(talk[0]) + " " + str(talk[1]) + " " + str(talk[2]) + "\n"
    return schedule



def composeMail (template, talkReminder, talks, seminarname):
    mails = [[0 for x in range(0)] for x in range(0)]
    schedule = computeSchedule (talks)
    for talk in talks:
        mailtext = Template(template)
        mailtext = mailtext.render(talk_list=talkReminder, mail_firstname=talk[1], mail_lastname=talk[2], seminar_name=seminarname, schedule=schedule)
        mail = [talk[3], mailtext]
        mails.append(mail)
    return mails



def sendMail (mails, mailcopy, subject):
    msg = MIMEText("Here is the body of my message")
    msg["From"] = "me@example.com"
    msg["To"] = "you@example.com"
    msg["Subject"] = "This is the subject."
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(msg.as_string())

    return



def main():
    # This holds every error and is sent to the admin
    error = []


    # read config.yaml
    with open(folderConfig + "/config.yaml", 'r') as stream:
        config = load(stream)

    configActive = False
    try:
        configActive = config["active"]
    except:
        error.append("No \"active\" field in " + folderConfig + "/config.yaml")
        
    configStudentPre = []
    try:
        configStudentPre = config["student-pre"]
    except:
        error.append("No \"student-pre\" field in " + folderConfig + "/config.yaml")

    configStudentPost = []
    try:
        configStudentPost = config["student-post"]
    except:
        error.append("No \"student-post\" field in " + folderConfig + "/config.yaml")

    configSupervisorPre = []
    try:
        configSupervisorPre = config["supervisor-pre"]
    except:
        error.append("No \"supervisor-pre\" field in " + folderConfig + "/config.yaml")

    configSupervisorPost = []
    try:
        configSupervisor = config["supervisor-post"]
    except:
        error.append("No \"supervisor-post\" field in " + folderConfig + "/config.yaml")

    configSeminarname = ""
    try:
        configSeminarname = config["seminarname"]
    except:
        error.append("No \"seminarname\" field in " + folderConfig + "/config.yaml")

    configMailsubject = ""
    try:
        configMailsubject = config["mailsubject"]
    except:
        error.append("No \"mailsubject\" field in " + folderConfig + "/config.yaml")

    configMailcopy = []
    try:
        configMailcopy = config["mailcopy"]
    except:
        error.append("No \"mailcopy\" field in " + folderConfig + "/config.yaml")

    configMailadmin = []
    try:
        configMailadmin = config["mailadmin"]
    except:
        error.append("No \"mailadmin\" field in " + folderConfig + "/config.yaml")


    # Read templates
    templateStudentPre = []
    for preN in configStudentPre:
        if isinstance(preN, (int)) and int(preN) >=0:
            try:
                f = open(folderTemplate + "/student-pre-" + str(preN) + ".txt.jinja", "r")
                templateStudentPre.append(f.read())
            except:
                error.append("Could not open template " + folderTemplate + "/student-pre-" + str(preN) + ".txt.jinja")

    templateStudentPost = []
    for postN in configStudentPost:
        if isinstance(postN, (int)) and int(postN) >=0:
            try:
                f = open(folderTemplate + "/student-post-" + str(postN) + ".txt.jinja", "r")
                templateStudentPost.append(f.read())
            except:
                error.append("Could not open template " + folderTemplate + "/student-post-" + str(postN) + ".txt.jinja")

    templateSupervisorPre = []
    for supervisorN in configSupervisorPre:
        if isinstance(supervisorN, (int)) and int(supervisorN) >=0:
            try:
                f = open(folderTemplate + "/supervisor-pre-" + str(supervisorN) + ".txt.jinja", "r")
                templateSupervisorPre.append(f.read())
            except:
                error.append("Could not open template " + folderTemplate + "/supervisor-pre-" + str(supervisorN) + ".txt.jinja")

    templateSupervisorPost = []
    for supervisorN in configSupervisorPost:
        if isinstance(supervisorN, (int)) and int(supervisorN) >=0:
            try:
                f = open(folderTemplate + "/supervisor-post-" + str(supervisorN) + ".txt.jinja", "r")
                templateSupervisorPost.append(f.read())
            except:
                error.append("Could not open template " + folderTemplate + "/supervisor-post-" + str(supervisorN) + ".txt.jinja")

    templateAdmin = []
    try:
        f = open(folderTemplate + "/admin.txt.jinja", "r")
        templateAdmin.append(f.read())
    except:
        error.append("Could not open template " + folderTemplate + "/admin.txt.jinja")


    # Read talk list
    talks = [[0 for x in range(0)] for x in range(0)]
    try:
        with open(folderConfig + "/talks.csv") as f:
            csv_reader = csv.reader(f, delimiter=',')
            c = 0
            for row in csv_reader:
                if c > 0:
                    talks.append(row)
                c += 1
    except:
        error.append("Could not read talk list " + folderConfig + "/talks.csv")


    # Append how many days are left until talk to talk list
    dateToday = datetime.today()
    for talk in talks:
        try:
            dateTalk = datetime.strptime(talk[0], '%d.%m.%Y')
        except:
            error.append("Date for talk " + str(row[1]) + " " + str(row[2]) + " is " + str(row[0]) + " and should be in the format 20.01.2000 (%d.%m.%Y).")

        # dateDiff < 0 means days prior talk, > 0 means days after talk
        dateDiff = (dateToday-dateTalk).days
        talk.append(dateDiff)


    # Check, if dateDiff is in student-pre
    talkList = [[0 for x in range(0)] for x in range(0)]
    c = 0
    for days in configStudentPre:
        for talk in talks:
            if talk[-1] == days:
                talkList.append(talk)

        # Compose mail
        mails = composeMail(templateStudentPre[c], talkList, talks, configSeminarname)
        # Send mail
        if configActive:
            sendMail(mails, configMailcopy)
        c += 1


    # Check, if dateDiff is in student-post
    talkList = [[0 for x in range(0)] for x in range(0)]
    c = 0
    for days in configStudentPost:
        for talk in talks:
            if talk[-1] == days:
                talkList.append(talk)

        # Compose mail
        mails = composeMail(templateStudentPre[c], talkList, talks, configSeminarname)
        # Send mail
        if configActive:
            sendMail(mails, configMailcopy)
        c += 1


    # Check, if dateDiff is in supervisor-pre
    talkList = [[0 for x in range(0)] for x in range(0)]
    c = 0
    for days in configSupervisorPre:
        for talk in talks:
            if talk[-1] == days:
                talkList.append(talk)

        # Compose mail
        mails = composeMail(templateStudentPre[c], talkList, talks, configSeminarname)
        # Send mail
        if configActive:
            sendMail(mails, configMailcopy)
        c += 1


    # Check, if dateDiff is in supervisor-post
    talkList = [[0 for x in range(0)] for x in range(0)]
    c = 0
    for days in configSupervisorPost:
        for talk in talks:
            if talk[-1] == days:
                talkList.append(talk)

        # Compose mail
        mails = composeMail(templateStudentPre[c], talkList, talks, configSeminarname)
        # Send mail
        if configActive:
            sendMail(mails, configMailcopy)
        c += 1


        

#
#        # Check, if dateDiff is in student-post
#        if dateDiff in configStudentPost:
#            talkStudentPost.append(talk)
#
#        # Check, if dateDiff is in supervisor-pre
#        if (dateDiff * -1) in configSupervisorPre:
#            talkSupervisorPre.append(talk)

#        # Check, if dateDiff is in supervisor-post
#        if dateDiff in configSupervisorPost:
#            talkSupervisorPost.append(talk)
#
#        for StudentPreN in configStudentPre:
#            if isinstance(preN, (int)) and int(preN) >=0:


        # Mail composet

    print(talks)
    #print(error)




if __name__ == "__main__":
     main()
