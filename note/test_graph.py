import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from typing import Any


def println(title: str | None = None, data: Any | None = None,):
    if title is not None:
        print(f"---------{title}---------")
    if data is not None:
        print(data)
    print('\n')


def test_create_graph():
    g = nx.Graph()

    g.add_node("a")
    # 给已建节点 添加属性
    g.nodes["a"]["alias"] = 1

    # 创建节点时 添加属性
    g.add_node("b", alias=2)

    # 批量创建节点 添加相同的属性
    g.add_nodes_from(["b", "c"], alias=-1)
    # 批量创建节点 分别添加不同的属性
    g.add_nodes_from([("d", {"alias": 5}), "e"])

    println(title="通过 node 直接添加节点", data=g.nodes())
    println(title="查看节点及其所有属性", data=g.nodes(data=True))
    println(title="查看节点及指定属性: 若无指定属性 则添加默认属性",
            data=g.nodes.data(data="alias", default="11"))  # 代码提示类型不对，其实没有问题

    g.add_edge("a", "b", desc="---")
    g.add_edges_from([("b", "c", {"desc": "hi"}), ("d", "e", {"desc": 123})])

    println(title="查看边及属性", data=g.edges(data=True))

    # # nx.draw(g, with_labels=True)
    # # plt.show()

    println(title="查看 graphml ")
    for i, line in enumerate(nx.generate_graphml(g)):
        print(i)
        print(line)

    entities = [
        ({"name": item[0], **(item[1] or {})})
        for item in g.nodes(data=True)
        if item is not None
    ]
    println(title="Entities", data=entities)

    df = pd.DataFrame({
        "nihao": [1, 2, 3, 4, 5]
    })
    df["nihao"] = ['\n'.join(nx.generate_graphml(g))]
    print(df)


if __name__ == "__main__":
    test_create_graph()
