DROP SCHEMA IF EXISTS message;
CREATE SCHEMA message;

-- DROP TABLE IF EXISTS message;
CREATE TABLE message.message(
    senderID VARCHAR(64) NOT NULL,
    messageID INT(32) NOT NULL AUTO_INCREMENT,
    datetime TIMESTAMP NOT NULL,
    messageText VARCHAR(1000) NOT NULL,
    isLocation BOOLEAN NOT NULL,
    receiverID VARCHAR(64) NOT NULL,
    PRIMARY KEY (messageID)
);