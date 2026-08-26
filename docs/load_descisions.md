# Load Decisions

Outage records referencing feeders that do not exist in the feeder register
were excluded before loading.

This keeps the outage foreign key valid and prevents orphan outage records
from entering the database.

The foreign key constraint remains enforced in PostgreSQL.
