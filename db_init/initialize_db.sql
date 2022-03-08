CREATE SCHEMA shape;

CREATE TABLE IF NOT EXISTS shape.sensors_log (
    id              SERIAL,
    sensor_id       INTEGER NOT NULL,
    event_date      TIMESTAMP NOT NULL,
    status          VARCHAR(20) NOT NULL,
    temperature     NUMERIC NOT NULL,
    vibration       NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS shape.equipment_sensors(
    id              SERIAL,
    equipment_id    INTEGER NOT NULL,
    sensor_id       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS shape.equipment_group(
    id              SERIAL,
    equipment_id    INTEGER NOT NULL,
    code            VARCHAR(20) NOT NULL,
    group_name      VARCHAR(20) NOT NULL
);
