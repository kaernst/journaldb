from __future__ import print_function        # make print a function
import mysql.connector  # mysql functionality
import sys  # for misc errors
from datetime import datetime
import os
import random

SERVER = "sunapee.cs.dartmouth.edu"  # db server to connect to
USERNAME = "kernst"  # user to connect as
PASSWORD = "unc9XWpQ"  # user's password
DATABASE = "kernst_db"  # db to user

def runQuery(query):
    try:
        # initialize db connection
        con = mysql.connector.connect(host=SERVER, user=USERNAME, password=PASSWORD,
                                      database=DATABASE)

        # initialize a cursor
        cursor = con.cursor(buffered=True)

        # query db
        cursor.execute(query)

        # returns the results of the SQL query
        if query[0:6] == "INSERT" or query[0:6] == "UPDATE" or query[0:6] == "DELETE":
            con.commit()
            return cursor.lastrowid
        else :
            return (cursor.fetchall())
    except mysql.connector.Error as e:  # catch SQL errors
        print("SQL Error: {0}".format(e.msg))
    except:  # anything else
        print("Unexpected error: {0}".format(sys.exc_info()[0]))

    # cleanup
    con.close()
    cursor.close()


def register (personType, fName, lName, pWord, email = None, addr1 = None, addr2 = None,
              city = None, state = None, country = None, zip = None,
              affiliation = None, ric1 = None, ric2 = None, ric3 = None):
    if personType == "author":
        if (fName == None or lName == None or email == None or addr1 == None or
                    city == None or country == None or affiliation == None or pWord == None):
            print("Error: Please specify all of the following: first name, last name, "
                  "password, email, address, and affiliation.\n")
            return
        else:
            addressID = create_addr(addr1, city, country, addr2, state, zip)
            print("Address ID Returned: " + str(addressID))
            personID = register_author(fName, lName, pWord, email, affiliation, addressID)
            return personID
    if (personType == "editor"):
        if (fName == None or lName == None or pWord == None):
            print("Error: Please specify all of the following: first name, last name, password")
        personID = register_editor(fName, lName, pWord)
        return personID
    if (personType == "reviewer"):
        if (fName == None or lName == None or email == None or affiliation == None or pWord == None):
            print("Error: Please specify all of the following: first name, last name,"
                  " password, email, affiliation, and between one and three areas of interest")
        if (ric1 == None and ric2 == None and ric3 == None):
            print("Error: Please specify at least one area of interest code")
        ## Condition to make sure RICodes exist
        personID = register_reviewer (fName, lName, pWord, email, affiliation, ric1, ric2, ric3)
        return personID
    else:
        print("Error: You must register as an author, editor, or reviewer.\n")
        return


def create_addr (addr1, city, country, addr2 = None, state = None, zip = None) :
    if addr2 is None:
        addr2 = "NULL"
    if state is None:
        state = "NULL"
    if zip is None:
        zip = "NULL"
    q1 = ("INSERT INTO Address VALUES (DEFAULT, \'" + addr1 + "\', \'" + str(addr2) + "\', \'" +
          city + "\', \'" + state + "\', \'" + country + "\', " + str(zip) + ");")
    addressID = runQuery(q1)
    print("Address ID: " + str(addressID))
    return addressID


def register_author (fName, lName, pWord, email, affiliation, addressID) :
    q1 = ("INSERT INTO Person VALUES (DEFAULT, \'a\', \'" + fName + "\', \'" + lName + "\', \'" + pWord + "\');")
    personID = runQuery(q1)
    q2 = ("INSERT INTO Author VALUES (" + str(personID) + ", \'" + email + "\', \'" +
          affiliation + "\', " + str(addressID) + ");")
    runQuery(q2)
    return personID


def register_editor (fName, lName, pWord) :
    q1 = ("INSERT INTO Person VALUES (DEFAULT, \'e\', \'" + fName + "\', \'" + lName + "\', \'" + pWord + "\');")
    personID = runQuery(q1)
    q2 = ("INSERT INTO Editor VALUES (" + str(personID) + ");")
    runQuery(q2)
    return personID


def register_reviewer (fName, lName, pWord, email, affiliation, ric1, ric2 = None, ric3 = None) :
    q1 = ("INSERT INTO Person VALUES (DEFAULT, \'r\', \'" + fName + "\', \'" + lName + "\', \'" + pWord + "\');")
    personID = runQuery(q1)
    q2 = ("INSERT INTO Reviewer VALUES (" + str(personID) + ", \'" + email + "\', \'" +
          affiliation + "\');")
    runQuery(q2)
    map_ric_reviewer(personID, ric1)
    if (ric2 is not None) :
        map_ric_reviewer(personID, ric2)
    if (ric3 is not None) :
        map_ric_reviewer(personID, ric3)
    return personID


def map_ric_reviewer(personID, ric) :
    q1 = ("INSERT INTO RICode_Reviewer VALUES (" + str(ric) + ", " + str(personID) + ");")
    runQuery(q1)


