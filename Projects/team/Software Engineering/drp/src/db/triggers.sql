DELIMITER //
CREATE TRIGGER add_user_id
BEFORE INSERT ON users 
FOR EACH ROW
BEGIN
    INSERT INTO entities (entity_type) VALUES ('user');
    SET NEW.account_id = LAST_INSERT_ID();
END; //

CREATE TRIGGER add_org_id
BEFORE INSERT ON organizations
FOR EACH ROW
BEGIN
    INSERT INTO entities (entity_type) VALUES ('organization');
    SET NEW.org_id = LAST_INSERT_ID();
END; //

CREATE TRIGGER limit_residential_associations
BEFORE INSERT ON meter_map
FOR EACH ROW
BEGIN
    DECLARE existing_user_association INT;
    DECLARE existing_meter_association INT;

    IF NEW.entity_id IN (SELECT account_id FROM users) THEN
        SET existing_user_association = (
            SELECT COUNT(*)
            FROM meter_map
            WHERE entity_id = NEW.entity_id
        );
        SET existing_meter_association = (
            SELECT COUNT(*)
            FROM meter_map as m
            JOIN entities as e ON m.entity_id = e.entity_id
            WHERE meter_id = NEW.meter_id AND entity_type = 'user'
        );
    END IF;

    IF existing_user_association > 0 OR existing_meter_association > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Meter is already associated with a residential user!';
    END IF;
END; //

CREATE TRIGGER link_user_entity_delete
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    DELETE FROM entities
    WHERE entity_id = OLD.account_id;
END; //

CREATE TRIGGER link_org_entity_delete
AFTER DELETE ON organizations
FOR EACH ROW
BEGIN
    DELETE FROM entities
    WHERE entity_id = OLD.org_id;
END; //

CREATE TRIGGER populate_deltas
BEFORE UPDATE ON meter_data
FOR EACH ROW
BEGIN
    DECLARE p_value DECIMAL(8,2);
    DECLARE d_value DECIMAL(8,2);

    IF NEW.meter_value IS NOT NULL THEN
        SELECT prediction_value INTO p_value
        FROM meter_data
        WHERE meter_id = NEW.meter_id AND start_time = NEW.start_time AND end_time = NEW.end_time;
        IF p_value IS NOT NULL THEN
            SET d_value = p_value - NEW.meter_value;
            IF d_value < 0 THEN
                SET NEW.delta_value = 0;
            ELSE
                SET NEW.delta_value = d_value;
            END IF;
        END IF;
    END IF;
END; //

CREATE TRIGGER org_prime_admin
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    DECLARE orguser_count INT;
    SELECT COUNT(*) INTO orguser_count
    FROM users
    WHERE org_id = NEW.org_id;
    IF orguser_count = 0 THEN
        SET NEW.approval_status = "Admin";
    END IF;
END;//

CREATE TRIGGER approve_residential
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    IF NEW.org_id IS NULL THEN
        SET NEW.approval_status = "Approved";
    END IF;
END;//

CREATE TRIGGER disallow_org_user_map
BEFORE INSERT ON meter_map
FOR EACH ROW
BEGIN
    DECLARE is_user INT;
    DECLARE in_org INT;
    SELECT
        CASE entity_type
            WHEN "User" THEN 1
            ELSE 0
        END INTO is_user
    FROM entities
    WHERE entity_id = NEW.entity_id;
    IF is_user = 1 THEN
        SELECT
            CASE
                WHEN org_id IS NULL THEN 0
                ELSE 1
            END INTO in_org
        FROM users
        WHERE account_id = NEW.entity_id;
    ELSE
        SET in_org = 0;
    END IF;

    IF is_user = 1 AND in_org = 1 THEN
        SIGNAL SQLSTATE "45000" SET MESSAGE_TEXT = "ORGANIZATION USER CANNOT BE ASSIGNED METER";
    END IF;
END;//

CREATE TRIGGER assign_distributor_meters
AFTER INSERT ON meters
FOR EACH ROW
BEGIN
    INSERT INTO meter_map (entity_id, meter_id) VALUES (1, NEW.meter_id);
END;//

DELIMITER ;
