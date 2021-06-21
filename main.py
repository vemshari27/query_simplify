from dependencyParsing.dependencyParsing import dependency_parsing
from keywordIdentification.keywordIdentification import keyword_identification
from simpleQueryGeneration.simpleQueryGeneration import simple_query_generator
from queryTreeConstruction.queryTreeConstruction import tree_constructor
from queryTreeConstruction.queryTree import print_qt
from progressiveQuerying.progressiveQuerying import progressive_searcher


from keywordIdentification.syntaxAnalyzer import Syntax_Analyzer

import logging
logging.basicConfig(filename='app.log', filemode='a+',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def ptgq(text):
    logging.info("Query = " + str(text))
    syntax_analyzer = Syntax_Analyzer()
    logging.info("Syntax Analyzer Constructed")

    print("Dependency Tree")

    doc = dependency_parsing(text)
    logging.info("Dependency Tree Constructed")

    keyword_identification(doc, syntax_analyzer)
    logging.info("Keyword Identification Completed")

    print("Keywords Identified")
    syntax_analyzer.print_syntax_analyzer()

    simple_query_generator(doc, syntax_analyzer)
    logging.info("SubQuery Generation Completed")

    print("Subqueries Identified")
    syntax_analyzer.print_subqueries()

    qt = tree_constructor(doc, syntax_analyzer.get_pos_queries(), syntax_analyzer.get_prep_queries(
    ), syntax_analyzer.get_when_queries(), syntax_analyzer.get_wh_queries())
    logging.info("Query Tree Formed")

    print("Query Tree Formed")
    print_qt(qt)

    print("Progressive Querying")
    result = progressive_searcher(qt, {})
    logging.info("Progressive Querying Completed")
    print(result)
    logging.info("Result = " + str(result))


def runner():
    text = input("Query: ")
    ptgq(text)


if __name__ == "__main__":
    runner()