def create_rics():
    q1 = "INSERT INTO RICodes(interest) VALUES (\'Agricultural engineering\'), (\'Biochemical engineering\'), " \
         "(\'Biomechanical engineering\'), (\'Ergonomics\'), (\'Food engineering\'), " \
         "(\'Bioprocess engineering\'), (\'Genetic engineering\'), (\'Human genetic engineering\'), " \
         "(\'Metabolic engineering\'), (\'Molecular engineering\'), (\'Neural engineering\'), " \
         "(\'Protein engineering\'), (\'Rehabilitation engineering\'), (\'Tissue engineering\'), " \
         "(\'Aquatic and environmental engineering\'), (\'Architectural engineering\'), (\'Civionic engineering\'), " \
         "(\'Construction engineering\'), (\'Earthquake engineering\'), (\'Earth systems engineering and management\'), " \
         "(\'Ecological engineering\'), (\'Environmental engineering\'), (\'Geomatics engineering\'), " \
         "(\'Geotechnical engineering\'), (\'Highway engineering\'), (\'Hydraulic engineering\'), " \
         "(\'Landscape engineering\'), (\'Land development engineering\'), (\'Pavement engineering\'), " \
         "(\'Railway systems engineering\'), (\'River engineering\'), (\'Sanitary engineering\'), (\'Sewage engineering\'), " \
         "(\'Structural engineering\'), (\'Surveying\'), (\'Traffic engineering\'), (\'Transportation engineering\'), " \
         "(\'Urban engineering\'), (\'Irrigation and agriculture engineering\'), (\'Explosives engineering\')," \
         "(\'Biomolecular engineering\'), (\'Ceramics engineering\'), (\'Broadcast engineering\'), " \
         "(\'Building engineering\'), (\'Signal Processing\'), (\'Computer engineering\'), (\'Power systems engineering\')," \
         "(\'Control engineering\'), (\'Telecommunications engineering\'), (\'Electronic engineering\'), " \
         "(\'Instrumentation engineering\'), (\'Network engineering\'), (\'Neuromorphic engineering\'), " \
         "(\'Engineering Technology\'), (\'Integrated engineering\'), (\'Value engineering\'), (\'Cost engineering\'), " \
         "(\'Fire protection engineering\'), (\'Domain engineering\'), (\'Engineering economics\'), " \
         "(\'Engineering management\'), (\'Engineering psychology\'), (\'Ergonomics\'), (\'Facilities Engineering\'), " \
         "(\'Logistic engineering\'), (\'Model-driven engineering\'), (\'Performance engineering\'), " \
         "(\'Process engineering\'), (\'Product Family Engineering\'), (\'Quality engineering\'), " \
         "(\'Reliability engineering\'), (\'Safety engineering\'), (\'Security engineering\'), (\'Support engineering\'), " \
         "(\'Systems engineering\'), (\'Metallurgical Engineering\'), (\'Surface Engineering\'), " \
         "(\'Biomaterials Engineering\'), (\'Crystal Engineering\'), (\'Amorphous Metals\'), (\'Metal Forming\')," \
         "(\'Ceramic Engineering\'), (\'Plastics Engineering\'), (\'Forensic Materials Engineering\'), " \
         "(\'Composite Materials\'), (\'Casting\'), (\'Electronic Materials\'), (\'Nano materials\'), " \
         "(\'Corrosion Engineering\'), (\'Vitreous Materials\'), (\'Welding\'), (\'Acoustical engineering\')," \
         "(\'Aerospace engineering\'), (\'Audio engineering\'), (\'Automotive engineering\'), " \
         "(\'Building services engineering\'), (\'Earthquake engineering\'), (\'Forensic engineering\'), " \
         "(\'Marine engineering\'), (\'Mechatronics\'), (\'Nanoengineering\'), (\'Naval architecture\'), (\'Sports engineering\'), " \
         "(\'Structural engineering\'), (\'Vacuum engineering\'), (\'Military engineering\'), " \
         "(\'Combat engineering\'), (\'Offshore engineering\'), (\'Optical engineering\'), (\'Geophysical engineering\')," \
         "(\'Mineral engineering\'), (\'Mining engineering\'), (\'Reservoir engineering\'), (\'Climate engineering\')," \
         "(\'Computer-aided engineering\'), (\'Cryptographic engineering\'), (\'Information engineering\'), " \
         "(\'Knowledge engineering\'), (\'Language engineering\'), (\'Release engineering\'), (\'Teletraffic engineering\')," \
         "(\'Usability engineering\'), (\'Web engineering\'), (\'Systems engineering\');"
    runQuery(q1)


#program returns an integer that corresponds to user type. Integers as follows: 0 - invalid username, 1 - author, 2 - editor, 3 - reviewer
def getUserType(userID):
    userType = runQuery("SELECT personType FROM Person WHERE Person.personID = " + str(userID))

    #return 0 if user is not found
    if userType == []:
        return 0 #userType is a required field
    return userType[0][0]

#handles login for all usertypes and prints greeting and relevant messages
def login(userID, userType):
    print ("Welcome to the Journal of E-commerce Research Knowledge!")
    userName = runQuery("SELECT fName FROM Person where Person.personID = " + str(userID))[0][0], runQuery("SELECT lName FROM Person where Person.personID = " + str(userID))[0][0]

    #handle authors
    if userType == "a":
        print ("Author: " + userName[0] + " " + userName[1])
        print("Current status: \n" + authorEditorStatus(userID, userType) + "\n")

    #handle editors
    elif userType == "e":
        print ("Editor: " + userName[0] + " " + userName[1])
        print("Current status: \n" + authorEditorStatus(userID, userType) + "\n")

    #handle reviewers
    elif userType == "r":
        print ("Reviewer: " + userName[0] + " " + userName[1])
        print("Assigned manuscripts: " + reviewerStatus(userID) + "\n")

