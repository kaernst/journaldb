# CS61 Labs 2d
# Kendall Ernst, Kevin Xue

## Overview
* This database allows users to interact register and login to interact with manuscripts. In doing so, it provides a medium for the publication of author manuscripts to given issues, and the control over unique systems by the three types of users: authors, editors, and reviewers.
** Authors: Authors are responsible for the submission of manuscripts within the system, and maintain the right to retract their manuscripts at will. 
** Editors: Editors are responsible for the progession of manuscripts throughout the system, and move these manuscripts from one state to another, assigning reviewers when necessary.
** Reviewers: Reviewers are responsible for providing feedback to manuscripts assigned to them by editors, and maintain the right to resign at any time.
* Through the implementation of the database in this way, authors, editors, and reviewers can interact within the same system without issue. Their changes are stored within the databases and cascade to all relevant tables. They are also able to view their corresponding statuses at any time.

## Implementation Notes
* For this database, authors, editors, and reviewers have access to the following commands:
** Authors: status, submit, retract, quit
** Editors: status, assign, reject, accept, typeset, schedule, publish, quit
** Reviewers: status, accept, reject, resign, quit
* All authors, editors, and reviewers are required to register with the database, at which time their usernames and passwords will be saved within the system.

## Runtime Notes
* For the system to work properly, submitted manuscripts may not have special characters within their names.
* In the login screen, User ID must be input as an integer.
* mystory.rtf is included as a a helper to be included when submitting a manuscript to the database. 

## Extra Credit
* NOTE: Access controls to enforce the limits described in the business rules on what a particular user can do have been implemented within this system. As such, when users log in, they will be prompted to enter a password, and registering users will be prompted to create a password. 


