// Account{num (not null, unique), name (not null)}
CREATE CONSTRAINT FOR (ac:Account) REQUIRE ac.num IS NOT NULL;
CREATE CONSTRAINT FOR (ac:Account) REQUIRE ac.num IS UNIQUE;
CREATE CONSTRAINT FOR (ac:Account) REQUIRE ac.name IS NOT NULL;

// Phone{phone (not null, unique)}
CREATE CONSTRAINT FOR (p:Phone) REQUIRE p.phone IS NOT NULL;
CREATE CONSTRAINT FOR (p:Phone) REQUIRE p.phone IS UNIQUE;

// Email{email (not null, unique)}
CREATE CONSTRAINT FOR (e:Email) REQUIRE e.email IS NOT NULL;
CREATE CONSTRAINT FOR (e:Email) REQUIRE e.email IS UNIQUE;

// Address{addr (not null, unique)}
CREATE CONSTRAINT FOR (ad:Address) REQUIRE ad.addr IS NOT NULL;
CREATE CONSTRAINT FOR (ad:Address) REQUIRE ad.addr IS UNIQUE;

// SENDS{num (not null, unique), timestamp (not null), amount (not null)}
CREATE CONSTRAINT FOR ()-[t:SENDS]-() REQUIRE t.num IS NOT NULL;
CREATE CONSTRAINT FOR ()-[t:SENDS]-() REQUIRE t.num IS UNIQUE;
CREATE CONSTRAINT FOR ()-[t:SENDS]-() REQUIRE t.timestamp IS NOT NULL;
CREATE CONSTRAINT FOR ()-[t:SENDS]-() REQUIRE t.amount IS NOT NULL;