# status command for use by Authors and Editors
# returns a string of the number of relevant manuscripts at each stage of process
def authorEditorStatus(userID, userType):

    statusString = ""
    if userType == "a":
        statusString = statusString + "Manuscripts submitted: " + ', '.join(getAuthorManuscripts(userID, 0)) + "\n"
        statusString = statusString + "Manuscripts rejected: " + ', '.join(getAuthorManuscripts(userID, 1)) + "\n"
        statusString = statusString + "Manuscripts under review: " + ', '.join(
            getAuthorManuscripts(userID, 2)) + "\n"
        statusString = statusString + "Manuscripts accepted: " + ', '.join(getAuthorManuscripts(userID, 3)) + "\n"
        statusString = statusString + "Manuscripts in typesetting: " + ', '.join(
            getAuthorManuscripts(userID, 4)) + "\n"
        statusString = statusString + "Manuscripts scheduled for publication: " + ''.join(
            getAuthorManuscripts(userID, 5)) + "\n"
        statusString = statusString + "Manuscripts published: " + ', '.join(getAuthorManuscripts(userID, 6))

    elif userType == "e":
        statusString = statusString + "Manuscripts submitted: " + ', '.join(getEditorManuscripts(userID, 0)) + "\n"
        statusString = statusString + "Manuscripts rejected: " + ', '.join(getEditorManuscripts(userID, 1)) + "\n"
        statusString = statusString + "Manuscripts under review: " + ', '.join(
            getEditorManuscripts(userID, 2)) + "\n"
        statusString = statusString + "Manuscripts accepted: " + ', '.join(getEditorManuscripts(userID, 3)) + "\n"
        statusString = statusString + "Manuscripts in typesetting: " + ', '.join(
            getEditorManuscripts(userID, 4)) + "\n"
        statusString = statusString + "Manuscripts scheduled for publication: " + ', '.join(
            getEditorManuscripts(userID, 5)) + "\n"
        statusString = statusString + "Manuscripts published: " + ', '.join(getEditorManuscripts(userID, 6))
    return statusString


def getAuthorManuscripts(userID, statusID):
    manuscriptIDs = runQuery("SELECT manuscriptID FROM Manuscript WHERE primaryAuthorID = " + str(
        userID) + " AND statusID = " + str(statusID) + " ORDER BY manuscriptID")

    if manuscriptIDs is None:
        return "None"

    for i in range(0, len(manuscriptIDs)):
        manuscriptName = \
        runQuery("SELECT title FROM Manuscript WHERE Manuscript.manuscriptID = " + str(manuscriptIDs[i][0]) + ";")[
            0][0]
        manuscriptIDs[i] = str(manuscriptIDs[i][0]) + ": " + manuscriptName

    return manuscriptIDs

def getEditorManuscripts(userID, statusID):
    manuscriptIDs = runQuery("SELECT manuscriptID FROM Manuscript WHERE editorID = " + str(
        userID) + " AND statusID = " + str(statusID) + " ORDER BY manuscriptID")

    if manuscriptIDs is None:
        return "None"

    for i in range(0, len(manuscriptIDs)):
        manuscriptName = \
        runQuery("SELECT title FROM Manuscript WHERE Manuscript.manuscriptID = " + str(manuscriptIDs[i][0]) + ";")[
            0][0]
        manuscriptIDs[i] = str(manuscriptIDs[i][0]) + ": " + manuscriptName

    return manuscriptIDs


#status command for use by Reviewer
#returns a string of the manuscript ids and correspond manuscript titles relevant for the reviewer
def reviewerStatus(userID):
    reviewerPaperIDs = getReviewerManuscripts(userID)
    setUnderReview = identifyUnderReview(reviewerPaperIDs)

    reviewerStatusString = ""
    for i in range(0, len(reviewerPaperIDs)):
        if i == len(reviewerPaperIDs) - 1:
            reviewerStatusString = reviewerStatusString + str(reviewerPaperIDs[i]) + ": " + runQuery(
                "SELECT title FROM Manuscript WHERE Manuscript.manuscriptID = " + str(reviewerPaperIDs[i]) + ";")[0][0]
        else:
            reviewerStatusString = reviewerStatusString + str(reviewerPaperIDs[i]) + ": " + runQuery(
                "SELECT title FROM Manuscript WHERE Manuscript.manuscriptID = " + str(reviewerPaperIDs[i]) + ";")[0][0] + ", "

    reviewerStatusString = reviewerStatusString + "\nManuscript IDs currently under review: "
    for j in range(0, len(setUnderReview)):
        if j == len(setUnderReview) - 1:
            reviewerStatusString = reviewerStatusString + str(setUnderReview[j])
        else:
            reviewerStatusString = reviewerStatusString + str(setUnderReview[j]) + ", "

    return reviewerStatusString

#returns list of manuscript IDs associated with author, editor, reviewer
def getReviewerManuscripts(userID):
    paperIDs = runQuery("SELECT manuscriptID FROM Feedback WHERE Feedback.personID = " + str(userID) + ";")

    #reformat paperIDs to remove extra commas
    for i in range(0, len(paperIDs)):
        paperIDs[i] = paperIDs[i][0]

    return paperIDs

#returns a subset of paperIDs whose status is under review
def identifyUnderReview(paperIDs):
    allUnderReview = runQuery("Select manuscriptID FROM Manuscript WHERE Manuscript.statusID = 2")
    setUnderReview = []

    #reformat paperIDs to remove extra commas
    for i in range(0, len(allUnderReview)):
        allUnderReview[i] = allUnderReview[i][0]

    for j in range(0, len(paperIDs)):
        if paperIDs[j] in allUnderReview:
            setUnderReview.append(paperIDs[j])

    return setUnderReview

def read_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            blob = f.read()
            return blob
    else:
        return None

def handle_submit():
    print("Please provide the following information regarding your manuscript.")
    title = raw_input("Title: ")
    while (title == ""):
        title = raw_input("This is a required input. Please enter a title: ")
    affiliation = raw_input("Affiliated institution: ")
    while (affiliation == ""):
        affiliation = raw_input("This is a required input. Please enter an affiliation: ")
    ric = raw_input("Area of interest code: ")
    ## HANDLE NON-INTEGER INPUT
    while (ric == "" or int(ric) < 1 or int(ric) > 124):
        ric = raw_input("Invalid code. Please enter a code between 1 and 124: ")
    author2 = raw_input("Please enter the name of the first coauthor (enter if none): ")
    if (author2 == ""):
        author2 = None
        author3 = None
        author4 = None
    else:
        author3 = raw_input("Please enter the name of the second coauthor (enter if none): ")
        if (author3 == ""):
            author3 = None
            author4 = None
        else:
            author4 = raw_input("Please enter the name of the fourth coauthor (enter if none): ")
            if (author4 == ""):
                author4 = None
    fileName = raw_input("Please enter the name of your file to upload: ")
    file = read_file(fileName)
    while (file is None):
        fileName = raw_input("Invalid file. Please enter the name of your file to upload: ")
        file = read_file(fileName)
    inputArray = [title, affiliation, int(ric), author2, author3, author4, file]
    return inputArray

