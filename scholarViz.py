import streamlit as st

import pandas as pd
import numpy as np

from semanticscholar import SemanticScholar

import plotly.express as px
from time import time

scholar = SemanticScholar()

st.set_page_config(page_title="ScholarViz")
title = st.title("ScholarViz: A Bird's Eye View Of The Research Changing The World")

def query_to_search(keys: list[str], chart_type: str):
    """Return search results based on query"""
    
    
    if len(query) < 1:
        
        return
    results = scholar.search_paper(query=query, fields=keys, limit=100)
    
    #shownResults = [f'{results[x]["title"]}: {results[x]["url"]} <br/>' for x in range(10)]
    
    df = pd.DataFrame(data = {key: [f"""<a href="{results[x]["url"]}">{results[x]["title"]}</a>""" if key == "title" \
                                    else results[x][key].get("name") if (key == "journal" and results[x][key] !=None) else results[x][key]  for x in range(100)] for key in keys})
    df["plainTitle"] = [results[x]["title"] for x in range(100)]
    df["publicationDate"].fillna("Uncertain", inplace=True)
    if "Bar" in chartType:
        if sortTypeToColumn[sortType] in ["citationCount", "influentialCitationCount"]:
            ascending = False
        else:
            ascending = True
        df = df.sort_values(sortTypeToColumn[sortType], ascending=ascending)
    if chart_type.lower() == "bar":
        graph = px.bar(df.iloc[:numResults], x = "title", y = ["citationCount", "influentialCitationCount"], title=f"Visualising the Academic Influence of Papers related to {query.capitalize()}", barmode="group", height = 1000, width = 1000, labels={key: key.capitalize() for key in keys if key != "url"}, hover_data=["publicationDate"], hover_name="title")
        graph.update_xaxes(tickangle=60)
        graph.update_yaxes(title="Citations Count")
    elif chart_type.lower() == "bubble":
        graph = px.scatter(df.iloc[:numResults], x ="publicationDate", y="influentialCitationCount", size=np.power(df.iloc[:numResults]["citationCount"], np.full(numResults, 0.7)) + 5, hover_name="title", log_y=True, color="venue", title=f"Visualising the Academic Influence of Papers related to {query.capitalize()}" )

    #query = st.text_input(label="Search a topic", placeholder="Search Query")
    #submitButton = st.button(label="Search", on_click=query_to_search, args=(query,  ["title", "url", "citationCount", "influentialCitationCount"]))    
    st.session_state["graph"] = graph
    #label = st.text(str(outputWidgets[0]))
    #graph

sortTypeToColumn = dict(zip(["Alphabetically", "By Recency", "By Citation Count", "By Influential Citation Count"], ["plainTitle", "publicationDate", "citationCount", "influentialCitationCount"]))

# Using "with" notation
with st.sidebar:
    chartType = st.selectbox(
        "Visualisation Type:",
        ["Bar Graph", "Bubble Chart"]
    )
    if chartType == "Bar Graph":
        sortType = st.selectbox(
        "Sort Papers:",
        ["Alphabetically", "By Recency", "By Citation Count", "By Influential Citation Count"], index=2
        )
    numResults = st.slider(
        "Number of Results",
        10, 100, 10, 1
    )
    updateResults = st.button("Update Results", on_click=query_to_search, args=(["title", "url", "citationCount", "influentialCitationCount", "publicationDate", "venue"], chartType[:chartType.index(" ")] ))
query = st.text_input(label="Search for topic", placeholder="query")
submitButton = st.button(label="Search", on_click=query_to_search, args=(["title", "url", "citationCount", "influentialCitationCount", "publicationDate", "venue"], chartType[:chartType.index(" ")]))




if len(st.session_state) > 0:
    st.session_state["graph"]

with st.expander("FAQ"):
    st.subheader("What are Citations?")
    "Citations, in the context of academia, are references to the sources of information or data used in a study. They serve as a rough, approximate measure of the academic influence a particular paper has."
    st.subheader("Why are there less labels than bars?")
    "If you choose to display a larger number of results, the chart will become too large to completely display. To display the labels for every bar, click on the full screen icon that can be seen on the top right of the chart when hovering over it."
    st.subheader("Why use ScholarViz instead of Semantic Scholar directly?")
    "ScholarViz is intended as a tool to help researchers, or anybody else, get a quick overview of an academic research area by visualising the relative impact of papers in the field. On the other hand, Semantic Scholar offers more detailed information."
        
    