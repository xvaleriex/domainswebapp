CREATE TABLE DOMAIN (
    fqdn varchar(50) NOT NULL,
    datetime_registered timestamp,
    datetime_unregistered timestamp NULL,
    PRIMARY KEY (fqdn)
);

CREATE OR REPLACE FUNCTION verifydomain2 ()
    RETURNS TRIGGER
    AS $body$
BEGIN
    PERFORM
        1
    FROM
        DOMAIN
    LIMIT 1;
    IF NOT FOUND THEN
        RETURN NEW;
    END IF;
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
    RETURN new;
END;
$body$
LANGUAGE plpgsql;

CREATE TRIGGER verify_domain_notexists2
    BEFORE INSERT OR UPDATE ON DOMAIN FOR EACH ROW
    EXECUTE PROCEDURE verifydomain2 ();

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
    PERFORM
        1
    FROM
        domain_flag
    LIMIT 1;
    IF NOT FOUND THEN
        RETURN NEW;
    END IF;
    IF OLD.domain_fqdn != NEW.domain_fqdn OR OLD.flag_type != NEW.flag_type OR OLD.datetime_from != NEW.datetime_to THEN
        RAISE exception 'Fields except for datetime_to cannot be changed.', new;
    END IF;
    IF NEW.datetime_to < CURRENT_TIMESTAMP THEN
        RAISE exception 'Datetime_to cannot be set to the past.';
    END IF;
    RETURN new;
END;
$body$
LANGUAGE plpgsql;

CREATE TRIGGER check_date_notpast
    BEFORE INSERT OR UPDATE ON domain_flag FOR EACH ROW
    EXECUTE PROCEDURE verify_date ();
 

 