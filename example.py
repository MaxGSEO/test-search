import streamlit as st
dummy_data = ['IND', 'USA', 'BRA', 'MEX', 'ARG']

if 'dummy_data' not in st.session_state.keys():
    st.session_state['dummy_data'] = dummy_data
else:
    dummy_data = st.session_state['dummy_data']


def checkbox_container(data):
    st.header('Select A country')
    input = st.text_input('Enter country Code to add')
    if input:
        if input not in data:
            data.append(input)
    for i in data:
        st.checkbox(i, key='dynamic_checkbox_' + i)


def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_', '') for i in st.session_state.keys() if
            i.startswith('dynamic_checkbox_') and st.session_state[i]]


checkbox_container(dummy_data)
st.write('You selected:')
st.write(get_selected_checkboxes())