#handles the following author queries: status, submit, quit
def authorQuery(userID):
    userInput = raw_input("Query: ")
    inputArray = userInput.split()

    if inputArray[0] == "status":
        print("Current status: \n" + authorEditorStatus(userID, "a") + "\n")
    elif inputArray[0] == "submit":
        manuInputs = handle_submit()
        print("INPUTS: " + str(manuInputs))
        authorSubmit(userID, manuInputs)
    elif inputArray[0] == "retract":
        manuID = inputArray[1]
        retract_manuscript(userID, manuID)
    elif inputArray[0] == "quit":
        return False
    else:
        print("Invalid input.")
        printAuthorInstructions()

#handles the following reviewer queries: status, accept, reject
def reviewerQuery(userID):
    userInput = raw_input("Query: ")
    inputArray = userInput.split()

    if inputArray[0] == "status":
        print("Assigned manuscripts: " + reviewerStatus(userID) + "\n")
    elif inputArray[0] == "accept" or inputArray[0] == "reject":
        reviewerFeedback(userID, inputArray)
    elif inputArray[0] == "resign":
        reviewerResign(userID)
        return False
    elif inputArray[0] == "quit":
        return False
    else:
        print("Invalid input.")
        printReviewerInstructions()

#handles the following editor queries: status, assign, reject, accept, typeset, schedule, publish
def editorQuery(userID):
    userInput = raw_input("Query: ")
    inputArray = userInput.split()

    if inputArray[0] == "status":
        print("Current status: \n" + authorEditorStatus(userID, "e") + "\n")
    elif inputArray[0] == "assign":
        manuID = inputArray[1]
        reviewerID = inputArray[2]
        assign_manuscript(manuID, reviewerID)
    elif inputArray[0] == "reject":
        manuID = inputArray[1]
        reject_manuscript(manuID)
    elif inputArray[0] == "accept":
        manuID = inputArray[1]
        acceptManuscript(manuID)
    elif inputArray[0] == "typeset":
        manuID = inputArray[1]
        pp = inputArray[2]
        typesetManuscript(manuID, pp)
    elif inputArray[0] == "schedule":
        manuID = inputArray[1]
        pubYear = inputArray[2]
        pubPeriod = inputArray[3]
        scheduleManuscript(manuID, pubYear, pubPeriod)
    elif inputArray[0] == "publish":
        manuID = inputArray[1]
        publishManuscript(manuID)
    elif inputArray[0] == "quit":
        return False
    else:
        print("Invalid input.")
        printEditorInstructions()

def printAuthorInstructions():
    print("Available queries:")
    print("'status': View the number of manuscripts you have at each stage of publication process")
    print("'submit': Submit a manuscript")
    print("'retract': Retract a manuscript by following the format: 'retract <manuscriptID>'")
    print("'quit': Exit the database")

def printReviewerInstructions():
    print("Available queries:")
    print("'status': View the manuscripts assigned to you and those which are currently under review")
    print("'accept': Accept a manuscript by following the format: 'accept <manuscriptID> <appropriateness (1-10)> <clarity (1-10)> "
          "<methodology (1-10)> <contribution (1-10)>")
    print("'reject': Reject a manuscript by following the format: 'reject <manuscriptID> <appropriateness (1-10)> <clarity (1-10)> "
          "<methodology (1-10)> <contribution (1-10)>")
    print("'resign': Resign as a reviewer")
    print("'quit': Exit the database")

def printEditorInstructions():
    print("Available queries:")
    print("'status': View the number of manuscripts you have at each stage of publication process")
    print("'assign': Assign manuscripts to reviewers by following the format: 'assign <manu#> <reviewer id>")
    print("'reject': Reject a manuscript by following the format: 'reject <manu#>'")
    print("'accept': Accept a manuscript by following the format: 'accept <manu#>'")
    print("'typeset': set a manuscript's status to 'typeset' by following the format: 'typeset <manu#> <pp>'")
    print("'schedule': schedule a manuscript by following the format: 'schedule <manu#> <pubYear> <pubPeriod>'")
    print("'publish': send a manuscript to be printed by following the format: publish <pubYear> <pubPeriod>")
    print("'quit': Exit the database")


