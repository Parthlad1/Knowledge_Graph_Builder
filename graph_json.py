from pyvis.network import Network

def generate_knowledge_graph(data, output_path, highlight_node=None):
    net = Network(
        height="1000px",
        width="100%",
        directed=True,
        bgcolor="#222222",
        font_color="white"
    )

    # Add nodes
    for node in data["nodes"]:
        color = "#ff4444" if node["id"] == highlight_node else None
        size = 30 if node["id"] == highlight_node else 20

        net.add_node(
            node["id"],
            label=node["id"],
            title=node["type"],
            group=node["type"],
            color=color,
            size=size
        )

    # Add edges
    for rel in data["relationships"]:
        net.add_edge(
            rel["source"],
            rel["target"],
            label=rel["relation"]
        )

    net.save_graph(output_path)
