# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair==6.3.0",
#     "marimo>=0.25.2",
#     "numpy==2.5.5",
#     "pandas==3.1.1",
#     "pingouin==0.7.0",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import numpy as np
    import pingouin as pg

    return alt, mo, np, pd, pg


@app.cell
def _(pd):
    base_url = "https://docs.google.com/spreadsheets/d/"
    doc_id = "1YY5iwL8J53umfHMNhJd1m-MbRPtRpX65oyxhq1KjzuI/"
    doc_format = "export?format=csv"

    url = base_url + doc_id + doc_format

    df_raw = pd.read_csv(url)
    return (df_raw,)


@app.cell
def _():
    ### CONFIG: written entirely by AI. Adapt this cell to your group's choices.
    GROUP = "06"
    CLAIM = "As countries get richer, they pollute more."
    MEMBERS = "Rahevar Sumitsinh Dharmendrasinh , Shreenath Shreepathi Hebbar"

    # Column names in df_raw for country and year. CHECK with df_raw.columns!
    COUNTRY_COL = "country"
    YEAR_COL = "date"

    COUNTRIES = ["Brazil", "Germany", "India", "China", "Nigeria"]  # >= 5
    MAIN = "co2_per_capita"
    LABELS = {
        "co2_per_capita": "CO2 emissions per capita (tonnes per person)",
        "gdp_per_capita": "GDP per capita (US$)",
        "renewvable_energy_consumption%": "Renewable energy (% of consumption)",
        "population_density": "Population density (people per km²)",
    }
    # dropdown: >= 3 indicators to compare with (NOT the main one)
    COMPARE = {
        LABELS[_k]: _k
        for _k in [
            "gdp_per_capita",
            "renewvable_energy_consumption%",
            "population_density",
        ]
    }

    # +1 = claim expects a positive correlation, -1 = a negative one
    EXPECTED_SIGN = 1
    METHOD = "spearman"  # or "pearson"

    WHY_CLAIM = "TODO: why is this claim worth checking?"
    WHY_INDICATORS = "TODO: why these indicators?"
    WHY_COUNTRIES = "TODO: why these countries?"
    WHY_METHOD = "TODO: why this method? (skewed values, outliers, curves ...)"
    return (
        CLAIM,
        COMPARE,
        COUNTRIES,
        EXPECTED_SIGN,
        GROUP,
        LABELS,
        MAIN,
        MEMBERS,
        METHOD,
        WHY_CLAIM,
        WHY_COUNTRIES,
        WHY_INDICATORS,
        WHY_METHOD,
    )


@app.cell
def _(COUNTRIES, df_raw, pd):
    ### DATA PREP: written entirely by AI
    df = df_raw.rename(columns={"date": "year"})
    if not pd.api.types.is_numeric_dtype(df["year"]):
        df["year"] = pd.to_datetime(df["year"], errors="coerce").dt.year
    df = df[df["year"].between(2000, 2020) & df["country"].isin(COUNTRIES)].copy()
    df["gdp_per_capita"] = df["GDP_current_US"] / df["population"]
    df["co2_per_capita"] = df["CO2_emisions"] * 1000 / df["population"]
    df["rural_population%"] = df["rural_population"] / df["population"] * 100
    return (df,)


@app.cell
def _(CLAIM, GROUP, MEMBERS, WHY_CLAIM, WHY_COUNTRIES, WHY_INDICATORS, mo):
    ### TITLE + JUSTIFICATION: written entirely by AI
    mo.md(
        f"""
    # Group {GROUP} · "{CLAIM}"
    **Members:** {MEMBERS}

    **Why this claim:** {WHY_CLAIM} &nbsp;·&nbsp; **Why these indicators:** {WHY_INDICATORS} &nbsp;·&nbsp; **Why these countries:** {WHY_COUNTRIES}

    *How to use: choose an indicator and a period. Each dot is one country in one year; lines are trends per country.*
    """
    )
    return


