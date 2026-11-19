# Week 06 · Checking popular claims with the World Bank data

In class, we explored the World Bank development indicators, plotted relationships between variables and tested them with correlation tests. This week, your group works as a **team of data analysts at a consultancy**, builds a **dashboard** and **deploys it online**.

## The brief

Your consultancy checks **popular claims about countries** that circulate in the news, on social media and in political debates. Claims like *"as countries get richer, they pollute more"* are repeated so often that they shape narratives and ideologies, and they are often used to push an agenda. Very few people check them against the data.

Your team **chooses one claim**, picks the **indicators** it is about and **at least five countries**, and builds a dashboard with **one purpose**: to **visualize and test the correlation** behind that claim, country by country, between **2000 and 2020**.

Your colleagues are not statisticians. They need to understand in plain words **what the data supports, what it does not support, and what a correlation cannot tell**. Your verdict must come from the data, not from what the claim wants to hear.

The dashboard must be **compact and intuitive**: someone who opens the link for the first time should understand it in a minute, without long scrolling or reading.

## Your claim, indicators and countries

Your group makes three choices and **justifies each of them in one or two sentences in the dashboard**:

1. **One claim.** Pick one from the examples below or write your own. Why is this claim worth checking?
2. **One main indicator and at least three indicators to compare it with.** Use the indicators that the claim is about. Why these?
3. **At least five countries.** Why these? For example: countries that differ in income, region or size, or countries that are often named when the claim is made.

Two groups may choose the same claim. They will still choose different indicators and countries, and may come to different conclusions.

### Example claims

| Claim | Possible main indicator | Possible indicators to compare with |
|---|---|---|
| "As countries get richer, they pollute more." | `co2_per_capita`\* | `gdp_per_capita`\*, `renewvable_energy_consumption%`, `population_density` |
| "Growing internet use brings birth rates down." | `birth_rate` | `individuals_using_internet%`, `gdp_per_capita`\*, `rural_population%`\* |
| "Economic growth destroys forests." | `forest_land%` | `gdp_per_capita`\*, `agricultural_land%`, `population_density` |
| "More public health spending means longer lives." | `life_expectancy_at_birth` | `government_health_expenditure%`, `gdp_per_capita`\*, `death_rate` |
| "Fighting corruption makes the economy grow." | `gdp_per_capita`\* | `control_of_corruption_estimate`, `goverment_effectiveness_estimate`, `rule_of_law_estimate` |
| "The green transition makes countries poorer." | `renewvable_energy_consumption%` | `gdp_per_capita`\*, `co2_per_capita`\*, `trade_in_services%` |
| "Political instability fuels inflation." | `inflation_annual%` | `political_stability_estimate`, `goverment_effectiveness_estimate`, `gdp_per_capita`\* |
| "Leaving the countryside makes people live longer." | `life_expectancy_at_birth` | `rural_population%`\*, `individuals_using_internet%`, `gdp_per_capita`\* |
| "Military spending makes countries more stable." | `political_stability_estimate` | `military_expenditure%`, `rule_of_law_estimate`, `voice_and_accountability_estimate` |
| "Freedom of speech keeps corruption down." | `control_of_corruption_estimate` | `voice_and_accountability_estimate`, `individuals_using_internet%`, `gdp_per_capita`\* |

\* These columns are **not in the data**. Create them yourself:

- `gdp_per_capita` = `GDP_current_US` / `population` (US$ per person)
- `co2_per_capita` = `CO2_emisions` × 1000 / `population` (tonnes per person; `CO2_emisions` is in kt)
- `rural_population%` = `rural_population` / `population` × 100

The column names `renewvable`, `emisions` and `goverment` are misspelled in the original data. Use them as they are. Check `world_bank_development_indicators_description.txt` (or the description in the class notebook) for what each column measures and its unit.

### Which indicators can you use?

A correlation within one country needs an indicator that **changes from year to year** and has **enough years of data** between 2000 and 2020. Check this for your countries before you decide.

