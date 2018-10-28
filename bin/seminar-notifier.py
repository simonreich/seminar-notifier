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
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with seminar-notifier.  If not, see <http://www.gnu.org/licenses/>.
"""

# (c) Simon Reich 2018

######################################################



# Folder for config files
folderConfig = "/home/simon/git/seminar-notifier/config"

# Folder for templates
folderTemplate = "/home/simon/git/seminar-notifier/templates"

# Sendmail binary
sendmail = "/usr/bin/sendmail"



######################################################
## No Configuration after this
######################################################



from yaml import load
from jinja2 import Template
import csv
from datetime import datetime



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
    
  configPre = []
  try:
    configPre = config["pre"]
  except:
    error.append("No \"pre\" field in " + folderConfig + "/config.yaml")

  configPost = []
  try:
    configPost = config["post"]
  except:
    error.append("No \"post\" field in " + folderConfig + "/config.yaml")

  configSupervisor = []
  try:
    configSupervisor = config["supervisor"]
  except:
    error.append("No \"supervisor\" field in " + folderConfig + "/config.yaml")

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
  templatePre = []
  for preN in configPre:
    if isinstance(preN, (int)) and int(preN) >=0:
      try:
        f = open(folderTemplate + "/pre-" + str(preN) + ".txt.jinja", "r")
        templatePre.append(f)
      except:
        error.append("Could not open template " + folderTemplate + "/pre-" + str(preN) + ".txt.jinja")

  templatePost = []
  for postN in configPost:
    if isinstance(postN, (int)) and int(postN) >=0:
      try:
        f = open(folderTemplate + "/post-" + str(postN) + ".txt.jinja", "r")
        templatePost.append(f)
      except:
        error.append("Could not open template " + folderTemplate + "/post-" + str(postN) + ".txt.jinja")

  templateSupervisor = []
  for supervisorN in configSupervisor:
    if isinstance(supervisorN, (int)) and int(supervisorN) >=0:
      try:
        f = open(folderTemplate + "/supervisor-" + str(supervisorN) + ".txt.jinja", "r")
        templateSupervisor.append(f)
      except:
        error.append("Could not open template " + folderTemplate + "/supervisor-" + str(supervisorN) + ".txt.jinja")

  templateAdmin = []
  try:
    f = open(folderTemplate + "/admin.txt.jinja", "r")
    templateAdmin.append(f)
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


  # Compose mails to students
  dateToday = datetime.today()
  for talk in talks:
    dateTalk = datetime.strptime(talk[0], '%d.%m.%Y')
    diff = (dateTalk-dateToday).days
    print (diff)
  #for preN in configPre:
  #  if isinstance(preN, (int)) and int(preN) >=0:

  print(talks)
  print(error)




if __name__ == "__main__":
   main()
