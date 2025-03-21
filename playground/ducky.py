import marimo

__generated_with = "0.11.23"
app = marimo.App(width="columns")


@app.cell(column=0)
def _(Rule, Via, uniq):
    via = Via(
        Rule(
            via=[
                Via(
                    Rule(src="$._id", dst="$.id"),
                    Rule(src="$.ids[*].value", dst="$.ids[*]"),
                    Rule(src="$..source", dst="$.sources[*]"),
                    Rule(src="$..title.value", dst="$.titles[*]"),
                    Rule(src="$..value", dst="$.values[*]"),
                ),
                Via(
                    Rule(),
                    Rule(src=["$.sources", "$.values"], map=uniq),
                ),
            ]
        )
    )
    return (via,)


@app.cell
def _(db):
    doc = db.get("match-id:0008fb2ddc6880c84d430feeb9195038")
    return (doc,)


@app.cell
def _(pycouchdb):
    server = pycouchdb.Server("http://chaise:sofa@lego:5984/")
    db = server.database("disco")
    return db, server


@app.cell
def uniq():
    def uniq(x: list[str]) -> list[str]:
        return list(set(x))
    return (uniq,)


@app.cell
def _():
    import json
    import pycouchdb
    import marimo as mo
    from via_jsonpath import Rule, Via
    return Rule, Via, json, mo, pycouchdb


@app.cell(column=1)
def _(cooked, json):
    print(json.dumps(cooked, indent=2))
    return


@app.cell
def _(doc, via):
    cooked = via.transform(doc)
    return (cooked,)


if __name__ == "__main__":
    app.run()
