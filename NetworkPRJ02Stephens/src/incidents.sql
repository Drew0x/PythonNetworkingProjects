DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS keys;


CREATE TABLE incidents (
    slug VARCHAR(16) PRIMARY KEY,
    event_date DATE NOT NULL, 
    year INT NOT NULL, 
    month INT NOT NULL, 
    actor VARCHAR(50) NOT NULL, 
    actor_type VARCHAR(25) NOT NULL, 
    organization VARCHAR(100) NOT NULL,
    industry_code INT NOT NULL, 
    industry VARCHAR(100) NOT NULL, 
    motive VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_subtype VARCHAR(50) NOT NULL, 
    description VARCHAR(250) NOT NULL,
    source_url VARCHAR(200) NOT NULL,
    country VARCHAR(100) NOT NULL,
    actor_country VARCHAR(100) NOT NULL
);



CREATE TABLE keys (
    key VARCHAR(32) PRIMARY KEY
);

INSERT INTO keys VALUES
    ('TyA0BhKO5SgCmodHzGyFlv1PqI4BqOzk0tu1gMr0Gsc'), 
    ('NQs7PF3MvoVQazuiYj2T7m9-jMji53WOuE_kyo6CHV4'), 
    ('g29suJUerHjHqeWTl04jSDg12eTyvaAV9q_0zekffKo');