---
date: 2024-04-15T18:00:35.091018
author: AutoGPT <info@agpt.co>
---

# QR Code Generator API 4

Given the information gathered from the user, the application's primary functionality centers around generating QR codes based on user-provided data, which encompasses URLs, textual content, or contact information. To cater to the user's preferences and requirements, the application will allow for customization of the QR code's physical attributes, including its size, with a minimum specification of 2 x 2 cm to ensure clarity and ease of scanning, and color, emphasizing a high contrast between the QR code and its background for optimal readability across various devices and scanning conditions, traditionally adopting a black-on-white configuration. Moreover, the user specifies a medium error correction level to balance data density and integrity effectively, making it adaptable across diverse applications while maintaining a satisfactory level of error correction. Lastly, the user has a preference for the QR code's output format to be in SVG, catering to scalability and high-resolution requirements. The tech stack chosen for implementing this functionality includes Python as the programming language, FastAPI for the API framework to handle requests efficiently, PostgreSQL for the database to store user preferences and generated codes, and Prisma as the ORM for seamless database integration and operations.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'QR Code Generator API 4'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
