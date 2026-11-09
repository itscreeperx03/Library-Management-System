# Deploying Athena Library Management System on Render

This guide explains how to deploy the Athena LMS web application to [Render](https://render.com) in under 3 minutes.

---

## Method 1: Automatic Blueprint Deployment (Recommended & Easiest)

Because this repository includes a [`render.yaml`](../render.yaml) specification, Render can configure everything automatically.

### Steps:
1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **Blueprints** on the top menu (or **New +** &rarr; **Blueprint**).
3. Connect your GitHub account and select this repository:
   **`itscreeperx03/Library-Management-System`**
4. Render will read `render.yaml` and display:
   - **Service Name:** `athena-lms`
   - **Environment:** `Python`
   - **Plan:** `Free`
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2`
   - **Health Check Path:** `/health`
5. Click **Apply**.
6. Render will build the container, install packages, and deploy your live web application at:
   `https://athena-lms.onrender.com` (or your custom service URL).

---

## Method 2: Manual Web Service Setup

If you prefer setting up the web service manually:

1. In the Render Dashboard, click **New +** &rarr; **Web Service**.
2. Select **Build and deploy from a Git repository** and connect:
   `https://github.com/itscreeperx03/Library-Management-System`
3. Configure the following fields:

| Configuration Field | Setting Value |
| :--- | :--- |
| **Name** | `athena-lms` (or any name you choose) |
| **Region** | Oregon (US West) or any region |
| **Branch** | `main` |
| **Root Directory** | *(leave blank)* |
| **Runtime** | `Python` |
| **Build Command** | `pip install --upgrade pip && pip install -r requirements.txt` |
| **Start Command** | `gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2` |
| **Instance Type** | **Free** ($0 / month) |

4. Under **Advanced Settings**:
   - **Health Check Path:** `/health`
   - **Add Environment Variables:**
     - `PYTHON_VERSION`: `3.11.9`
     - `FLASK_ENV`: `production`
     - `SECRET_KEY`: *(click Generate or enter a secure string)*

5. Click **Create Web Service**.

---

## Post-Deployment Verification

Once deployed, visit your Render URL:
- **Web App Dashboard:** `https://<your-subdomain>.onrender.com/`
- **Books Catalog:** `https://<your-subdomain>.onrender.com/books`
- **Circulation Desk:** `https://<your-subdomain>.onrender.com/circulation`
- **Decision Table Simulator:** `https://<your-subdomain>.onrender.com/fines`
- **SE Dossier & DFDs:** `https://<your-subdomain>.onrender.com/se-dossier`
- **Health Check API:** `https://<your-subdomain>.onrender.com/health`

> [!NOTE]
> On Render's Free tier, instances spin down after 15 minutes of inactivity. When a new request arrives, Render spins the container back up within 30-50 seconds.
