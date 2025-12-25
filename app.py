import streamlit as st
import json
import os
import streamlit.components.v1 as components
from graph_json import generate_knowledge_graph

GRAPH_HTML = "graphs/knowledge_graph.html"
DATA_FILE = "graph_data.json"

st.set_page_config(layout="wide")
st.title("🧠 Knowledge Graph Builder")

# Load graph data
if "graph_data" not in st.session_state:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        st.session_state.graph_data = json.load(f)

highlight_node = None
nodes = [n["id"] for n in st.session_state.graph_data["nodes"]]

col1, col2 = st.columns([1, 2])

# ---------------- ADD NODE ----------------
with col1:
    st.subheader("➕ Add Node")

    node_id = st.text_input("Node ID")
    node_type = st.text_input("Node Type")

    if st.button("Add Node"):
        if node_id and node_id not in nodes:
            st.session_state.graph_data["nodes"].append({
                "id": node_id,
                "type": node_type
            })
            st.rerun()

# ---------------- ADD RELATIONSHIP ----------------
with col1:
    st.subheader("🔗 Add Relationship")

    if nodes:
        source = st.selectbox("Source", nodes)
        target = st.selectbox("Target", nodes)
        relation = st.text_input("Relation")

        if st.button("Add Relationship"):
            st.session_state.graph_data["relationships"].append({
                "source": source,
                "target": target,
                "relation": relation
            })
            st.rerun()

# ---------------- DELETE NODE ----------------
with col1:
    st.subheader("❌ Delete Node")

    del_node = st.selectbox("Select Node to Delete", nodes)

    if st.button("Delete Node"):
        st.session_state.graph_data["nodes"] = [
            n for n in st.session_state.graph_data["nodes"]
            if n["id"] != del_node
        ]

        # Remove connected edges
        st.session_state.graph_data["relationships"] = [
            r for r in st.session_state.graph_data["relationships"]
            if r["source"] != del_node and r["target"] != del_node
        ]
        st.rerun()

# ---------------- DELETE EDGE ----------------
with col1:
    st.subheader("❌ Delete Relationship")

    edges = st.session_state.graph_data["relationships"]
    edge_labels = [
        f'{r["source"]} → {r["target"]} ({r["relation"]})'
        for r in edges
    ]

    if edge_labels:
        edge_index = st.selectbox("Select Relationship", range(len(edge_labels)),
                                  format_func=lambda i: edge_labels[i])

        if st.button("Delete Relationship"):
            st.session_state.graph_data["relationships"].pop(edge_index)
            st.rerun()

# ---------------- SEARCH NODE ----------------
with col1:
    st.subheader("🔍 Search Node")

    search = st.text_input("Search by Node ID")

    if search and search in nodes:
        highlight_node = search

# ---------------- SAVE JSON ----------------
with col1:
    if st.button("💾 Save Graph"):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.graph_data, f, indent=2)

# ---------------- GRAPH DISPLAY ----------------
with col2:
    st.subheader("📊 Live Knowledge Graph")

    os.makedirs("graphs", exist_ok=True)
    generate_knowledge_graph(
        st.session_state.graph_data,
        GRAPH_HTML,
        highlight_node=highlight_node
    )

    with open(GRAPH_HTML, "r", encoding="utf-8") as f:
        components.html(f.read(), height=1000)
