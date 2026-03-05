---
title: BS Backend Task
emoji: ⚙️
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
---

# BiteSpeed Backend Task

## Live Deployment

```
https://lightrajat-bs-backend-task.hf.space/identify
```

## Request / Response Structure

### Request

```json
{
    "email"?: string,
    "phoneNumber"?: string
}
```

### Response

```json
{
    "contact": {
        "primaryContactId": number,
        "email": string[],
        "phoneNumber": string[],
        "secondaryContactIds": number[]
    }
}
```

## Tech Stack

* **FastAPI** – Backend server
* **Supabase** — PostgreSQL database
* **Docker** – Containerization
* **Hugging Face** – Hosting platform

## Identification Algorithm

To solve the [given problem](https://drive.google.com/file/d/1h3xh2PKP8aQW85hDdn2qUkXDUUAVDKaP/view), my algorithm follows these steps:

### 1. Find Existing Contacts

Query the database for contacts matching the incoming `email` or `phoneNumber`.

If none are found, a new **primary contact** is created and returned.

### 2. Expand Connected Contacts

For every matched contact, fetch all related contacts in the same identity group:

* If the contact is **primary**, retrieve all its secondary contacts.
* If the contact is **secondary**, retrieve its primary contact and then, in turn find its secondary contacts.

### 3. Resolve Multiple Primary Contacts

The previous step may end up gathering 2 different identity groups, in which case, multiple primary contacts will exist.

To resolve this, the **oldest contact (identified by `createdAt`) becomes the single primary**.

All other primaries are converted to **secondary contacts** and linked to the oldest primary.

### 4. Handle New Information

If the request contains a **new email or phone number not already present** in the contacts found so far, a new **secondary contact** is created and linked to the identified primary contact.

## Local Setup

### Prerequisites

1. [Astral uv](https://docs.astral.sh/uv/getting-started/installation) (Python dependency manager)

### Clone the repository

```bash
git clone git@github.com:lightRajat/bs-backend-task.git
cd bs-backend-task
```

### Install dependencies

```bash
uv sync
```

### Configure environment variables

Create a `.env` file with the following contents:

```bash
DATABASE_URL=your_database_connection_string
```

> **NOTE:** Database needs to be configured for this. You can use [Supabase](https://supabase.com/) for this.

### Initialize the database

```bash
uv run init.py --reset
```

> **NOTE:** `--reset` flag tells the script to reset the database if it already exists. Omitting it will skip the database initialization if it already exists.

### Run the server

```bash
uv run main.py
```

The API will be available at:

```
http://localhost:8000/identify
```
