# 🐾 Crystal Portal Deployment Guide

Hey Mike! Here is your step-by-step guide to push this gorgeous Crystal dashboard to your new GitHub repository (`https://github.com/m0l0igd/Walmart-Crystal`) and configure the automated GitHub Action to keep it live on GitHub Pages!

---

## Step 1: Push the Files to GitHub

Since you have initialized the repository on GitHub, open **Git Bash** or your command line inside this directory (`C:\Users\m0l0igd\Documents\puppy_workspace`) and run these commands to sync up your files:

```bash
# 1. Initialize git locally
git init

# 2. Add your GitHub repository as the remote
git remote add origin https://github.com/m0l0igd/Walmart-Crystal.git

# 3. Pull the initial files (README.md, .gitattributes) to stay in sync
git pull origin main --rebase

# 4. Add all your new Crystal Portal files!
git add index.html index_template.html build_crystal_portal.py update_loop.py .github/

# 5. Commit your files
git commit -m "🐾 Initial commit: High-fidelity Crystal Portal with dual sub-markets and telemetry"

# 6. Push to GitHub!
git push -u origin main
```

---

## Step 2: Configure the Automated GitHub Action

To guarantee that the data stays up-to-the-minute live on GitHub Pages automatically without needing a local PC running:

1. Go to your repository on GitHub: `https://github.com/m0l0igd/Walmart-Crystal`
2. Click on **Settings** (top tab bar).
3. On the left sidebar, expand **Secrets and variables** $\rightarrow$ click **Actions**.
4. Click the green **New repository secret** button.
5. Set the **Name** to: `GCP_SA_KEY`
6. For the **Value**, paste your Google Cloud Service Account JSON key (the one with BigQuery viewer access).
7. Click **Add secret**.

*That's it!* Every 15 minutes, the GitHub Action will securely launch a runner, execute `build_crystal_portal.py`, compile the latest BigQuery metrics, and push the updated `index.html` to your site!

---

## Step 3: Turn on GitHub Pages 🌐

To host this portal for free on your GitHub Pages link so you can share it with Mike Leanox, Tony, and the rest of the team:

1. In your repository on GitHub, click **Settings**.
2. On the left sidebar, click **Pages**.
3. Under **Build and deployment**, set the **Source** to `Deploy from a branch`.
4. Under **Branch**, select `main` and `/ (root)` $\rightarrow$ click **Save**.
5. Give GitHub about 1 minute, and your site will be live at:
   👉 **`https://m0l0igd.github.io/Walmart-Crystal/`**

---

### 🐾 Files Included in your Workspace:
*   `index.html` $\rightarrow$ The fully compiled, ready-to-run dashboard.
*   `index_template.html` $\rightarrow$ The high-fidelity master template.
*   `build_crystal_portal.py` $\rightarrow$ The BigQuery integration & compilation script.
*   `update_loop.py` $\rightarrow$ Your local background service that updates `index.html` every 30 seconds.
*   `.github/workflows/update_portal.yml` $\rightarrow$ The automated GitHub action.
