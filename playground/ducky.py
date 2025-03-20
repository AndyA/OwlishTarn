import marimo

__generated_with = "0.11.23"
app = marimo.App(width="medium")


@app.cell
def _():
    import json

    import pycouchdb
    return json, pycouchdb


@app.cell
def _():
    import duckdb
    from via_jsonpath import Rule, Via
    return Rule, Via, duckdb


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(pycouchdb):
    server = pycouchdb.Server("http://chaise:sofa@lego:5984/")
    db = server.database("disco")
    return db, server


@app.cell
def _(Rule, Via):
    via = Via(
        Rule(src="$._id", dst="$.id"),
        Rule(src="$.ids[*].value", dst="$.ids[*]"),
        Rule(src="$..source", dst="$.sources[*]"),
        Rule(src="$..title.value", dst="$.titles[*]"),
    )
    return (via,)


@app.cell
def _(db):
    doc = db.get("match-id:00034dfdb5f6ade2308057c539a86151")
    return (doc,)


@app.cell
def _(doc, json, via):
    cooked = via.transform(doc)
    print(json.dumps(cooked, indent=2))
    return (cooked,)


if __name__ == "__main__":
    app.run()
