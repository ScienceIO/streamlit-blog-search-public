import streamlit as st
import pandas as pd

st.set_page_config(page_title="Text Search", layout="centered", page_icon="📝")
DATA_FILEPATH = "litcovid.export.all.tsv"


@st.cache
def load_data(filepath:str) -> pd.DataFrame:
    """ Load data from local TSV """
    return pd.read_csv(filepath, sep="\t", skiprows=33).fillna("")


def search_dataframe(df:pd.DataFrame, column:str, search_str:str) -> pd.DataFrame:
    """ Search a column for a substring and return results as df """
    return df.loc[df[column].str.contains(search_str, case=False)]

print(st.__version__)

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
            st.success(f"Search is complete :rocket: — **{len(results)}** results found")

        # now display the top 10 results
        st.table(results.head(n=10))


if __name__ == '__main__':
    app()