@app.cell
def _(COMPARE, mo):
    ### CONTROLS: written entirely by AI
    indicator = mo.ui.dropdown(
        options=COMPARE, value=list(COMPARE)[0], label="Compare with"
    )
    period = mo.ui.range_slider(
        start=2000, stop=2020, step=1, value=[2000, 2020], label="Period", show_value=True
    )
    mo.hstack([indicator, period], justify="start", gap=2)
    return indicator, period


@app.cell
def _(MAIN, df, indicator, period):
    ### SELECTION: written entirely by AI
    x_col = indicator.value
    start_year, end_year = period.value
    df_sel = df[df["year"].between(start_year, end_year)]
    plot_df = (
        df_sel[["country", "year", x_col, MAIN]]
        .dropna()
        .rename(columns={x_col: "x", MAIN: "y"})
    )
    return df_sel, end_year, plot_df, start_year, x_col


@app.cell
def _(COUNTRIES, MAIN, METHOD, df_sel, pd, pg, x_col):
    ### CORRELATION PER COUNTRY: written entirely by AI
    _rows = []
    notes = []
    for _c in COUNTRIES:
        _d = df_sel.loc[df_sel["country"] == _c, [x_col, MAIN]].dropna()
        if len(_d) < 5:
            notes.append(
                f"**{_c}:** only {len(_d)} year(s) with data for this pair and period, so no test."
            )
            continue
        if _d[x_col].nunique() < 2 or _d[MAIN].nunique() < 2:
            notes.append(
                f"**{_c}:** one of the indicators does not change in this period, so no test."
            )
            continue
        _res = pg.corr(_d[x_col], _d[MAIN], method=METHOD)
        # column names differ a bit between pingouin versions
        _ci_col = [_k for _k in _res.columns if _k.startswith("CI95")][0]
        _p_col = "p_val" if "p_val" in _res.columns else "p-val"
        _ci = _res[_ci_col].iloc[0]
        _rows.append(
            {
                "country": _c,
                "n": int(_res["n"].iloc[0]),
                "r": float(_res["r"].iloc[0]),
                "p_val": float(_res[_p_col].iloc[0]),
                "CI95": f"[{_ci[0]:.2f}, {_ci[1]:.2f}]",
            }
        )
    results = pd.DataFrame(_rows, columns=["country", "n", "r", "p_val", "CI95"])
    return notes, results


@app.cell
def _(METHOD, WHY_METHOD, end_year, mo, notes, results, start_year):
    ### TABLE + WARNINGS: written entirely by AI
    _show = results.copy()
    _show["r"] = _show["r"].round(2)
    _show["p"] = _show["p_val"].map(lambda _p: "<0.001" if _p < 0.001 else f"{_p:.3f}")
    _show = _show[["country", "n", "r", "p", "CI95"]].rename(
        columns={"country": "Country"}
    )
    table = mo.ui.table(
        _show,
        selection=None,
        pagination=False,
        show_download=False,
        show_column_summaries=False,
    )
    callouts = mo.vstack([mo.callout(mo.md(_m), kind="warn") for _m in notes])
    method_note = mo.md(
        f"**{METHOD.capitalize()}**, {start_year}–{end_year}. {WHY_METHOD}"
    )
    return callouts, method_note, table


@app.cell
def _(
    EXPECTED_SIGN,
    LABELS,
    MAIN,
    METHOD,
    end_year,
    np,
    results,
    start_year,
    x_col,
):
    ### VERDICT (draft, edit thresholds/wording as a group): written entirely by AI
    _n = len(results)
    if _n == 0:
        verdict_text = (
            "**Verdict: cannot tell.** No country has enough data for this pair and period."
        )
    else:
        _sign = np.sign(results["r"])
        _sig = results["p_val"] < 0.05
        _same = int((_sign == EXPECTED_SIGN).sum())
        _same_sig = int(((_sign == EXPECTED_SIGN) & _sig).sum())
        _opp_sig = int(((_sign == -EXPECTED_SIGN) & _sig).sum())
        _mean_abs = float(results["r"].abs().mean())
        if _mean_abs < 0.1:
            _strength = "negligible"
        elif _mean_abs < 0.3:
            _strength = "small"
        elif _mean_abs < 0.5:
            _strength = "moderate"
        else:
            _strength = "large"

        if _same_sig >= 0.8 * _n:
            _label = "supports the claim"
        elif _opp_sig >= 0.8 * _n:
            _label = "contradicts the claim"
        elif _same_sig + _opp_sig == 0:
            _label = "cannot tell (nothing significant)"
        else:
            _label = "mixed picture"

        verdict_text = (
            f"**Verdict: {_label}.** For {LABELS[x_col]} vs. {LABELS[MAIN]} "
            f"({start_year}–{end_year}, {METHOD}), the correlation points in the expected "
            f"direction in {_same} of {_n} countries and is significant in "
            f"{int(_sig.sum())} of them; the average strength is {_strength} "
            f"(mean |r| = {_mean_abs:.2f}). "
            "Years are not independent, so p-values are probably too optimistic, and shared "
            "time trends can create strong correlations (see the *Over time* tab). "
            "A correlation cannot show that one indicator causes the other; a third factor "
            "could drive both."
        )
    return (verdict_text,)


