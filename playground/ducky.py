import marimo

__generated_with = "0.11.23"
app = marimo.App(width="medium")


@app.cell
def _():
    import json

    return (json,)


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
def _(mo):
    _df = mo.sql(
        """
        CREATE TABLE foo (
          id integer,
          name varchar
        );
        """
    )
    return (foo,)


@app.cell
def _():
    obj = {
        "_id": "match-id:000016107429316a1d35bbc32fd02eaa",
        "_rev": "1-4c3d0c37fe600c9d6bb0a702d0a611d1",
        "ids": [
            {
                "authority": "bds",
                "type": "crid",
                "value": "crid://bbc.co.uk/b/22117454",
            },
            {
                "authority": "music_reporting",
                "type": "programme_number",
                "value": "PEF42000332AAB",
            },
            {"authority": "pips", "type": "pid", "value": "b00ryf18"},
        ],
        "title": {"value": "Episode 4", "source": "pips"},
        "contentType": {"value": "episode", "source": "pips"},
        "synopses": [
            {
                "source": "pips",
                "value": "Olivia O'Leary talks to gay ministers Martin Reynolds and Clare Herbert.",
                "type": "short",
            },
            {
                "source": "pips",
                "value": "Olivia O'Leary is joined in conversation by two gay ministers Martin Reynolds and Clare Herbert, who talk about whether the church accepts their sexuality.",
                "type": "medium",
            },
            {
                "source": "pips",
                "value": "Gay ministers, Martin Reynolds and Clare Herbert, talk to Olivia O'Leary about whether the church accepts their sexuality and how open they can be about their personal life. How do they reconcile the fact that if they win the acceptance they crave, it may split the church they love?\n\nProducer: Sara Conkey.",
                "type": "long",
            },
        ],
        "masterBrand": {
            "id": "bbc_radio_four",
            "source": "pips",
            "name": "BBC Radio 4",
        },
        "entityParents": [
            {"id": "match-id:16848cd5a8902c30c833d6cf0ac0596f", "source": "pips"}
        ],
        "ancestors": [
            {
                "id": "match-id:16848cd5a8902c30c833d6cf0ac0596f",
                "contentType": {"value": "series", "source": "pips"},
                "entityParents": [
                    {
                        "id": "match-id:20abfa23a64a672a71016b2997d0deeb",
                        "source": "pips",
                    }
                ],
                "ids": [
                    {
                        "authority": "bds",
                        "type": "crid",
                        "value": "crid://bbc.co.uk/b/21626307",
                    },
                    {"authority": "pips", "type": "pid", "value": "b00rdxyt"},
                ],
                "synopses": [
                    {
                        "source": "pips",
                        "value": "Olivia O'Leary brings together two people who have had profound and similar experiences",
                        "type": "short",
                    },
                    {
                        "source": "pips",
                        "value": "Olivia O'Leary presents the series which brings together two people who have had profound and similar experiences",
                        "type": "medium",
                    },
                ],
                "title": {"value": "Series 5", "source": "pips"},
            },
            {
                "id": "match-id:20abfa23a64a672a71016b2997d0deeb",
                "contentType": {"value": "brand", "source": "pips"},
                "entityParents": [],
                "ids": [
                    {
                        "authority": "bds",
                        "type": "crid",
                        "value": "crid://bbc.co.uk/b/7091347",
                    },
                    {"authority": "pips", "type": "pid", "value": "b007p144"},
                ],
                "synopses": [
                    {
                        "source": "pips",
                        "value": "Series bringing together people who have had profound and similar experiences",
                        "type": "short",
                    },
                    {
                        "source": "pips",
                        "value": "Series bringing together people who have had profound and similar experiences to hear their individual stories and compare the long-term effects on each of their lives",
                        "type": "medium",
                    },
                ],
                "title": {"value": "Between Ourselves", "source": "pips"},
            },
        ],
        "mediaType": {"value": "audio", "source": "pips"},
        "versions": [],
        "transmissions": [],
        "mcc_cdc": {"update_type": "INSERT", "object_type": "episode", "sequence": 0},
    }
    return (obj,)


@app.cell
def _(Rule, Via):
    via = Via(
        Rule(src="$._id", dst="$.id"),
        Rule(src="$.ids[*].value", dst="$.ids[*]"),
        Rule(src="$..source", dst="$.sources[*]"),
        Rule(src="$..id", dst="$.all_ids[*]"),
    )
    return (via,)


@app.cell
def _(json, obj, via):
    cooked = via.transform(obj)
    # print(json.dumps(cooked, indent=2))
    print(json.dumps(cooked, indent=2))
    return (cooked,)


if __name__ == "__main__":
    app.run()
