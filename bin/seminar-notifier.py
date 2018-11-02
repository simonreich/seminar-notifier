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
            if (talk[1] != "") or (talk[2] != "") or (talk [3] != ""):
                schedule += str(talk[0]) + " " + str(talk[1]) + " " + str(talk[2]) + "\n"
    return schedule



def composeMailStudent (template, talkList, talks, seminarname):
    # If there is a date, but no first name, second name, and mail address, than this talk does not take place
    talkListClean = [[0 for x in range(0)] for x in range(0)]
    for talk in talkList:
        if (talk[1] != "") or (talk[2] != "") or (talk [3] != ""):
            talkListClean.append(talk)

    mails = [[0 for x in range(0)] for x in range(0)]
    schedule = computeSchedule (talks)
    for talk in talks:
        mailtext = Template(template)
        mailtext = mailtext.render(talk_list=talkListClean, student_firstname=talk[1], student_lastname=talk[2], seminar_name=seminarname, schedule=schedule, talk=talk, supervisor_name=talk[6])
        if (talk[3] != ""):
            mail = [talk[3], mailtext]
        mails.append(mail)
    return mails



def composeMailSupervisor (template, talk, talks, seminarname):
    schedule = computeSchedule (talks)
    mailtext = Template(template)
    mailtext = mailtext.render(student_firstname=talk[1], student_lastname=talk[2], seminar_name=seminarname, schedule=schedule, talk=talk, supervisor_name=talk[6])
    return [[talk[7], mailtext]]



def composeMailAdmin (template, errors, seminarname):
    mailtext = Template(template)
    mailtext = mailtext.render(problem_list=errors, seminar_name=seminarname)
    return mailtext



def sendMail (mails, mailcopy, subject, binSendmail):
    for mail in mails:
        bcc = ""
        c = len(mailcopy)
        for recipient in mailcopy:
            bcc += str(recipient)
            if c > 1:
                cc +=", "
            c -= 1
        msg = MIMEText(mail[1])
        msg["From"] = ""
        msg["To"] = mail[0]
        msg["BCC"] = bcc
        msg["Subject"] = subject
        #p = Popen([binSendmail, "-t", "-oi"], stdin=PIPE)
        #p.communicate(msg.as_string())
        print(msg.as_string())
    return



def sendMailAdmin (mailtext, mailAdmin, subject, binSendmail):
    for recipient in mailAdmin:
        bcc = ""
        c = len(mailAdmin)
        for recipient in mailAdmin:
            bcc += str(recipient)
            if c > 1:
                cc +=", "
            c -= 1
        msg = MIMEText(mailtext)
        msg["From"] = ""
        msg["To"] = ""
        msg["BCC"] = bcc
        msg["Subject"] = subject
        #p = Popen([binSendmail, "-t", "-oi"], stdin=PIPE)
        #p.communicate(msg.as_string())
        print(msg.as_string())
    return



