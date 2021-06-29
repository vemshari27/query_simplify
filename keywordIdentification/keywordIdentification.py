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

from .syntaxAnalyzer import *


def query_detection(doc, syntax_analyzer):
    [syntax_check(sent.root, None, syntax_analyzer) for sent in doc.sents]
    return


def syntax_check(node, parent, syntax_analyzer):
    if node.n_lefts + node.n_rights > 0:
        syntax_analyzer.syntax_analyzer_preorder(node, parent)

        [syntax_check(child, node, syntax_analyzer) for child in node.lefts]
        syntax_analyzer.syntax_analyzer_inorder(node, parent)

        [syntax_check(child, node, syntax_analyzer) for child in node.rights]
        syntax_analyzer.syntax_analyzer_postorder(node, parent)
    else:
        syntax_analyzer.syntax_analyzer_preorder(node, parent)
        syntax_analyzer.syntax_analyzer_inorder(node, parent)
        syntax_analyzer.syntax_analyzer_postorder(node, parent)


def keyword_identification(doc, syntax_analyzer):
    query_detection(doc, syntax_analyzer)
    # syntax_analyzer.print_syntax_analyzer()