# inserts reviewer feedback as defined by the reviewer query
def reviewerFeedback(userID, inputArray):
    reviewerPaperIDs = getReviewerManuscripts(userID)
    setUnderReview = identifyUnderReview(reviewerPaperIDs)

    # determine whether the review has decided to accept or reject the manuscript
    # 1 = accept, 0 = reject
    accept = 1
    if inputArray[0] == "reject":
        accept = 0

    # verify the number of inputs
    if len(inputArray) != 6:
        print("Error: Invalid number of inputs.")
        return

    for i in range(1, len(inputArray)):

        # make sure all inputs besides accept/reject are integers
        if isinstance(inputArray[i] , int):
            print("Error: Please make sure input " + str(i + 1) + " must be an integer.")
            return

        # check that all reviewer scores are between 1 and 10
        if i > 1:
            if int(inputArray[i]) < 1 or int(inputArray[i]) > 10:
                print("Error: All review scores must be between 1 and 10.")
                return

        # check manuscriptID to verify that the reviewer is responsible for that manuscript and that
        # the manuscript is under review
        if i == 1:
            if (int(inputArray[i]) not in reviewerPaperIDs):
                print("Error: Please review manuscript ID.")
                return

            if (int(inputArray[i]) not in setUnderReview):
                print("Error: This paper is not under review.")
                return

    manuID = inputArray[1]
    appropriateness = inputArray[2]
    clarity = inputArray[3]
    methodology = inputArray[4]
    contribution = inputArray[5]
    feedbackSentDate = datetime.now().strftime('%Y-%m-%d')
    print("DATE: " + str(feedbackSentDate))
    q1 = "UPDATE Feedback SET appropriateness = " + appropriateness + ", clarity = " + clarity + ", methodology = " + methodology + \
         ", contribution = " + contribution + ", recommendation = " + str(accept) + ", feedbackSentDate = \'" + str(feedbackSentDate) + \
        "\' WHERE Feedback.manuscriptID = " + str(manuID) + " AND Feedback.personID = " + str(userID) + ";"

    runQuery(q1)

#inserts author submission into database
def authorSubmit(userID, inputArray):

    # make sure the input array includes all 8 entries
    if len(inputArray) != 7:
        print("Error: Invalid number of inputs.")
        return

    title = inputArray[0]
    affiliation = inputArray[1]
    ric = inputArray[2]
    author2Name = inputArray[3]
    author3Name = inputArray[4]
    author4Name = inputArray[5]
    fileName = inputArray[6]
    pAuthor = userID
    dateReceived = datetime.now().strftime('%Y-%m-%d')
    # maxEditor = runQuery("SELECT MAX(personID) FROM Editor;")[0][0][0]
    maxEditor = runQuery("SELECT MAX(personID) FROM Editor;")
    maxEditor = maxEditor[0][0]
    if (maxEditor is not None):
        editorID = choose_editor(maxEditor)
    else:
        print("Error: There are no available editors. Please submit at a later date.")
        return

    # does this check work? I think Python throws an error for no index before you reach this point?
    if title is None or affiliation is None or ric is None or fileName is None:
        print("Error: Please specify a title, affiliation, area of interest, and fileName")
        return

    print("EDITOR ID: " + str(editorID))
    q1 = "INSERT INTO Manuscript VALUES (DEFAULT, \'" + title + "\', \'" + affiliation + "\', \'" + dateReceived + \
         "\', 0, NULL, \'" + fileName + "\', " + str(editorID) + ", " + str(pAuthor) + ", " + \
         str(ric) + ");"
    manuID = runQuery(q1)

    if author2Name is not None:
        author2 = create_coauthor(author2Name, manuID, 2)

    if author3Name is not None:
        author3 = create_coauthor(author3Name, manuID, 3)

    if author4Name is not None:
        author4 = create_coauthor(author4Name, manuID, 4)

def choose_editor(maxEditor):
    editors = []
    for i in range(0,maxEditor+1,1):
        q1 = "SELECT * FROM Editor WHERE personID = " + str(i) + ";"
        if (runQuery(q1) != []):
            editors.append(i)
    editorID = random.choice(editors)
    return editorID

def create_coauthor(name, manuID, orderID):
    q1 = "INSERT INTO Coauthor VALUES (DEFAULT, \'" + name + "\');"
    coauthorID = runQuery(q1)
    q2 = "INSERT INTO Coauthor_Manuscript VALUES (" + str(coauthorID) + ", " + \
         str(manuID) + ", " + str(orderID) + ");"
    runQuery(q2)
    return coauthorID

def getSpecificReviewerRICs(reviewerID):
    reviewerRICS = runQuery("SELECT ric FROM RICode_Reviewer WHERE personID = " + str(reviewerID) + ";")

    for i in range(0, len(reviewerRICS)):
        reviewerRICS[i] = reviewerRICS[i][0]

    return reviewerRICS

def assign_manuscript(manuID, reviewerID):
    ## Catch bad manuID or reviewerID
    q4 = "SELECT MAX(manuscriptID) FROM Manuscript"
    numManus = runQuery(q4)[0][0]
    if int(manuID) > int(numManus):
        print("Invalid manuscript.")
        return
    if getManuscriptStatus(manuID) > 2 or getManuscriptStatus(manuID) == 1:
        print("Cannot assign reviewer to a manuscript that has been rejected or has already been accepted.")
        return
    q5 = "SELECT personID FROM Reviewer WHERE personID = " + str(reviewerID) + ";"
    isRev = runQuery(q5)
    if (isRev == None or len(isRev) is 0):
        print("Invalid reviewer.")
        return

    ## Check reviewer Ric = manuscript ric
    revRICS = getSpecificReviewerRICs(reviewerID)
    q6 = "SELECT ric FROM Manuscript WHERE manuscriptID = " + str(manuID) + ";"
    manuRIC = runQuery(q6)[0][0]
    if manuRIC not in revRICS:
        print("Please assign manuscript to a reviewer with the same area of interest code.")
        return

    reviewerAssignedDate = datetime.now().strftime('%Y-%m-%d')
    q1 = "INSERT INTO Feedback VALUES (" + str(manuID) + ", " + \
         str(reviewerID) + ", NULL, NULL, NULL, NULL, NULL, \'" + \
         str(reviewerAssignedDate) + "\', NULL);"
    runQuery(q1)
    q2 = "UPDATE Manuscript SET statusID = 2 WHERE manuscriptID = " + str(manuID) + ";"
    runQuery(q2)
    q3 = "UPDATE Manuscript SET statusDate = \'" + \
         reviewerAssignedDate + "\' WHERE manuscriptID = " + str(manuID) + ";"
    runQuery(q3)

