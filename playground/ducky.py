import marimo

__generated_with = "0.11.23"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(sample_slider):
    sample_slider
    return


@app.cell
def _(Rule, Via, date_time, lit, uniq):
    via = Via.chain(
        Via(
            Rule(dst="$.txTimes", via=lit([])),
            Rule(
                src="$.transmissions[*]",
                dst="$.txTimes[*]",
                via=date_time("$.transmissionDate", "$.transmissionStartTime"),
            ),
            Rule(src="$..source", dst="$.sources[*]"),
            Rule(
                src=[
                    "$._id",
                    "$..ids[*].value",
                    "$..id",
                    "$.transmissions[*].transmissionId",
                    "$.programmeNumber",
                ],
                dst="$.ids[*]",
            ),
        ),
        Via(
            Rule(),
            Rule(
                src=[
                    "$.txTimes",
                    "$.sources",
                    "$.ids",
                ],
                map=[sorted,uniq],
            ),
        ),
    )
    return (via,)


@app.cell
def _(Deleted, JP, ViaContext):
    def date_time(date_path: str, time_path: str):
        date_path = JP(date_path)
        time_path = JP(time_path)
        def vf(ctx: ViaContext):
            tx_time = ctx.get(time_path)
            if tx_time == Deleted:
                return ctx.get(date_path)
            else:
                return ctx.get(date_path) + "T" + tx_time

        return vf
    return (date_time,)


@app.cell(column=1)
def _(cooked, json):
    print(json.dumps(cooked, indent=2))
    return


@app.cell
def _(doc, via):
    cooked = via.transform(doc)
    return (cooked,)


@app.cell
def _(doc, json):
    print(json.dumps(doc, indent=2))
    return


@app.cell(column=2)
def _(db, sample_ids, sample_slider):
    current_id = sample_ids[sample_slider.value]
    doc = db.get(current_id)
    return current_id, doc


@app.cell
def _(mo, sample_ids):
    sample_slider = mo.ui.slider(start=0, stop=len(sample_ids)-1, step=1)
    return (sample_slider,)


@app.cell
def _(db):
    sample = db.query("sample/sample", limit=25, update="lazy", start_key=0.4)
    sample_ids = sorted([row["id"] for row in sample])

    return sample, sample_ids


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
    from via_jsonpath import Rule, Via, ViaContext, JP, Deleted, lit
    return Deleted, JP, Rule, Via, ViaContext, json, lit, mo, pycouchdb


if __name__ == "__main__":
    app.run()
