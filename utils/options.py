USER_ROLES = (
    ('admin', 'admin'),
    ('auditor', 'auditor'),
    ('field_worker', 'field_worker'),
    ('manager', 'manager'),
    ('customer', 'customer')
)

CUSTOMER_TYPE = (
    ('residential', 'residential'),
    ('business', 'business')
)

SMS_CONSENT = (
    ('inferred', 'inferred'),
    ('expressed', 'expressed'),
    ('no', 'no')
)

LEAD_STATUS = (
    ("New Lead", "New Lead"),
    ("Call Scheduled", "Call Scheduled"),
    ("Contacted", "Contacted"),
    ("Negotiation", "Negotiation"),
    ("Won", "Won"),
    ("Lost", "Lost"),
)
