    # Copyright © 2021 Eric John, Srihari Vemuru. All rights reserved
    
    # This file is part of PTGQ.

    # PTGQ is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # PTGQ is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with PTGQ.  If not, see <https://www.gnu.org/licenses/>.

from dependencyParsing.dependencyParsing import dependency_parsing
from keywordIdentification.keywordIdentification import keyword_identification
from simpleQueryGeneration.simpleQueryGeneration import simple_query_generator
from queryTreeConstruction.queryTreeConstruction import tree_constructor
from queryTreeConstruction.queryTree import print_qt
from progressiveQuerying.progressiveQuerying import progressive_searcher


from keywordIdentification.syntaxAnalyzer import Syntax_Analyzer

from time import process_time_ns


def ptgq(text):
    syntax_analyzer = Syntax_Analyzer()

    doc = dependency_parsing(text)

    t1_start = process_time_ns()

    keyword_identification(doc, syntax_analyzer)
    simple_query_generator(doc, syntax_analyzer)
    qt = tree_constructor(doc, syntax_analyzer.get_pos_queries(), syntax_analyzer.get_prep_queries(
    ), syntax_analyzer.get_when_queries(), syntax_analyzer.get_wh_queries())

    t1_stop = process_time_ns()

    return (t1_stop - t1_start)


def runner():
    f = open("./testCases/test_cases_queries_with_complexities.txt", "r")
    result = []
    for line in f:
        line_split = line.rsplit(' ', 1)

        if(line_split[1] != "-1\n"):
            print(line_split)
            result.append(ptgq(line_split[0]))

    f1 = open(
        "./results/ptgq_query_results.csv", "w+")
    f1.write("Query,Complexity,Word_Count,Time\n")
    f.seek(0, 0)

    i = 0
    for line in f:
        line_split = line.rsplit(' ', 1)

        if(line_split[1] != "-1\n"):
            content = line_split[0] + "," + \
                line_split[1][:1] + "," + \
                str(len(line_split[0].split())) + "," + str(result[i]) + "\n"
            f1.write(content)
            i += 1
        else:
            content = line_split[0] + "," + line_split[1][:2] + \
                "," + str(len(line_split[0].split())) + "," + "\n"
            f1.write(content)

    f.close()
    f1.close()


if __name__ == "__main__":
    runner()
