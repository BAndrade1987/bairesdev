1. ETL Pipeline (Python)
The first component is a Python-based ETL pipeline responsible for ingesting raw data from two external REST endpoints
Extraction
Fetch JSON data from the public API (users, posts) using robust HTTP requests with retry handling, timeouts, and error logging.
Transformation
Normalize nested fields into tabular form, join users with their respective posts, compute aggregation metrics, and standardize schema.
Loading
Write the curated dataset to a versioned CSV file (processed_users.csv), which serves as the downstream source of truth.

2. Relational Data Model (SQL)
The data model is designed in 3rd Normal Form to preserve data integrity and support efficient analytical querying.
Schema:
companies: A unique list of companies.
user: User entities referencing a company via foreign key.
posts; Posts referencing their authors.
Constraints & Performance:
Primary keys on all tables.
Foreign keys enforcing referential integrity.
Indexes on:
users.companyId
posts.userId
users.city

3. Analytics Layer (Google Sheets)
A lightweight analytics layer provides visibility into the processed dataset.
Using Google Sheets ensures accessibility and eliminates the need for BI tools.
Components:
Pivot tables:
Users per city
Posts per company
Average posts per user
Visual charts derived from these pivots
A consolidated dashboard for non-technical stakeholders

4. Automation Workflow (Zapier)
The automation layer introduces event-driven behavior to the system.
Trigger:
A new or updated CSV file in cloud storage (Google Drive).
Actions:
Parse the CSV contents.
Upsert records into the relational database.
Calculate processed metrics (users count, total posts).
Send a notification to Slack, email, or a webhook endpoint.
Optionally update the base CSV stored in the drive.

5. Webhook Service (FastAPI)
A simple FastAPI-based microservice provides an integration endpoint for external clients or systems that wish to insert new users into the database.
Responsibilities:
Accept JSON payloads via POST /webhook/new-user.
Validate input using Pydantic models.
Ensure company existence (create if absent).
Insert new users with referential integrity.
Return structured status responses.
Log all inbound events for auditability.
