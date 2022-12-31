import streamlit as st

import pandas as pd

from semanticscholar import SemanticScholar

import plotly.express as px
from time import time

scholar = SemanticScholar()

st.set_page_config(page_title="ScholarViz")
title = st.title("ScholarViz: A Bird's Eye View Of The Research Changing The World")

def query_to_search(keys: list[str]):
    """Return search results based on query"""
    
    
    if len(query) < 1:
        
        return
    results = scholar.search_paper(query=query, fields=keys)
    
    #shownResults = [f'{results[x]["title"]}: {results[x]["url"]} <br/>' for x in range(10)]
    
    df = pd.DataFrame(data = {key: [results[x][key] if key != "title" else f"""<a href="{results[x]["url"]}">{results[x]["title"]}</a>""" for x in range(100)] for key in keys})
    df["plainTitle"] = [results[x]["title"] for x in range(100)]
    if sortTypeToColumn[sortType] in ["citationCount", "influentialCitationCount"]:
        ascending = False
    else:
        ascending = True
    df = df.sort_values(sortTypeToColumn[sortType], ascending=ascending)

    graph = px.bar(df.iloc[:numResults], x = "title", y = ["citationCount", "influentialCitationCount"], title=f"Visualising the Academic Influence of Papers related to {query.capitalize()}", barmode="group", height = 1000, width = 1000, labels={key: key.capitalize() for key in keys if key != "url"})
    graph.update_xaxes(tickangle=60)
    graph.update_yaxes(title="Citations Count")
    #query = st.text_input(label="Search a topic", placeholder="Search Query")
    #submitButton = st.button(label="Search", on_click=query_to_search, args=(query,  ["title", "url", "citationCount", "influentialCitationCount"]))    
    st.session_state["graph"] = graph
    #label = st.text(str(outputWidgets[0]))
    #graph

sortTypeToColumn = dict(zip(["Alphabetically", "By Recency", "By Citation Count", "By Influential Citation Count"], ["plainTitle", ["year", "publicationDate"], "citationCount", "influentialCitationCount"]))

# Using "with" notation
with st.sidebar:
    sortType = st.selectbox(
    "Sort Papers:",
    ["Alphabetically", "By Recency", "By Citation Count", "By Influential Citation Count"], index=2
    )
    numResults = st.slider(
        "Number of Results",
        10, 100, 10, 1
    )
    updateResults = st.button("Update Results", on_click=query_to_search, args=(["title", "url", "citationCount", "influentialCitationCount", "publicationDate", "year"], ))
query = st.text_input(label="Search for topic", placeholder="query")
submitButton = st.button(label="Search", on_click=query_to_search, args=(["title", "url", "citationCount", "influentialCitationCount", "publicationDate", "year"], ))




if len(st.session_state) > 0:
    st.session_state["graph"]

with st.expander("FAQ"):
    st.subheader("What are Citations?")
    "Citations, in the context of academia, are references to the sources of information or data used in a study. They serve as a rough, approximate measure of the academic influence a particular paper has."
        
    