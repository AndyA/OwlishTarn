import marimo

__generated_with = "0.12.2"
app = marimo.App(width="columns")


@app.cell(column=0)
def _(doc, json):
    print(json.dumps(doc, indent=2))
    return


@app.cell(column=1, hide_code=True)
def _(sample_slider):
    sample_slider
    return


@app.cell
def _(Rule, Via, date_time, uniq):
    via = Via.chain(
        Via(
            Rule(
                src="$.transmissions[*]",
                dst="$.txTimes[*]",
                via=date_time("$.transmissionDate", "$.transmissionStartTime"),
            ),
            Rule(src="$..source", dst="$.sources[*]"),
            Rule(src="$.patches[*][*].path", dst="$.patch_paths[*]")
        ),
        Via(
            Rule(),
            Rule(
                src=[
                    "$.txTimes",
                    "$.sources",
                ],
                map=[sorted, uniq],
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


@app.cell(column=2)
def _(cooked, json):
    print(json.dumps(cooked, indent=2))
    return


@app.cell(column=3)
def _(doc, via):
    cooked = via.transform(doc)
    return (cooked,)


@app.cell
def _(db, sample_ids, sample_slider):
    current_id = sample_ids[sample_slider.value]
    doc = db.get(current_id)
    return current_id, doc


@app.cell
def _(mo, sample_ids):
    sample_slider = mo.ui.slider(start=0, stop=len(sample_ids) - 1, step=1)
    return (sample_slider,)


@app.cell
def _():
    # sample = db.query("sample/sample", limit=25, update="lazy", start_key=0.1)
    # sample_ids = sorted([row["id"] for row in sample])
    return


@app.cell
def _():
    sample_ids = [
      "match-id:15a4734b33625e1a94bcffaa6a7babb2",
      "match-id:15a47408dac9a517b39efbec0f3d623d",
      "match-id:15a639ac3a24b0342124294cfb7cace1",
      "match-id:15a934bacfecbce88f735c8241a302b3",
      "match-id:15aa95b5385b295b943c9adaaa3a3d59",
      "match-id:15ad2cb8ac70006fd8549fab724017e5",
      "match-id:15af3853bd9329482b2f5d242babfc7b",
      "match-id:15aff4f49d1c437812ef0c2991358fa9",
      "match-id:15b04581703abe2c7dc5da291aacf596",
      "match-id:15b0874ad0eb0c65ff43124ad1e7cefd",
      "match-id:15b098740d028a5422b93a11815f0d59",
      "match-id:15b23c4b6dc650ee0cc6fe4e23620f29",
      "match-id:15b2cab055963c41eff5c5cf4c7aa273",
      "match-id:15b382d0f839f0c9014e6bf09c03c57e",
      "match-id:15b4caf6a44e9d01d4254b9c9624dc43",
      "match-id:15ba0e698026592782174287d9dd958c",
      "match-id:15ba7a098a87d9abe3c24c32dec5d6f5",
      "match-id:15bc9498ee21e32532666024085f5a0d",
      "match-id:15bc99870e2227f233194e57a43cfbeb",
      "match-id:15bcdf1e3c5815bb31c76cd6f5ad7a38",
      "match-id:15bd0e8af726b71df765a011b383ebcf",
      "match-id:38d68e05e3cba6bea93357677bf1c136",
      "match-id:38d74b9575753be54fd02625114dfadc",
      "match-id:38daaf5ba2902890b0f2494b59056aa4",
      "match-id:38dbe343791bc65013b1354d252a9ed6",
      "match-id:38dd44c04131a676b7b2db59ba6cfbb6",
      "match-id:38ddff4e6ccab29718f10d2c168dc51a",
      "match-id:38de43300f8aae46ff4febd64601f2d5",
      "match-id:38df38733185da34460e487ca91899b5",
      "match-id:38e5d9d7db0afea9f35172688bb2ccb4",
      "match-id:38e70833772545dab193d9249871cbca",
      "match-id:38eaf67e78a25a371e1bd3e24747a63a",
      "match-id:38ebeb21cda6c6da1a5afe7d357a9b4e",
      "match-id:38ed283aaf2fa3da326a2c84ae684c4a",
      "match-id:38ed3cced079ec3524b755af1b0e882f",
      "match-id:38ef0c224df7dcc24adfcba9343b71d3",
      "match-id:38f0d2bacfdd5e280d874be2fc95ddd0",
      "match-id:38f15409aef84d0141014a628b55340b",
      "match-id:38f1bd5f084829affe2012adf340f62e",
      "match-id:38f34ba20d49a49108274b3d2758d406",
      "match-id:38f3fa6e13f8757e9ada43123054867f",
      "match-id:38f6a2184af3981dccbfbe41c885d9c0",
      "match-id:38f85fc5418eb964903bc2dc36ca3101",
      "match-id:38fa3022c99645120ba8df5e6d27c736",
      "match-id:38fb1dec493ceb61d30e819da9f858d8",
      "match-id:38fd0060f086884e966f851ddb5c9256"
    ]
    return (sample_ids,)


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