def main():
    # This holds every error and is sent to the admin
    error = []

    # Sendmail binary
    configSendmail = "/usr/bin/sendmail"

    # read config.yaml
    with open(folderConfig + "/config.yaml", 'r') as stream:
        config = load(stream)

    configActive = False
    try:
        configActive = config["active"]
    except:
        error.append("No \"active\" field in " + folderConfig + "/config.yaml")
        
    configStudentEvent = []
    try:
        configStudentEvent = config["student-event"]
    except:
        error.append("No \"student-event\" field in " + folderConfig + "/config.yaml")
        
    configSupervisorEvent = []
    try:
        configSupervisorEvent = config["supervisor-event"]
    except:
        error.append("No \"supervisor-event\" field in " + folderConfig + "/config.yaml")
        
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
        configSupervisorPost = config["supervisor-post"]
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
    templateStudentEvent = []
    for eventN in configStudentEvent:
        try:
            datetime.strptime(eventN, '%d.%m.%Y')
            try:
                f = open(folderTemplate + "/student-event-" + str(eventN) + ".txt.jinja", "r")
                templateStudentEvent.append(f.read())
            except:
                error.append("Could not open template " + folderTemplate + "/student-event-" + str(eventN) + ".txt.jinja")
        except:
            error.append("Date in  \"student-event\" field in " + folderConfig + "/config.yaml has wrong format. Must be %d.%m.%Y, e.g. 14.01.2001.")

    templateSupervisorEvent = []
    for eventN in configSupervisorEvent:
        try:
            datetime.strptime(eventN, '%d.%m.%Y')
            try:
                f = open(folderTemplate + "/supervisor-event-" + str(eventN) + ".txt.jinja", "r")
                templateSupervisorEvent.append(f.read())
            except:
                error.append("Could not open template " + folderTemplate + "/supervisor-event-" + str(eventN) + ".txt.jinja")
        except:
            error.append("Date in  \"supervisor-event\" field in " + folderConfig + "/config.yaml has wrong format. Must be %d.%m.%Y, e.g. 14.01.2001.")

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

    templateAdmin = ""
    try:
        f = open(folderTemplate + "/admin.txt.jinja", "r")
        templateAdmin = f.read()
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


    # Check for errors
    # If present, send mail to admin and exit
    if len(error) > 0:
        mailtext = composeMailAdmin (templateAdmin, error, configSeminarname)
        sendMailAdmin (mailtext, configMailadmin, configMailsubject, configSendmail)
        exit(1)


    # Check for student events
    dateToday = datetime.today()
    c = 0
    for event in configStudentEvent:
        dateEvent = datetime.strptime(event, '%d.%m.%Y')
        if (dateToday - dateEvent).days == 0:
            # Compose mail
            mails = composeMailStudent(templateStudentEvent[c], talks, talks, configSeminarname)
            # Send mail
            if configActive:
                sendMail(mails, configMailcopy, configMailsubject, configSendmail)
        c += 1


    # Check for supervisor events
    dateToday = datetime.today()
    c = 0
    for event in configSupervisorEvent:
        dateEvent = datetime.strptime(event, '%d.%m.%Y')
        if (dateToday - dateEvent).days == 0:
            # Compose mail
            for talk in talks:
                mails = composeMailSupervisor(templateSupervisorEvent[c], talk, talks, configSeminarname)

                # Send mail
                if configActive:
                    sendMail(mails, configMailcopy, configMailsubject, configSendmail)
        c += 1


    # Check, if dateDiff is in student-pre
    c = 0
    for days in configStudentPre:
        talkList = [[0 for x in range(0)] for x in range(0)]
        for talk in talks:
            if talk[-1] == days*(-1):
                talkList.append(talk)

        # Compose mail
        if (len(talkList) > 0):
            mails = composeMailStudent(templateStudentPre[c], talkList, talks, configSeminarname)
            # Send mail
            if configActive:
                sendMail(mails, configMailcopy, configMailsubject, configSendmail)
        c += 1


    # Check, if dateDiff is in student-post
    c = 0
    for days in configStudentPost:
        talkList = [[0 for x in range(0)] for x in range(0)]
        for talk in talks:
            if talk[-1] == days:
                talkList.append(talk)

        # Compose mail
        if (len(talkList) > 0):
            mails = composeMailStudent(templateStudentPre[c], talkList, talks, configSeminarname)
            # Send mail
            if configActive:
                sendMail(mails, configMailcopy, configMailsubject, configSendmail)
        c += 1


    # Check, if dateDiff is in supervisor-pre
    c = 0
    for days in configSupervisorPre:
        talkList = [[0 for x in range(0)] for x in range(0)]
        for talk in talks:
            if talk[-1] == days*(-1):
                talkList.append(talk)

        # Compose mail
        if (len(talkList) > 0):
            for talk in talkList:
                mail = composeMailSupervisor(templateSupervisorPre[c], talk, talks, configSeminarname)
                # Send mail
                if configActive:
                    sendMail(mail, configMailcopy, configMailsubject, configSendmail)
        c += 1


    # Check, if dateDiff is in supervisor-post
    c = 0
    for days in configSupervisorPost:
        talkList = [[0 for x in range(0)] for x in range(0)]
        for talk in talks:
            if talk[-1] == days:
                talkList.append(talk)

        # Compose mail
        if (len(talkList) > 0):
            for talk in talkList:
                mail = composeMailSupervisor(templateSupervisorPost[c], talk, talks, configSeminarname)
                # Send mail
                if configActive:
                    sendMail(mail, configMailcopy, configMailsubject, configSendmail)
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

    #print(error)




if __name__ == "__main__":
     main()