#changes manuscript status to accepted
def acceptManuscript(manuID):

    #validate that at least 3 have completed their reviews
    q1 = "SELECT count(personID) FROM Feedback WHERE manuscriptID = " + str(
        manuID) + " AND feedbackSentDate IS NOT NULL;"
    numReviews = runQuery(q1)[0][0]
    if (numReviews < 3):
        print("Error: Manuscript must receive feedback from at least three reviewers before acceptance")
        return

    #validate that the manuscript is currently under review
    manuStatus = getManuscriptStatus(manuID)
    if (manuStatus != 2):
        print("Error: Manuscript must be under review to be accepted")
        return

    acceptDate = datetime.now().strftime('%Y-%m-%d')
    q2 = "UPDATE Manuscript SET statusID = 3, statusDate = \'" + str(acceptDate) + "\' WHERE manuscriptID = " + str(manuID)
    updateConfirm = runQuery(q2)

    # why does date insert as 0s???
    q3 = "INSERT INTO Accepted VALUES (" + str(manuID) + ", \'" + str(acceptDate) + "\', NULL, NULL, NULL, NULL, NULL);"
    insertConfirm = runQuery(q3)

def reject_manuscript(manuID):
    rejectDate = datetime.now().strftime('%Y-%m-%d')
    q1 = "UPDATE Manuscript SET statusID = 1 WHERE manuscriptID = " + str(manuID) + ";"
    runQuery(q1)
    q2 = "UPDATE Manuscript SET statusDate = \'" + \
         str(rejectDate) + "\' WHERE manuscriptID = " + str(manuID) + ";"
    runQuery(q2)

#changes manuscript status to typeset and adds number of pages to Accepted
def typesetManuscript(manuID, pp):
    manuStatus = getManuscriptStatus(manuID)
    if int(pp) > 100:
        print("ERROR: The maximum number of pages within an issue is 100 pages. A manuscript cannot exceed this limit")
        return

    if manuStatus != 3:
        print("ERROR: Manuscript must be in 'Accepted' state prior to typesetting")
        return

    q1 = "UPDATE Manuscript SET statusID = 4 WHERE manuscriptID = " + str(manuID) + ";"
    runQuery(q1)

    q2 = "UPDATE Accepted SET pages = " + str(pp) + " WHERE manuscriptID = " + str(manuID) + ";"
    runQuery(q2)


def scheduleManuscript(manuID, pubYear, pubPeriod):
    manuStatus = getManuscriptStatus(manuID)
    if manuStatus != 4:
        print("ERROR: Manuscript must be in 'typesetting' state prior to scheduling")
        return

    q1 = "SELECT pages FROM Accepted WHERE manuscriptID = " + str(manuID) + ";"
    numPages = runQuery(q1)[0][0]
    q2 = "SELECT totalPages FROM Issue WHERE pubYear = " + str(pubYear) + " AND pubPeriod = " + str(pubPeriod) + ";"
    totalPages = runQuery(q2)
    if totalPages != []:
        totalPages = totalPages[0][0]
        if (int(numPages) + int(totalPages)) > 100:
            print("Error: The addition of this manuscript to the selected issue exceeds the page limit")
            return


    #create issue if it does not exist, add to existing issue if it does
    if checkForIssue(pubYear, pubPeriod):
        runQuery("UPDATE Issue SET totalPages = " + str(totalPages + numPages) + " WHERE pubYear = " + str(
            pubYear) + " AND pubPeriod = " + str(pubPeriod) + ";")
    else:
        runQuery("INSERT INTO Issue VALUES (" + str(pubYear) + ", " + str(pubPeriod) + ", " + str(numPages) + ", NULL);")

    #updates Accepted and Issue entries
    runQuery("UPDATE Accepted SET pubYear = " + str(pubYear) + ", pubPeriod = " + str(pubPeriod) + " WHERE manuscriptID = " + str(manuID) + ";")
    runQuery("UPDATE Manuscript SET statusID = 5 WHERE manuscriptID = " + str(manuID) + ";")


def publishManuscript(pubYear, pubPeriod):
    publishDate = datetime.now().strftime('%Y-%m-%d')
    q1 = "UPDATE Issue SET printDate = " + publishDate + " WHERE pubYear = " + str(pubYear) + " AND pubPeriod = " + str(pubPeriod) + ";"
    runQuery(q1)

    issueManuscripts = getIssueManuscripts(pubYear, pubPeriod)
    for i in range(0, len(issueManuscripts)):
        runQuery("UPDATE Manuscript SET statusID = 6 WHERE manuscriptID = " + str(issueManuscripts[i]) + ";")

def checkForIssue(pubYear, pubPeriod):
    existingIssues = runQuery("SELECT pubYear, pubPeriod FROM Issue")
    print(existingIssues)
    if existingIssues is None:
        return False
    if [(int(pubYear), int(pubPeriod))] == existingIssues:
        return True
    return False

#handle reviewer resignation
def reviewerResign(userID):
    userManuscripts = getReviewerManuscripts(userID)
    manuscriptsUnderReview = identifyUnderReview(userManuscripts)

    for i in range(0, len(manuscriptsUnderReview)):
        manuscriptID = manuscriptsUnderReview[i]
        reviewCount = runQuery("SELECT COUNT(manuscriptID) FROM Feedback WHERE manuscriptID = " + str(manuscriptID) + ";")

        #if the resigned reviewer is the only reviewer, set manuscript status to submitted
        if reviewCount == 1:
            runQuery("UPDATE Manuscript SET statusID = 0 WHERE manuscriptID = " + str(manuscriptID) + ";")

        manuscriptRIC = runQuery("SELECT ric FROM Manuscript WHERE manuscriptID = " + str(manuscriptID) + ";")
        reviewerRICs = getReviewerRICs()

        #if no other reviewers exist with matching RICs, set manuscript status to rejected
        if manuscriptRIC not in reviewerRICs:
            runQuery("UPDATE Manuscript SET statusID = 1 WHERE manuscriptID = " + str(manuscriptID) + ";")

    runQuery("DELETE FROM Feedback WHERE personID = " + str(userID) + ";")
    runQuery("DELETE FROM Reviewer WHERE personID = " + str(userID) + ";")
    runQuery("DELETE FROM Person WHERE personID = " + str(userID) + ";")
    print("Thank you for your service.")

