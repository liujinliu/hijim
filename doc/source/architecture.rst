ARCHITECTURE
==============

.. graphviz::

    digraph "arch_diagram" {
        rankdir=TB
        fontname="Helvetica,Arial,sans-serif"
        node [fontname="Helvetica,Arial,sans-serif"]
        edge [fontname="Helvetica,Arial,sans-serif"]
        graph [
            newrank = true,
            nodesep = 0.3,
            ranksep = 0.2,
            overlap = false,
            splines = false,
            layout=fdp,
        ]
        node [
            fixedsize = false,
            fontsize = 24,
            height = 1,
            shape = box,
            style = "filled,setlinewidth(5)",
            width = 2.2
        ]
        edge [
            arrowhead = none,
            arrowsize = 0.5,
            labelfontname = "Ubuntu",
            weight = 10,
            style = "filled,setlinewidth(5)"
        ]

        subgraph clusterUI {
            node [color = "#e27dd6ff"]
            edge [color = "#e27dd6ff"]
            label = "hijim ui"
            cluster = true
            webui [
                fillcolor = "#d9e7ee",
                fixedsize = true,
                label = "webui",
                row = usr,
                shape = ellipse
            ]
        }
        subgraph clusterHijim {
            node [color = "#e27dd6ff"]
            edge [color = "#e27dd6ff"]
            label = "hijim"
            cluster = true
            app [
                fillcolor = "#d9e7ee",
                fixedsize = true,
                label = "app",
                row = usr,
                shape = ellipse
            ]
            suite [
                fillcolor = "#d9e7ee",
                fixedsize = true,
                label = "suite",
                row = usr,
                shape = ellipse
            ]
        }
        clusterUI -> clusterHijim
    }
