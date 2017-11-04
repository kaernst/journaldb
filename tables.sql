/* Kendall Ernst & Kevin Xue */
/* Lab Assignment 2C */
/* Due: October 20, 2017 */

drop table IF EXISTS Coauthor_Manuscript;
drop table IF EXISTS Feedback;
drop table IF EXISTS RICode_Reviewer;
drop table IF EXISTS Accepted;
drop table IF EXISTS Issue;
drop table IF EXISTS Manuscript;
drop table IF EXISTS RICodes;
drop table IF EXISTS Author;
drop table IF EXISTS Coauthor;
drop table IF EXISTS Editor;
drop table IF EXISTS Reviewer;
drop table IF EXISTS Address;
drop table IF EXISTS Person;

CREATE TABLE Person (
	personID INT NOT NULL AUTO_INCREMENT,
    personType VARCHAR(1) NOT NULL CHECK (personType in ('a', 'e', 'r')),
    fName VARCHAR(45) NOT NULL,
    lName VARCHAR(45) NOT NULL,
    
    PRIMARY KEY (personID)
)
ENGINE = InnoDB;

CREATE TABLE Address (
	addressID INT NOT NULL AUTO_INCREMENT,
    addr1 VARCHAR(45) NOT NULL,
    addr2 VARCHAR(45) NULL,
    city VARCHAR(45) NOT NULL,
    state VARCHAR(45) NULL,
    country VARCHAR(45) NOT NULL,
    zip INT NULL CHECK (zip > 9999 AND `zip` < 100000),
    
    PRIMARY KEY (addressID))
ENGINE = InnoDB;

CREATE TABLE Author (
	personID INT NOT NULL,
    email VARCHAR(45) NOT NULL,
    affiliation VARCHAR(45) NOT NULL,
    addressID INT NOT NULL,
    
    PRIMARY KEY (personID),
    FOREIGN KEY (personID) REFERENCES Person (personID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (addressID) REFERENCES Address (addressID) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = InnoDB;

/* We chose to implement Coauthors as their own entity that does not inherit
from Person in order to maintain Person as a table solely of the system users,
since in our next assignment, they will be the only ones logging into the system
and will do so via their personIDs. Since coauthors cannot log into the system,
they should not have personIDs. It would cause more redundancy to search through
all the coauthors every time someone logs in to the system than it is to repeat
the first and last name attributes. */
CREATE TABLE Coauthor (
	coauthorID INT NOT NULL AUTO_INCREMENT,
    fName VARCHAR(45) NOT NULL,
    lName VARCHAR(45) NOT NULL,
    
    PRIMARY KEY (coauthorID)
)
ENGINE = InnoDB;

CREATE TABLE Editor (
	personID INT NOT NULL,

	PRIMARY KEY (personID),
    FOREIGN KEY (personID) REFERENCES Person (personID) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = InnoDB;

CREATE TABLE Reviewer (
	personID INT NOT NULL,
    email VARCHAR(45) NOT NULL,
    affiliation VARCHAR(45) NOT NULL,
    
	PRIMARY KEY (personID),
    FOREIGN KEY (personID) REFERENCES Person (personID) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = InnoDB;

CREATE TABLE RICodes (
	ric MEDIUMINT NOT NULL AUTO_INCREMENT,
    interest VARCHAR(64) NOT NULL,
    PRIMARY KEY (ric)
)
ENGINE = InnoDB;

CREATE TABLE Manuscript (
	manuscriptID INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(45) NOT NULL,
    dateReceived DATE NOT NULL, /* Asking Palmer if you can restrict to exclude future dates */
    statusID TINYINT NOT NULL CHECK (statusID >= 0 AND statusID <= 6),
    statusDate DATE NULL, /* Not in future restriction? */
    fileName BLOB NOT NULL,
    editorID INT NOT NULL, /* References Editor */
    primaryAuthorID INT NOT NULL, /* References Author */
    ric MEDIUMINT NOT NULL, /* References RICodes */
    
    PRIMARY KEY (manuscriptID),
    FOREIGN KEY (editorID) REFERENCES Editor (personID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (primaryAuthorID) REFERENCES Author (personID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ric) REFERENCES RICodes (ric) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = InnoDB;

CREATE TABLE Issue (
    pubYear INT NOT NULL,
    pubPeriod TINYINT NOT NULL CHECK (pubPeriod >= 1 AND pubPeriod <= 4),
    printDate DATE NULL, /* Not in future restriction? */
    totalPages TINYINT NULL CHECK (totalPages >= 1 AND totalPages <= 100),
    
    PRIMARY KEY (pubYear, pubPeriod)
)
ENGINE = InnoDB;

CREATE TABLE Accepted (
	manuscriptID INT NOT NULL,
    acceptDate DATE NOT NULL,
    pages TINYINT NULL CHECK (pages <= 100), /* Asking Palmer if you can restrict such that if status > typesetting, this can't be NULL */
    startPage TINYINT NULL CHECK (startPage >= 1 AND startPage <= 100),
    orderID INT NULL CHECK (orderID >= 1),
    pubYear INT NULL,
    pubPeriod TINYINT NULL CHECK (pubPeriod >= 1 AND pubPeriod <= 4),
    
    PRIMARY KEY (manuscriptID),
    FOREIGN KEY (manuscriptID) REFERENCES Manuscript (manuscriptID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (pubYear, pubPeriod) REFERENCES Issue (pubYear, pubPeriod) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = InnoDB;

CREATE TABLE Coauthor_Manuscript (
	coauthorID INT NOT NULL,
    manuscriptID INT NOT NULL,
    authorOrderID INT NOT NULL CHECK (authorOrderID > 1),
    
    PRIMARY KEY (coauthorID, manuscriptID),
    FOREIGN KEY (coauthorID) REFERENCES Coauthor (coauthorID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (manuscriptID) REFERENCES Manuscript (manuscriptID) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = InnoDB;

CREATE TABLE Feedback (
	manuscriptID INT NOT NULL,
    personID INT NOT NULL,
    appropriateness INT NULL CHECK (appropriateness >= 1 AND appropriateness <= 10),
    clarity INT NULL CHECK (clarity >= 1 AND clarity <= 10),
    methodology INT NULL CHECK (methodology >= 1 AND methodology <= 10),
    contribution INT NULL CHECK (contribution >= 1 AND contribution <= 10),
    recommendation INT NULL CHECK (recommendation = 0 OR recommendation = 1),
    reviewerAssignedDate DATE NOT NULL, /* Not in future restriction? */
    feedbackSentDate DATE NULL, /* Not in future restriction? */
    
    PRIMARY KEY (personID, manuscriptID),
    FOREIGN KEY (personID) REFERENCES Reviewer (personID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (manuscriptID) REFERENCES Manuscript (manuscriptID) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = InnoDB;

CREATE TABLE RICode_Reviewer (
	ric MEDIUMINT NOT NULL,
    personID INT NOT NULL,
    
    PRIMARY KEY (ric, personID),
	FOREIGN KEY (personID) REFERENCES Reviewer (personID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ric) REFERENCES RICodes (ric) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = InnoDB;