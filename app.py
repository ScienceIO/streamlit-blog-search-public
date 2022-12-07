#!/usr/bin/env python

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Text Search", layout="centered", page_icon="📝")
DATA_FILEPATH = "litcovid.export.all.tsv"


@st.cache
def load_data(filepath:str) -> pd.DataFrame:
    """ Load data from local TSV """
    return pd.read_csv(filepath, sep="\t", skiprows=33).fillna("")


def search_dataframe(df:pd.DataFrame, column:str, search_str:str) -> pd.DataFrame:
    """ Search a column for a substring and return results as df """
    return df.loc[df[column].str.contains(search_str, case=False)]


def generate_barplot(results:pd.DataFrame, count_column:str, top_n:int=10):
    """load results from search_dataframe() and create barplot """
    return alt.Chart(results).transform_aggregate(
        count='count()',
        groupby=[f'{count_column}']
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('count', order='descending')]
    ).transform_filter(
        alt.datum.rank < top_n
    ).mark_bar().encode(
        y=alt.Y(f'{count_column}:N', sort='-x'),
        x='count:Q',
        tooltip=[f'{count_column}:N', 'count:Q']
    ).properties(
        width=700,
        height=400
    ).interactive()


def app():
    """ Search Streamlit App """
    st.title("Text Search 📝")

    # load data from local tsv as dataframe
    df = load_data(DATA_FILEPATH)

    # search box
    with st.form(key='Search'):
        text_query = st.text_input(label='Enter text to search')
        submit_button = st.form_submit_button(label='Search')
    
    # if button is clicked, run search
    if submit_button:
        with st.spinner("Searching (this could take a minute...) :hourglass:"):

            # search logic goes here! - search titles for keyword
            results = search_dataframe(df, "title_e", text_query)

            # notify when search is complete
            st.success(f"Search is complete :rocket: — **{len(results):,}** results found in {len(df):,}  papers.")

        # display the first 10 results
        st.table(results.head(n=10))

        # display a bar chart of top journals
        st.altair_chart(
            generate_barplot(results, "journal", 10)
        )


if __name__ == '__main__':
    app()