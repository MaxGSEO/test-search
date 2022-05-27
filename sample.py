import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid import GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_lottie import st_lottie

from utils import load_lang_loc_file, local_css, hide_st_style, load_lotti_file, get_live_search_results, get_entities

st.set_page_config(
    page_title="The Entities Swissknife",
    layout="centered",
    page_icon="https://cdn.shortpixel.ai/spai/q_lossy+ret_img+to_auto/https://studiomakoto.it/wp-content/uploads/2021/08/cropped-favicon-16x16-1-192x192.png",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": None
    }
)

# The code below is for the title and logo.
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown("###### [![this is an image link](https://studiomakoto.it/wp-content/uploads/2021/08/header-logo.webp)](https://studiomakoto.it/?utm_source=streamlit&utm_medium=app&utm_campaign=Entities-swissknife)")
st.markdown("###### Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/) , with ❤️ by [@max_geraci](https://studiomakoto.it/makoto_member/massimiliano-geraci/)   |   [![Twitter Follow](https://img.shields.io/twitter/follow/max_geraci?style=social)](https://twitter.com/max_geraci)   |   [![this is an image link](https://i.imgur.com/thJhzOO.png)](https://www.buymeacoffee.com/MaxG.SEO)")


lotti_path = load_lotti_file('data/data.json')
langs, locs, data = load_lang_loc_file('data/ll.json')
local_css("assets/search.css")

with st.sidebar:
    st_lottie(lotti_path, width=280, height=180, loop=False)

with st.expander("ℹ️ - About this app "):
    st.markdown(
        """  
This app, devoted to ✍️[Semantic Publishing](https://en.wikipedia.org/wiki/Semantic_publishing)✍️, relies on:
-   [Text Razor API](https://www.textrazor.com/) for Named-Entity Recognition ([NER](https://en.wikipedia.org/wiki/Named-entity_recognition)) and Linking ([NEL](https://en.wikipedia.org/wiki/Entity_linking));
-   [Google NLP API](https://cloud.google.com/natural-language) for NER and NEL;
-   Wikipedia API for scraping entities description;
-   For everything else, the beauty and power of 🐍Python🐍 and Steamlit.
        """
    )

with st.expander("✍️ - Semantic Publishing "):
    st.write(
        """  
The Entities Swissknife (TES) is a 100% 🐍Python🐍 app for Semantic publishing, i.e., publishing information on the web as documents accompanied by semantic markup (using the [schema.org](https://schema.org) vocabulary in JSON-LD format). Semantic publication provides a way for machines to understand the structure and meaning of the published information, making information search and data integration more efficient.
Semantic publishing relies on Structured Data adoption and Entity Linking (Wikification). Named entities are then injected into the JSON-LD markup to make the Content Topics explicit and 🥰Search engines friendly🥰: declare the main topic with the '[about](https://schema.org/about)' property and the secondary topics with the '[mentions](https://schema.org/mentions)' property).
The 'about' property should refer to 1-2 entities/topics at most, and these entities should be present in your H1 title. The 'mentions' properties should be no more than 3-5 depending on the article's length; as a general rule, an entities/topics should be explicitly mentioned in your schema markup if there is at least one paragraph dedicated to them (and they are possibly present in the relative headline).
The table with the "Top Entities by Frequency" takes into account for the Frequency count also the normalized entities and not only the exact word with which the entities are present in the text.
        """
    )

with st.expander("🔎 - How TES can support your Semantic SEO tasks "):
    st.write(
        """  
-   Know how NLU (Natural Language Understanding) algorithms “understand” your text to optimize it until the topics which are more relevant to you have the best relevance/salience score;
-   Analyze your SERP competitor’s main topics to discover possible topical gaps in your content;
-   Generate the JSON-LD markup (and inject it into your page schema) to explicit which topics your page is about to search engines. Declare your main topic with the 'about' property. Use the 'mentions' property to declare your secondary topics. This is helpful for disambiguation purposes too;
-   Analyze short texts such as a copy for an ad or a bio/description for an About-page (i.e., the [Entity Home](https://kalicube.com/faq/brand-serps/entity-home-in-seo-explainer/)).
       """
    )
st.write("Enter keywords to search for entities:")

col1, col2, col3, col4 = st.columns([1.8, 1.25, 1.25, 1.25])

with col1:
    keywords = st.text_input("Search keywords", "", placeholder="Search keywords")

with col2:
    location = st.selectbox(
        "location",
        locs,
    )
with col3:
    language = st.selectbox(
        "language",
        data[location],
    )
with col4:
    bsearch_clicked = st.button(label="Search")
#     device = st.selectbox("Device", ["Desktop", "Mobile"])

if bsearch_clicked:
    if keywords == "":
        st.warning("Please enter a keyword in search box")
        if "df" in st.session_state:
            del st.session_state.df
            st.session_state.extract_entities = False
    else:
        st.session_state.keywords = keywords
        st.session_state.location = location
        st.session_state.language = language
        st.session_state.extract_entities = False
        st.session_state.df = get_live_search_results(st.session_state.keywords, st.session_state.language, st.session_state.location)
if "df" in st.session_state:
    df = st.session_state.df
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridOptions = gb.build()
    with st.form("qf", clear_on_submit=True):
        response = AgGrid(
            df,
            key='grid1',
            gridOptions=gridOptions,
            enable_enterprise_modules=False,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            height=300,
            reload_data=True,
            fit_columns_on_grid_load=True,
            configure_side_bar=False,
        )

        submitted = st.form_submit_button("Extract Entities")
        st.session_state.extract_entities = True
        # if submitted:
        #     pass


api_selectbox = st.sidebar.selectbox(
    "Choose the API you wish to use",
    ("DataForSeo", "Scale Serp")
)
input_type_selectbox = st.sidebar.selectbox(
    "Choose what you want to analyze",
    ("TextRazor", "Google NLP")
)
st.sidebar.info('##### Knowledge Graph Entity ID is extracted only using the Google NLP API.')
side_form = st.sidebar.button("Do A Search Query")

if api_selectbox == "DataForSeo":
    if 'FormSubmitter:qf-Extract Entities' in st.session_state and st.session_state['FormSubmitter:qf-Extract Entities']:
        # find entities in selected rows from st.session_state
        if "selectedRows" in st.session_state['grid1'].keys():
            entities = get_entities(st.session_state["grid1"]["selectedRows"], st.session_state.language, st.session_state.location)
            st.write('### Entities', pd.DataFrame(entities))
        else:
            st.write("Please select some rows")
        # st.write(df)

# Download csv
if "grid1" in st.session_state:
    df = pd.DataFrame(st.session_state["df"])
    cs, c1 = st.columns([2, 2])
    with cs:
        @st.cache
        def convert_df(df):
            return df.to_csv().encode("utf-8")

        csv = convert_df(df)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="results.csv",
            mime="text/csv",
        )
if side_form and "grid1" not in st.session_state and "keywords" not in st.session_state:
    st.sidebar.warning("Please enter keywords in search box and click search")
