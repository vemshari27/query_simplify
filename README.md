# PTGQ
Humans can easily parse and find answers to complex queries such as "What was the capital of the country of the discoverer of the element which has atomic number 1?" by breaking them up into small pieces, querying these appropriately, and assembling a final answer.  However, contemporary search engines lack such capability and fail to handle even slightly complex queries.  Search engines process queries by identifying keywords and searching against them in knowledge bases or indexed web pages. The results are, therefore, dependent on the keywords and how well the search engine handles them. In our work, we propose a three-step approach called parsing, tree generation, and querying (PTGQ) for effective searching of larger and more expressive queries of potentially unbounded complexity.  PTGQ parses a complex query and constructs a query tree where each node represents a simple query.  It then processes the complex query by recursively querying a back-end search engine, going over the corresponding query tree in postorder.  Using PTGQ makes sure that the search engine always handles a simpler query containing very few keywords.  Results demonstrate that PTGQ can handle queries of much higher complexity than standalone search engines.

## Compnents to PTGQ
Our work, _parsing, tree generation, and querying_ (PTGQ), is a three-step approach for processing complex queries. PTGQ breaks the search query into smaller pieces at relevant positions, orders these into its corresponding query tree, and processes it recursively with a search engine. This ensures that the reasoner always works with a few keywords. PTGQ uses dependency parsing as an intermediate step to construct smaller queries from a search query. The three steps involved in PTGQ are:
1. Dependency Parsing
2. Query Tree Construction
3. Progressive Querying

---

## About this repository
- main.py is to demo PTGQ. 
- tester.py is to reproduce results
- Each of the folders **dependencyParsing** ... contain the code of the respective step of the PTGQ process.
