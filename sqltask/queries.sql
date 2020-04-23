SELECT domain_fqdn FROM
    domain_flag
WHERE
    (flag_type = 'EXPIRED'
    OR flag_type = 'OUTZONE')
    AND datetime_to < CURRENT_TIMESTAMP;

SELECT
    domain.fqdn
FROM
    DOMAIN
    left outer JOIN domain_flag ON (domain.fqdn = domain_flag.domain_fqdn)
WHERE domain_flag.id IS NULL OR NOT(
    domain_flag.flag_type = 'EXPIRED'
    AND domain_flag.datetime_from < CURRENT_TIMESTAMP
    AND domain_flag.datetime_to > CURRENT_TIMESTAMP) AND domain.datetime_unregistered is null;