def getReviewerRICs():
    reviewerRICs = runQuery("SELECT ric FROM RICode_Reviewer")

    #reformat RICs to remove extra commas
    for i in range(0, len(reviewerRICs)):
        reviewerRICs[i] = reviewerRICs[i][0]

    return reviewerRICs


def getIssueManuscripts(pubYear, pubPeriod):
    issueManuscripts = runQuery("SELECT manuscriptID FROM Accepted WHERE pubYear = " + str(pubYear) + " AND pubPeriod = " + str(pubPeriod) + ";")

    #reformat to remove commas
    for i in range(0, len(issueManuscripts)):
        issueManuscripts[i] = issueManuscripts[i][0]

    return issueManuscripts


def get_reviewers(manuID):
    q1 = "SELECT personID FROM Feedback WHERE manuscriptID = " + str(manuID) + ";"
    reviewers = runQuery(q1)
    if (len(reviewers) == 0):
        return None
    elif (len(reviewers) == 1):
        reviewers = [reviewers[0]]
    elif (len(reviewers) == 2):
        reviewers = [reviewers[0], reviewers[1]]
    else:
        reviewers = [reviewers[0], reviewers[1], reviewers[2]]
    return reviewers


def getManuscriptStatus(manuID):
    q1 = "SELECT statusID FROM Manuscript WHERE manuscriptID = " + str(manuID) + ";"
    manuscriptStatus = runQuery(q1)[0][0]
    return manuscriptStatus


#handles all database interactions of users
def handleUserInteraction(userID, pWord):
    userType = getUserType(userID)
    if userType == 0:
        print("Error: User not found\n")
        return
    q2 = "SELECT fName FROM Person WHERE personID = " + str(userID) + ";"
    result2 = runQuery(q2)
    if len(result2) == 0:
        print("Error: User id not found in the system.\nIf you are a new user,"
              "please register.\n")
        return
    q1 = "SELECT fName FROM Person WHERE (personID = " + str(userID) + " AND pWord = \'" + pWord + "\');"
    result = runQuery(q1)
    if (len(result) == 0):
        print("Error: User id and password do not match.\n")
        return

    login(userID, userType)

    ranQuery = True
    firstQuery = True # keep track of first query to only print instructions once

    while ranQuery == True:

        if userType == "a":
            if firstQuery:
                printAuthorInstructions()
                firstQuery = False

            if authorQuery(userID) == False:
                ranQuery = False

        elif userType == "e":
            if firstQuery:
                printEditorInstructions()
                firstQuery = False

            if editorQuery(userID) == False:
                ranQuery = False

        elif userType == "r":
            if firstQuery:
                printReviewerInstructions()
                firstQuery = False

            if reviewerQuery(userID) == False:
                ranQuery = False
        else:
            print ("Invalid usertype")
            ranQuery = False

def retract_manuscript(userID, manuID):
    q2 = "SELECT primaryAuthorID FROM Manuscript WHERE (manuscriptID = " + \
         str(manuID) + " AND primaryAuthorID = " + str(userID) + ");"
    result = runQuery(q2)
    if len(result) == 0:
        print("You have not submitted any manuscripts with that ID.\n")
        return
    if getManuscriptStatus(manuID) > 3:
        print("Manuscript cannot be retracted because it has already\n"
              "been sent for typesetting.\n")
        return
    decision = raw_input("Are you sure? Type \"YES\" or \"NO\".\n")
    if decision == "YES":
        q1 = "DELETE FROM Manuscript WHERE manuscriptID = " + str(manuID) + ";"
        runQuery(q1)
        print("Manuscript deleted.\n")
        return
    elif decision == "NO":
        print("Manuscript delete canceled.\n")
        return
    else:
        print("You did not answer \"YES\" or \"NO\". Manuscript delete canceled.\n")
        return

def handleAuthorRegistration():
    fName = raw_input("Please enter your first name: ")
    lName = raw_input("Please enter your last name: ")
    pWord = raw_input("Please enter a password for the system: ")
    email = raw_input("Please enter your email address: ")
    affiliation = raw_input("Please enter the institution you are affiliated with: ")
    print("Please enter the following fields of your current address: ")
    addr1 = raw_input("Address Line 1: ")
    addr2 = raw_input("Address Line 2 (enter if none): ")
    city = raw_input("City: ")
    state = raw_input("State (enter if none): ")
    country = raw_input("Country: ")
    zip = raw_input("5-digit zip (enter if none): ")
    if zip == "":
        zip = None
    else:
        while (int(zip) > 99999):
            zip = raw_input("Invalid zip. Please enter 5-digit zip (enter if none): ")

    pID = register("author", fName, lName, pWord, email, addr1, addr2, city, state,
                   country, zip, affiliation)
    return pID

def handleEditorRegistration():
    fName = raw_input("Please enter your first name: ")
    lName = raw_input("Please enter your last name: ")
    pWord = raw_input("Please enter a password for the system: ")
    pID = register("editor", fName, lName, pWord)
    return pID

