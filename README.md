# Min-Bench

![travis build status](https://travis-ci.com/wigginslab/min-bench.svg?token=sJyWwcVqmgjZ6SuF12eq&branch=master)

An experimental minimalistic Lean Workbench. This product is specifically designed to help
NYCRIN I-Corps teams before and after the 6-week intensive I-Corps program.

Goals
-----
* Make it easy to modify and extend.
* Provide the minimal utilities/features to help early-staged startups commercialize their
products/research.

Setup
-----
1. Make sure you have a MongoDB server running. For example, to start a standalone
   MongoDB server, use `mongod --dbpath <database path>`. if you want to use the default path, first `mkdir -p /data/db`, set permissions, then `mongod`.

2. Next, install python requirements via `pip install -r requirements.txt`.

3. Run the tornado server via `python app.py`

4. open http://localhost:3036/

Todos
-----
* Get `Mentor Matcher` to work
* Get `VC Matcher` to work
