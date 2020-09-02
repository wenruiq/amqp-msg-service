    DROP SCHEMA IF EXISTS user;
    CREATE SCHEMA user;

    -- DROP TABLE IF EXISTS user;
    CREATE TABLE user.user (
        userID VARCHAR(64) NOT NULL,
        username VARCHAR(32) NOT NULL,
        fullname VARCHAR(64) NOT NULL,
        picture VARCHAR(300) NOT NULL,
        ipaddress VARCHAR(32) DEFAULT NULL,
        PRIMARY KEY (userID)
    );

    DROP SCHEMA IF EXISTS grp;
    CREATE SCHEMA grp;

    -- DROP TABLE IF EXISTS grp;
    CREATE TABLE grp.grp(
        grpID VARCHAR(32) NOT NULL,
        grpname VARCHAR(32) NOT NULL,
        PRIMARY KEY (grpID)
    );

    -- DROP TABLE IF EXISTS grpUsers;
    CREATE TABLE grp.grpUsers (
        grpID VARCHAR(32) NOT NULL,
        userID VARCHAR(64) NOT NULL,
        PRIMARY KEY (grpID, userID),
        FOREIGN KEY (grpID) REFERENCES grp(grpID),
        FOREIGN KEY (userID) REFERENCES user.user(userID)
    );

    -- DROP SCHEMA IF EXISTS message;
    -- CREATE SCHEMA message;

    -- DROP TABLE IF EXISTS message;
    -- CREATE TABLE message.message(
    --     senderID VARCHAR(64) NOT NULL,
    --     messageID INT(32) NOT NULL AUTO_INCREMENT,
    --     datetime TIMESTAMP NOT NULL,
    --     messageText VARCHAR(300) NOT NULL,
    --     isLocation BOOLEAN NOT NULL,
    --     receiverID VARCHAR(64) NOT NULL,
    --     PRIMARY KEY (messageID),
    --     FOREIGN KEY (senderID) REFERENCES user.user(userID),
    --     FOREIGN KEY (receiverID) REFERENCES user.user(userID)
    -- );

    DROP SCHEMA IF EXISTS contact;
    CREATE SCHEMA contact;

    -- DROP TABLE IF EXISTS contact;
    CREATE TABLE contact.contact(
        userID VARCHAR(64) NOT NULL,
        contactID VARCHAR(64) NOT NULL,
        PRIMARY KEY (userID, contactID)
    );