| | Indicators |
|---|---|
| **Good** for most countries | `birth_rate`, `death_rate`, `life_expectancy_at_birth`, `population`, `population_density`, `rural_population`, `GDP_current_US`, `individuals_using_internet%`, `renewvable_energy_consumption%`, `CO2_emisions`, `other_greenhouse_emisions`, `inflation_annual%`, `trade_in_services%`, `government_health_expenditure%`, `agricultural_land%`, the six `..._estimate` governance indices |
| **Check your countries** | `forest_land%` and `access_to_electricity%` (constant in some countries, for example 100 % electricity access), `military_expenditure%`, `government_expenditure_on_education%`, `real_interest_rate`, `intentional_homicides`, `tax_revenue%`, `expense%`, `electric_power_consumption` (ends in 2014) |
| **Do not use** | `avg_precipitation` and `land_area` (the same value, or almost, every year: precipitation is a long-term average copied into each year), the `..._std` columns (standard errors, not indicators), and the indicators with only a few years of data: `gini_index`, `research_and_development_expenditure%`, `central_goverment_debt%`, `risk_premium_on_lending`, `human_capital_index`, `doing_business`, `time_to_get_operation_license`, `statistical_performance_indicators`, `logistic_performance_index`, `multidimensional_poverty_headcount_ratio%` |

## Task

Build a dashboard that checks your claim. Layout, charts and UI elements are your choice, but these points are **required**:

1. **Group number, claim and members.** The title shows your **group number** and the **claim**, and the dashboard shows the **full names of the members who contributed**.
2. **Your choices, justified.** Below the title, one or two short sentences each on **why this claim**, **why these indicators** and **why these countries**.
3. **Only years 2000 to 2020.** Remove all other years from the data.
4. **Controls at the top.** The user chooses **one of your comparison indicators** (for example `mo.ui.dropdown`) and a **period within 2000–2020** (for example `mo.ui.range_slider`), placed together at the **top**. Everything updates when they change.
5. **Scatterplot.** The chosen indicator (x) against your main indicator (y). **Each point is one country in one year**, coloured by country, with a **tooltip** showing the **country**, the **year** and both values, and a **trend line per country**. This is the **main view** of the dashboard.
6. **One correlation test per country.** For each of your countries, run `pg.corr` on its years in the chosen period. Show, per country, `n` (years), `r`, the `p_val` and the 95 % confidence interval (`CI95`) in **one small table** (or a bar chart of `r` per country), next to or right below the scatterplot.
7. **Pearson or Spearman.** Your group decides which method to use. The dashboard says **which method** was used and **why**, in one or two sentences.
8. **Verdict on the claim.** In plain words: in **how many of your countries** the correlation is in the direction the claim expects, how **strong** it is (see *Correlation: what to check and report*) and whether it is **statistically significant**. Then a short verdict: the data for these countries and this period **supports** the claim, **contradicts** it, gives a **mixed** picture, or **cannot tell**. Add **one sentence on what a correlation cannot show** (see *Watch out*). Keep it to **three or four sentences**.
9. **Over time, in a tab.** A line chart (Altair) of your main indicator and of the chosen indicator **over the years**, one line per country. It shows the trends behind the correlation.
10. **No errors on screen.** If a country has fewer than 5 years with data for the chosen pair and period, or an indicator does not change at all in that period, show a message (for example with `mo.callout`) for that country instead of an error or `NaN`.
11. **Deployed and tested.** The dashboard runs online and the link works (see *Deployment*).

**Recommended: distributions.** Add **bar charts** (histograms, Altair `mark_bar` with binning) of your main indicator and of the chosen indicator for the selected countries and period. They help you decide between Pearson and Spearman (skewed values, outliers, a few extreme years). They are a **check, not the message** of the dashboard, so keep them **secondary**: it is up to you where to place them, but they must not push the scatterplot, the test table or the verdict down the page. For example, a separate tab, a collapsible section (`mo.accordion`), or small charts side by side below the main view.

### Keep it compact

Nobody reads a dashboard that scrolls forever. Your dashboard has to fit in **about one to two screens**:

