import json
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid import GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_lottie import st_lottie
from streamlit_tags import st_tags

from utils import local_css, load_lang_loc_file, load_lotti_file, hide_st_style

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

local_css("assets/search.css")


def set_lang():
    if st.session_state.get("location", None) is None:
        st.session_state["location"] = "Algeria"


lotti_path = load_lotti_file('data/data.json')
langs, locs, data = load_lang_loc_file('data/ll.json')

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

col1, col2, col3, col4 = st.columns([1.8, 1.25, 1.25, 1.1])
with col1:
    keywords = col1.text_input("Search keywords", "", placeholder="Search keywords")
    clicked = col1.button("Search", key="Search")

with col2:
    loc = col2.selectbox(
        "location",
        locs,
        # on_change=set_lang
    )

with col3:
    lang = col3.selectbox(
        "language",
        data[loc],
    )

with col4:
    device = col4.selectbox("Device", ["Desktop", "Mobile"])


if clicked:
    if keywords == "":
        st.error("❌ Please enter a keyword!")
    else:
        df = pd.DataFrame({"present?": [""], "keywords": [keywords], "locations": [loc], "languages": [lang], "device": [device]})
        gb = GridOptionsBuilder.from_dataframe(df)
        # enables pivoting on all columns
        gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True, editable=True)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True, )
        gb.configure_side_bar()
        gridOptions = gb.build()

        response = AgGrid(
            df,
            key="grid1",
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            data_return_mode=DataReturnMode.AS_INPUT,
            height=300,
            fit_columns_on_grid_load=True,
            configure_side_bar=False,
        )

        # The code below is for the download button
        cs, c1 = st.columns([2, 2])

        with cs:
            @st.cache
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode("utf-8")


            csv = convert_df(df)
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name="results.csv",
                mime="text/csv",
            )
        st.session_state.result = response

with st.form("my_form"):
    with st.sidebar:
        api_selectbox = st.selectbox(
            "Choose the API you wish to use",
            ("DataForSeo", "Scale Serp")
        )
        input_type_selectbox = st.selectbox(
            "Choose what you want to analyze",
            ("TextRazor", "Google NLP")
        )
        st.sidebar.info('##### Knowledge Graph Entity ID is extracted only using the Google NLP API.')
        submitted = st.form_submit_button("Extract Entities")
    if submitted:
        st.session_state.keywords = keywords
        st.session_state.location = loc
        st.session_state.language = lang
        st.session_state.device = device
        st.session_state.query_form = True


if 'query_form' in st.session_state and st.session_state.keywords:
    st.success("✅ Done!")
    df = pd.DataFrame(st.session_state.result["data"])
    gb = GridOptionsBuilder.from_dataframe(df)
    # enables pivoting on all columns
    gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="single", use_checkbox=True, )
    gb.configure_side_bar()
    gridOptions = gb.build()

    response = AgGrid(
        df,
        key="grid2",
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        data_return_mode=DataReturnMode.AS_INPUT,
        height=300,
        fit_columns_on_grid_load=True,
        configure_side_bar=False,
    )

    # The code below is for the download button
    cs, c1 = st.columns([2, 2])

    with cs:
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode("utf-8")

        csv = convert_df(df)
        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name="results.csv",
            mime="text/csv",
        )

if "query_form" in st.session_state and "keywords" not in st.session_state and "result" not in st.session_state.result:
    st.error("❌ Please enter a keyword and click search")