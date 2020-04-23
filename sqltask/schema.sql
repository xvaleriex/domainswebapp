CREATE TABLE DOMAIN (
    fqdn varchar(50) NOT NULL,
    datetime_registered timestamp,
    datetime_unregistered timestamp NULL,
    PRIMARY KEY (fqdn)
);

CREATE OR REPLACE FUNCTION verifydomain ()
    RETURNS TRIGGER
    AS $body$
BEGIN
    ---First, check if table is empty, if it is return new
    PERFORM
        1
    FROM
        DOMAIN
    LIMIT 1;
    IF NOT FOUND THEN
        RETURN NEW;
    END IF;
    ---if domain with same name found and is not unregistered yet, do not let change entry and raise exception
    PERFORM
        1
    FROM
        DOMAIN
    WHERE
        fqdn = NEW.fqdn
        AND datetime_unregistered IS NULL
    LIMIT 1;
    IF FOUND AND NEW.datetime_unregistered IS NULL THEN
        RAISE exception 'Domains cannot overlapse.';
    END IF;
    ---otherwise let user do the change
    RETURN new;
END;
$body$
LANGUAGE plpgsql;

CREATE TRIGGER verify_domain_notexists
    BEFORE INSERT OR UPDATE ON DOMAIN FOR EACH ROW
    EXECUTE PROCEDURE verifydomain ();

CREATE TYPE flag_types_choices AS enum (
    'EXPIRED',
    'OUTZONE',
    'DELETE_CANDIDATE'
);

CREATE TABLE domain_flag (
    id int PRIMARY KEY,
    domain_fqdn varchar(50) REFERENCES DOMAIN (fqdn) ON DELETE CASCADE,
    flag_type flag_types_choices,
    datetime_from timestamp,
    datetime_to timestamp NULL
);

CREATE FUNCTION verify_date ()
    RETURNS TRIGGER
    AS $body$
BEGIN
    ---First, check if table is empty, if it is then return new
    PERFORM
        1
    FROM
        domain_flag
    LIMIT 1;
    IF NOT FOUND THEN
        RETURN NEW;
    END IF;
    ---check if entry that is intended to change is different then datetime_to, then raise exception
    IF OLD.domain_fqdn != NEW.domain_fqdn OR OLD.flag_type != NEW.flag_type OR OLD.datetime_from != NEW.datetime_to THEN
        RAISE exception 'Fields except for datetime_to cannot be changed.';
    END IF;
    ---check if wanted time is not in the past
    IF NEW.datetime_to < CURRENT_TIMESTAMP THEN
        RAISE exception 'Datetime_to cannot be set to the past.';
    END IF;
    RETURN new;
END;
$body$
LANGUAGE plpgsql;

CREATE TRIGGER check_date_notpast
    BEFORE INSERT OR UPDATE ON domain_flag FOR EACH ROW
    EXECUTE PROCEDURE verify_date();

SELECT
    domain_fqdn
FROM
    domain_flag
WHERE
    flag_type = 'EXPIRED'
    OR flag_type = 'OUTZONE'
    AND datetime_to < CURRENT_TIMESTAMP;

SELECT
    domain.fqdn
FROM
    DOMAIN
    INNER JOIN domain_flag ON (domain.fqdn = domain_flag.domain_fqdn)
WHERE
    domain_flag.flag_type = 'EXPIRED'
    AND domain_flag.datetime_from < CURRENT_TIMESTAMP
    AND domain_flag.datetime_to > CURRENT_TIMESTAMP;


 