@app.cell
def _(LABELS, MAIN, alt, plot_df, x_col):
    ### SCATTERPLOT: written entirely by AI
    _base = alt.Chart(plot_df).encode(
        x=alt.X("x:Q", title=LABELS[x_col], scale=alt.Scale(zero=False)),
        y=alt.Y("y:Q", title=LABELS[MAIN], scale=alt.Scale(zero=False)),
        color=alt.Color("country:N", title="Country"),
    )
    _points = _base.mark_circle(size=45, opacity=0.7).encode(
        tooltip=[
            alt.Tooltip("country:N", title="Country"),
            alt.Tooltip("year:Q", title="Year", format="d"),
            alt.Tooltip("x:Q", title=LABELS[x_col], format=",.2f"),
            alt.Tooltip("y:Q", title=LABELS[MAIN], format=",.2f"),
        ]
    )
    _lines = _base.transform_regression("x", "y", groupby=["country"]).mark_line()
    scatter = (_points + _lines).properties(width=400, height=300)
    return (scatter,)


@app.cell
def _(LABELS, MAIN, alt, df_sel, mo, x_col):
    ### OVER TIME + DISTRIBUTIONS (tabs content): written entirely by AI
    def _line(_col):
        _d = df_sel[["country", "year", _col]].rename(columns={_col: "value"})
        return (
            alt.Chart(_d)
            .mark_line(point=True)
            .encode(
                x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d")),
                y=alt.Y("value:Q", title=LABELS[_col], scale=alt.Scale(zero=False)),
                color=alt.Color("country:N", title="Country"),
                tooltip=[
                    alt.Tooltip("country:N", title="Country"),
                    alt.Tooltip("year:Q", title="Year", format="d"),
                    alt.Tooltip("value:Q", title=LABELS[_col], format=",.2f"),
                ],
            )
            .properties(width=330, height=230)
        )

    def _hist(_col):
        _d = df_sel[["country", _col]].dropna().rename(columns={_col: "value"})
        return (
            alt.Chart(_d)
            .mark_bar()
            .encode(
                x=alt.X("value:Q", bin=alt.Bin(maxbins=15), title=LABELS[_col]),
                y=alt.Y("count()", title="Country-years"),
                color=alt.Color("country:N", title="Country"),
            )
            .properties(width=330, height=200)
        )

    time_view = mo.hstack([_line(MAIN), _line(x_col)], align="start")
    dist_view = mo.hstack([_hist(MAIN), _hist(x_col)], align="start")
    return dist_view, time_view


@app.cell
def _(
    callouts,
    dist_view,
    method_note,
    mo,
    scatter,
    table,
    time_view,
    verdict_text,
):
    ### LAYOUT WITH TABS: written entirely by AI
    _side = mo.vstack([method_note, table, callouts])
    _claim_check = mo.vstack(
        [mo.hstack([scatter, _side], align="start", gap=2), mo.md(verdict_text)]
    )
    mo.ui.tabs(
        {
            "Claim check": _claim_check,
            "Over time": time_view,
            "Distributions": dist_view,
        }
    )
    return


if __name__ == "__main__":
    app.run()
