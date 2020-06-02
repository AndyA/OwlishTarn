"use strict";

require("../lib/use");

const dgraph = require("dgraph-js");
const grpc = require("grpc");
const config = require("config");

// Create a client stub.
function newClientStub() {
  return new dgraph.DgraphClientStub(
    config.get("dgraph.host"),
    grpc.credentials.createInsecure()
  );
}

// Create a client.
function newClient(clientStub) {
  return new dgraph.DgraphClient(clientStub);
}

// Drop All - discard all data and start from a clean slate.
async function dropAll(client) {
  const op = new dgraph.Operation();
  op.setDropAll(true);
  await client.alter(op);
}

// Set schema.
async function setSchema(client) {
  const schema = `
    name: string @index(exact) .
    age: int .
    married: bool .
    loc: geo .
    dob: datetime .
    friend: [uid] @reverse .
  `;
  const op = new dgraph.Operation();
  op.setSchema(schema);
  await client.alter(op);
}

// Create data using JSON.
async function createData(client) {
  // Create a new transaction.
  const txn = client.newTxn();
  try {
    // Create data.
    const p = {
      uid: "_:astrid",
      name: "Astrid",
      age: 26,
      married: true,
      loc: { type: "Point", coordinates: [1.1, 2] },
      dob: new Date(1980, 1, 1, 23, 0, 0, 0),
      friend: [
        { name: "Bob", age: 24 },
        { name: "Charlie", age: 29 }
      ],
      school: [{ name: "Crown Public School" }],
      meta: { publish: true }
    };

    // Run mutation.
    const mu = new dgraph.Mutation();
    mu.setSetJson(p);
    const response = await txn.mutate(mu);

    // Commit transaction.
    await txn.commit();

    // Get uid of the outermost object (person named "Astrid").
    // Response#getUidsMap() returns a map from blank node names to uids.
    // For a json mutation, blank node label is used for the name of the created nodes.
    console.log(
      `Created person named "Astrid" with uid = ${response
        .getUidsMap()
        .get("astrid")}\n`
    );

    console.log("All created nodes (map from blank node names to uids):");
    response
      .getUidsMap()
      .forEach((uid, key) => console.log(`${key} => ${uid}`));
    console.log();
  } finally {
    // Clean up. Calling this after txn.commit() is a no-op
    // and hence safe.
    await txn.discard();
  }
}

// Query for data.
async function queryData(client) {
  // Run query.
  const query = `
    query all($a: string) {
      all(func: eq(name, $a)) {
        uid
        name
        age
        married
        loc
        dob
        friend {
          name
          age
        }
        school {
          name
        }
        meta { 
          publish
        }
      }
    }`;

  const vars = { $a: "Astrid" };
  const res = await client.newTxn().queryWithVars(query, vars);
  const ppl = res.getJson();

  // Print results.
  console.log(`Number of people named "Astrid": ${ppl.all.length}`);
  ppl.all.forEach(person => console.log(person));
}

(async () => {
  const stub = newClientStub();
  const client = newClient(stub);
  try {
    await dropAll(client);
    await setSchema(client);
    await createData(client);
    await queryData(client);

    // Close the client stub.
    stub.close();
  } catch (e) {
    console.error(e);
    process.exit(1);
  } finally {
    stub.close();
  }
})();
