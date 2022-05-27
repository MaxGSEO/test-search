import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import numpy as np

np.random.seed(42)

def get_df():
    df = pd.DataFrame(columns=['foo','bar','baz'], data=np.random.choice(range(10), size=(100,3)))
    return df

df = get_df()

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(value=True, enableRowGroup=True, aggFunc=None, editable=False)

gb.configure_selection(selection_mode="multiple", use_checkbox=True)

with st.form("table_form", clear_on_submit=False):
    grid_response = AgGrid(df, gridOptions=gb.build(), height=700, data_return_mode="AS_INPUT", update_mode="SELECTION_CHANGED")#, enable_enterprise_modules=True)#.style.apply(highlight_clusters, axis=1))

    st.write(f"grid_response {grid_response}")
    selected = grid_response['selected_rows']
    st.write(f"selected {selected}")
    if st.form_submit_button("Submit"):
        pass