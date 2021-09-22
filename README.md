# invoice_reports

A Python script that helps me process invoices from our logistics providers.

Main.py runs the program.

The script reads:

- sales orders from Hasura/Postgres database through GraphQL
- all invoices from the invoice folder

The data is cleaned and combined into settlement reports (Excel).