- **One main view:** controls on top, then the **scatterplot with the test table and the verdict beside or right below it**.
- **Secondary views in tabs** (`mo.ui.tabs`), so they don't add length.
- **Moderate chart sizes:** set `width` and `height` in `.properties()`; no chart wider than the page or taller than about half a screen.
- **Short text:** a title, the justification of your choices, one line that explains how to use the dashboard, and the verdict. No paragraphs of explanation, no raw tables of data, no printed pingouin output: show only the columns you need, rounded.
- **Readable labels:** axis titles in plain words with units (for example `GDP per capita (US$)`), not column names like `GDP_current_US`. Use the same labels in the dropdown.

A possible layout:

```
┌──────────────────────────────────────────────────────────────────────┐
│  Group X · "As countries get richer, they pollute more."             │
│  Members: full name 1, full name 2, full name 3                      │
│  Why this claim ... · Why these indicators ... · Why these countries │
│  Compare with [GDP per capita ▾]      Period [2000 ●────────● 2020]  │
├──────────────────────────────────────────────────────────────────────┤
│  [ Claim check ]  [ Over time ]  [ Distributions ]                   │
│  ┌──────────────────────────────┐   Spearman, 2000–2020              │
│  │                              │   Country   n    r      p          │
│  │  Scatterplot, one colour     │   Brazil    21   0.86   <0.001     │
│  │  and trend line per country  │   Germany   21  -0.80   <0.001     │
│  │                              │   India     21   0.98   <0.001     │
│  └──────────────────────────────┘   ...                              │
│  Verdict: mixed. In 2 of 5 countries ...                             │
└──────────────────────────────────────────────────────────────────────┘
```

### Correlation: what to check and report

**Null hypothesis.** For each country: H0 = between the two indicators there is **no linear** relationship (Pearson) or **no monotonic** relationship (Spearman) over the years of the chosen period.

**Pearson or Spearman?**
- **Pearson** measures a **straight-line** relationship. It is sensitive to skewed variables and to a few extreme years.
- **Spearman** works on the **ranks** of the values. It measures whether one variable tends to go up (or down) when the other goes up, even if the relationship is curved, and a few extreme years weigh less.
- With about 20 years per country, normality is hard to check. Look at the scatterplot: if the points of a country follow a curve or have outliers, prefer Spearman.

**Strength.** As a rough guide for the absolute value of `r`: below 0.1 negligible, 0.1 to 0.3 small, 0.3 to 0.5 moderate, above 0.5 large.

**Reading the pingouin table.**

```python
pg.corr(x=df_country["gdp_per_capita"], y=df_country["co2_per_capita"], method="spearman")
```

- `n` is the number of **years** that have **both** values for that country. Report it.
- `r` is the coefficient, from -1 to 1. The sign is the direction, the absolute value the strength.
- `CI95` is the range where the true correlation probably lies. If it contains 0, the result is not significant at 5 %. With only about 20 years, the intervals are wide.
- `p_val` is the probability of finding a correlation at least this strong if H0 were true.

### Watch out

- **Shared trends over time.** Many indicators move steadily in one direction between 2000 and 2020: internet use goes up almost everywhere, birth rates go down almost everywhere. Two such indicators will show a very strong correlation within a country (often close to -1 or 1) **even if one has nothing to do with the other**: both simply follow time. Look at the *Over time* tab before you write your verdict, and say if a shared trend could explain the result.
- **Correlation is not causation.** A correlation can also come from a third indicator (for example, the wealth of a country) that drives both. Many claims are about causes ("makes", "brings", "fuels"). A correlation cannot prove them.
- **Years are not independent.** The value of one year depends on the year before, so the p-values come out too optimistic. Read them with care, and give more weight to the direction and strength across your countries.
- **Countries, not aggregates.** The data also contains rows such as `World`, `High income` or `Sub-Saharan Africa`. They are not countries: do not choose them. Czechia, Turkiye and Viet Nam appear twice, under their new and old names. Use the new names, the old ones have almost no data.
- **Missing values.** Not every country reports every indicator every year. `pg.corr` drops the missing years, but you must report `n`.

### Optional extras

- **Year-to-year changes.** Add a switch (`mo.ui.switch`) that tests the **changes** from one year to the next instead of the values themselves (`.diff()` per country). Shared trends disappear, so this shows whether the two indicators also move together **from year to year**. Does your verdict change?
- **More countries.** Let the user add or remove countries with `mo.ui.multiselect`, starting with your selection.

## Deployment

