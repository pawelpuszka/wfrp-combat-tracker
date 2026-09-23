CREATE TABLE momentum_actions (
    id                 SERIAL PRIMARY KEY,
    name               VARCHAR(200) NOT NULL,
    description        TEXT         NOT NULL,
    required_talent_id INT          DEFAULT NULL REFERENCES talents(id)
);