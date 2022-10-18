ARCHITECTURE
==============

.. graphviz::

   digraph appArch {
        compound=true
        fontsize=10
        margin="0,0"
        ranksep = .75
        nodesep = .65
        node [shape=Mrecord fontname="Inconsolata, Consolas", fontsize=12, penwidth=0.5]
        edge [fontname="Inconsolata, Consolas", fontsize=10, arrowhead=normal]

        "HIJIM-UI" -> "HIJIM" [style = blod];
   }