Deploy the dashboard as a static website with **GitHub Pages**. Use **Netlify** or **molab** only if GitHub Pages does not work. GitLab is only for your submission, not for hosting.

**Before you start:** connect your local git with your GitHub account, following the instructions from **week 1**.

1. Create a new folder for the app, outside the GitLab repository, and turn it into a git repository:
   ```bash
   mkdir app-repo
   cd app-repo
   git init
   ```
2. Copy your `world_bank_dashboard.py` into that folder.
3. Open it in a sandbox and **wait until it runs as expected**. Install the libraries it asks for:
   ```bash
   uvx marimo edit --sandbox world_bank_dashboard.py
   ```
4. Close the notebook.
5. Export it as a WebAssembly app into a `docs` folder:
   ```bash
   mkdir docs
   uvx marimo export html-wasm world_bank_dashboard.py -o docs
   ```
6. Create a `.gitignore`, check with `git status` what would be uploaded, and add everything that should not be published (for example `.venv/`, `__pycache__/`):
   ```bash
   touch .gitignore
   git status
   nano .gitignore
   ```
7. Create an empty repository on GitHub, then commit and push:
   ```bash
   git add .
   git commit -m "deploy world bank dashboard"
   git remote add origin <url of your GitHub repository>
   git push -u origin main
   ```
8. On GitHub, go to *Settings → Pages*, choose *Deploy from a branch*, branch `main`, folder `/docs`. After a few minutes your link appears there.

**Test before you send the link.** Open it in a **private browser window** (or on another member's device) and try every UI element. Check that the data loads and the tests run. Ask someone outside your group to open it: if they cannot tell within a minute what the dashboard checks and what the verdict is, make it simpler.

**Sharing the link is mandatory.** Post it on our **Discord server** and paste it at the top of your **merge request description**, both by **Tuesday morning** at the latest (morning, not noon).

## Documentation

- Your class notebook and your drill of week 6
- marimo: [exporting to WebAssembly HTML](https://docs.marimo.io/guides/exporting/), [API reference](https://docs.marimo.io/api/): `mo.ui.dropdown`, `mo.ui.range_slider`, `mo.ui.tabs`, `mo.ui.switch`, `mo.ui.multiselect`, `mo.accordion`, `mo.hstack`, `mo.callout`
- Altair: [scatterplot with tooltips](https://altair-viz.github.io/gallery/scatter_tooltips.html), [regression line](https://altair-viz.github.io/user_guide/transform/regression.html), [histogram](https://altair-viz.github.io/gallery/simple_histogram.html), [multi-series line chart](https://altair-viz.github.io/gallery/multi_series_line.html), [regression per group](https://altair-viz.github.io/user_guide/transform/regression.html#grouping)
- pingouin: [`corr`](https://pingouin-stats.org/build/html/generated/pingouin.corr.html)
- Dataset: World Bank, [World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)

A UI element only updates other cells when it is **defined in one cell** and its `.value` is **read in another cell**.

If you use AI for any part of the code, mark it as described in your drills README: `###` = written entirely by AI, `##` = written partially by AI.

## What to deliver

This repository contains a template notebook, `world_bank_dashboard.py`, with the libraries and the data loading. **Fill in this file. Do not rename it, and do not create another notebook.**

- **Each variable can be defined in only one cell.** Names starting with an underscore, like `_tmp`, are private to their cell.
- **Do not delete or change the existing cells.** Add your own cells below them.
- **Do not upload data files to this repository.**

## Commits

**Every member must commit their own work themselves** and have **at least one commit** on the group branch.

## How to submit

1. Clone this repository.
2. **One member** creates your group branch, named `group-x-solution` with your group number, and pushes it.
3. **Each member** commits their work on that branch **themselves**. Pull before you start editing and again before you push:
   ```bash
   git pull
   git add world_bank_dashboard.py
   git commit -m "<what you added> by <your name>"
   git push
   ```
4. Open a **merge request** from your group branch into `main`, titled `group-x` with your group number, with the **link to the deployed dashboard** at the top of the description.
5. Post the same link on our **Discord server**.
6. **Do not merge it.** The merge request is your submission.

## Deadline

Merge request and link on Discord: **Tuesday morning** at the latest.
