# Godspower Johnson | Financial Data Analytics Portfolio

A responsive, zero-build static website designed for financial analytics, payment operations, reconciliation and commission economics. Includes **two runnable analytical demonstrations** and **one clearly labelled project blueprint**.

## Start

1. Unzip the folder.
2. Open `index.html` in Chrome, Edge or Firefox. It works offline, apart from optional Google Fonts.
3. Explore the **Analytics demo** and switch between Settlement and Commission. Change the provider/product filter.

## Personalize before publishing

Edit `assets/config.js`:
- `name`, `title` and `location` if needed
- `email`: your genuine contact address
- `github`: URL to your GitHub profile or repository
- `linkedin`: URL to your actual LinkedIn profile
- `resume`: relative URL to a PDF résumé you add, for example `assets/resume.pdf`

Only nonblank links are displayed. Add genuine education, certifications and professional achievements to the About section if you want to strengthen the personal narrative. **Do not publish confidential company data, private customer information, invented results or unverified claims.**

## What is real, what is illustrative?

- **Real, implemented:** the site, responsive layout, case pages, interactive filters, generated source data, PostgreSQL SQL queries, and Python/pandas analysis scripts.
- **Synthetic:** every sample amount, rate, provider transaction, agent and monthly trend.
- **Not implemented:** the architecture blueprint, production integrations, deployed Power BI dashboards or company outcomes.

## Included analysis files

```
data/synthetic_settlements.csv
analysis/settlement/analyze.py
analysis/settlement/reconciliation.sql

data/synthetic_agent_commissions.csv
analysis/commission/analyze.py
analysis/commission/commission.sql
analysis/requirements.txt
```

To run Python analysis:
```
python -m pip install -r analysis/requirements.txt
python analysis/settlement/analyze.py
python analysis/commission/analyze.py
```

The SQL files assume that CSVs have been imported as tables with matching fields. They are PostgreSQL examples rather than automatic database installers.

## Publish on GitHub Pages

1. Create a public GitHub repository, e.g. `financial-data-portfolio`.
2. Upload the **contents** of this folder to the repository root. `index.html` must be in the root, not nested one folder deep.
3. In repository **Settings > Pages > Build and deployment**, select **Deploy from a branch**.
4. Choose `main`, `/(root)`, and click **Save**.
5. GitHub provides a site URL, typically `https://YOURUSERNAME.github.io/financial-data-portfolio/`.
6. Test your project links, all filters and contact links on desktop and mobile.

The `.nojekyll` file is included for safe static hosting.

## File map

- `index.html`: home page
- `assets/styles.css`: all responsive styling
- `assets/app.js`: filter and dashboard logic
- `assets/config.js`: editable contact information
- `assets/demo-data.js`: generated synthetic records for the browser demo
- `case-studies/`: individual project pages
- `data/`: downloadable synthetic source CSVs
- `analysis/`: Python and SQL source code

## Calculation notes

- Settlement **unreconciled exposure** is the sum of absolute `expected - received`, with missing `received` treated as zero. It is an investigation estimate, not a booked liability.
- `Matched` means exact amount matching in the synthetic data; settlement delay is measured separately.
- GGR = stake minus winnings. Commission/GGR ratios are unavailable for non-positive denominators at the row level.
- The 40% cost threshold is a **hypothetical review threshold** in the demo, not an official policy.

## Next content milestones

1. Add verified results and screenshots of real, publishable Power BI reports.
2. Add an anonymized source-to-dashboard project using a documented data model.
3. Add one technical write-up showing edge-case tests, validation and choices made.
4. Link each project to a public repository containing setup instructions and tests.


## Five new portfolio case studies

The `projects/` directory now includes five end-to-end reproducible projects: fraud detection, commission optimisation, cashflow forecasting, payment reconciliation and business process efficiency. Each includes synthetic data, Python, SQL, calculated metrics, case-study pages, and Power BI DAX measures/build instructions. Compiled Power BI PBIX files are not included. All outputs are illustrative, not audited findings.