def handleReviewerRegistration():
    fName = raw_input("Please enter your first name: ")
    lName = raw_input("Please enter your last name: ")
    pWord = raw_input("Please enter a password for the system: ")
    email = raw_input("Please enter your email address: ")
    affiliation = raw_input("Please enter the institution you are affiliated with: ")
    ric1 = raw_input("Please enter your first area of interest code: ")
    while (ric1 == "" or int(ric1) < 1 or int(ric1) > 124):
        ric1 = raw_input("Invalid code. Please enter a code between 1 and 124: ")
    ric2 = raw_input("Please enter your second area of interest code (enter if none): ")
    ric3 = raw_input("Please enter your third area of interest code (enter if none): ")

    if ric2 is "" or int(ric2) < 1 or int(ric2) > 124:
        ric2 = None
    if ric3 is "" or int(ric3) < 1 or int(ric3) > 124:
        ric3 = None
    pID3 = register("reviewer", fName, lName, pWord, email, None, None, None, None, None, None, affiliation, ric1, ric2, ric3)
    return pID3

if __name__ == "__main__" :
    # getManuscriptStatus(1)
    #
    # acceptManuscript(8)
    # typesetManuscript(8, 12)
    # scheduleManuscript(8, 2014, 3)
    # print(getIssueManuscripts(2014, 3))
    # publishManuscript(2014, 3)
    # handleUserInteraction(7)

    # q1 = "INSERT INTO Test VALUES (DEFAULT, \'Kendall\');"
    # if q1[0:6] == "INSERT":
    #     print("YES!")
    # print(q1)
    # print("ID: " + str(runQuery(q1)))
    # #
    # pID = register("author", "Kendall", "Ernst", "password", "kendall@ernsthome.com", "5914 Norway Rd.", None, "Dallas", "TX", "USA", 75230, "Dartmouth College")
    # q2 = "SELECT * FROM Author WHERE personID = " + str(pID) + ";"
    # print(q2)
    # print(str(runQuery(q2)))
    #
    # pID2 = register("editor", "Kevin", "Xue", "password", "xuexue@databaseislife.com")
    # q3 = "SELECT * FROM Person WHERE personID = " + str(pID2) + ";"
    # print(q3)
    # print(str(runQuery(q3)))
    # q4 = "SELECT * FROM Editor WHERE personID = " + str(pID2) + ";"
    # print(q4)
    # print(str(runQuery(q4)))
    #
    # pID4 = register("editor", "Zach", "Schnell", "ohboyohboy")
    #
    #
    # create_rics()
    # pID3 = register("reviewer", "Elias", "Bello", "thisismypassword", "elias@happyhappydb.org", None, None,
    #                 None, None, None, None, "University of North Carolina", 3, 4)
    # q5 = "SELECT * FROM Person WHERE personID = " + str(pID3) + ";"
    # print(q5)
    # print(str(runQuery(q5)))
    # q6 = "SELECT * FROM Reviewer WHERE personID = " + str(pID3) + ";"
    # print(q6)
    # print(str(runQuery(q6)))
    # q7 = "SELECT * FROM RICode_Reviewer WHERE personID = " + str(pID3) + ";"
    # print(q7)
    # print(str(runQuery(q7)))
    # q8 = "SELECT interest FROM RICodes WHERE ric = 3"
    # print(q8)
    # print(str(runQuery(q8)))
    #
    # pID5 = register("reviewer", "Connor", "Lehan", "kendallrox", "cOnNoR@LeHaN.com", None, None, None,
    #                 None, None, None, "Dartmouth College", 3, 4)
    #
    # pID6 = register("reviewer", "Hannah", "Matheson", "kevinrox", "hannah@booboo.org", None, None,
    #                 None, None, None, None, "University of Iowa", 3, 4)
    #
    # print(datetime.now().strftime('%Y-%m-%d'))
    #
    # inputArray = ["submit", "My article", "Dartmouth College", 2,
    #               "Elias Bello", "Jean Shaheen", None, "kendall.pdf"]
    # authorSubmit(1, inputArray)
    #
    # # THIS WORKS BUT WITH ERROR
    # assign_manuscript(1,4)
    #
    # # THIS WORKS BUT WITH ERROR
    # reject_manuscript(1)
    #
    # assign_manuscript(1,5)
    # assign_manuscript(1,6)
    # print(str(get_reviewers(1)))

    # retract_manuscript(1, 1)
    create_rics()
    print("Welcome to the Journal of E-commerce Research Knowledge!")
    mode = raw_input("Please type either \"register\", \"login\" or \"quit\": ")
    validInput = 0
    while (validInput == 0):
        if (mode == "register"):
            validInput = 1
            validType = 0
            personType = raw_input("Are you an editor, reviewer, or author?: ")
            while (validType == 0):
                if (personType == "author"):
                    validType = 1
                    authorID = handleAuthorRegistration()
                    print("Your user ID is: " + str(authorID))
                    userID = raw_input("Enter your user ID: ")
                    pWord = raw_input("Enter your password: ")
                    handleUserInteraction(userID, pWord)
                elif (personType == "editor"):
                    validType = 1
                    editorID = handleEditorRegistration()
                    print("Your user ID is: " + str(editorID))
                    userID = raw_input("Enter your user ID: ")
                    pWord = raw_input("Enter your password: ")
                    handleUserInteraction(userID, pWord)
                elif (personType == "reviewer"):
                    validType = 1
                    reviewerID = handleReviewerRegistration()
                    print("Your user ID is: " + str(reviewerID))
                    userID = raw_input("Enter your user ID: ")
                    pWord = raw_input("Enter your password: ")
                    handleUserInteraction(userID, pWord)
                else:
                    personType = raw_input("Invalid input. Please type either \"author\", \"editor\" or \"reviewer\": ")
        elif (mode == "login"):
            validInput = 1
            userID = raw_input("Enter your user ID: ")
            pWord = raw_input("Enter your password: ")
            handleUserInteraction(userID, pWord)
        elif (mode == "quit"):
            print("Goodbye!")
            validInput = 1
        else:
            mode = raw_input("Invalid input. Please type either \"register\", \"login\" or \"quit\": ")





