// sh.removeShardTag("shard01", "US");
// sh.addShardTag("shard01", "US");
// sh.disableBalancing("test.customers");
// db.customers.drop();
// db.createCollection("customers"); 
// db.customers.createIndex( { factoryId: 1 } );
// sh.enableSharding("test");
// sh.shardCollection("test.customers",{ location: 1, factoryId: 1});
// sh.addTagRange(
//   "test.customers",
//   { "location" : "US", "factoryId" : MinKey },
//   { "location" : "US", "factoryId" : MaxKey },
//   "US"
// );

// sh.enableBalancing("test.customers");
var num = 2000
for(var i=0; i<num; i++){

    db.customers.insert({

        "location": "US",

        "factoryId": NumberInt(i)

    });
    db.customers.insert({

        "location": "EU",

        "factoryId": NumberInt(num+i)

    });

}


// sh.startBalancer();
// db.customers.find();