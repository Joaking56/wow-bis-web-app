import streamlit as st
import github_functions
import bg_func

bg_func.set_background("images/retri.jpeg", darkness=0.6)

if "missing_items_fonok_retri" not in st.session_state:
    st.session_state["missing_items_fonok_retri"] = github_functions.get_github_file("texts/fonok_retri.txt")
if "found_items_fonok_retri" not in st.session_state:
    st.session_state["found_items_fonok_retri"] = github_functions.get_github_file("texts/completed_fonok_retri.txt")

missing_items = st.session_state["missing_items_fonok_retri"]
found_items = st.session_state["found_items_fonok_retri"]

def save_edit():
    if "editing_fonok_retri" in st.session_state and "edit_input_fonok_retri" in st.session_state:
        new_value = st.session_state["edit_input_fonok_retri"]
        index = found_items.index(st.session_state["editing_fonok_retri"])
        found_items[index] = new_value + "\n"
        github_functions.write_github_file("texts/completed_fonok_retri.txt", found_items)
        del st.session_state["editing_fonok_retri"]

def clear_checkboxes():
    for i in range(len(missing_items) + 1):
        if f"missing_fonok_retri_{i}" in st.session_state:
            del st.session_state[f"missing_fonok_retri_{i}"]

st.title("Fonokvagyok RETRI BIS Checklist (Midnight Season 1)")

col_input, col_add = st.columns([4, 1])
with col_input:
    st.text_input(label="Enter the item and the dungeon name here to upload your list!",
                  placeholder="e.g. Ring 1 - WORK",
                  key="new_item_fonok_retri")
with col_add:
    st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
    if st.button("Add", key="add_fonok_retri"):
        if st.session_state["new_item_fonok_retri"] != "":
            missing_items.append(st.session_state["new_item_fonok_retri"] + "\n")
            github_functions.write_github_file("texts/fonok_retri.txt", missing_items)
            del st.session_state["new_item_fonok_retri"]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("Missing Items:")
for index, missing_item in enumerate(missing_items):
    checkbox = st.checkbox(missing_item, key=f"missing_fonok_retri_{index}")
    if checkbox:
        found_items.append(missing_item)
        github_functions.write_github_file("texts/completed_fonok_retri.txt", found_items)
        missing_items.pop(index)
        github_functions.write_github_file("texts/fonok_retri.txt", missing_items)
        clear_checkboxes()
        st.rerun()

st.write("Equipped Items:")
selected_item = st.radio(label="Item Select", options=found_items, index=None, label_visibility="hidden", key="radio_fonok_retri")

col1, col2 = st.columns(2)
with col1:
    if st.button("Edit", disabled=selected_item is None, key="edit_btn_fonok_retri"):
        st.session_state["editing_fonok_retri"] = selected_item
with col2:
    if st.button("Delete", disabled=selected_item is None, key="delete_btn_fonok_retri"):
        found_items.remove(selected_item)
        github_functions.write_github_file("texts/completed_fonok_retri.txt", found_items)
        st.rerun()

if "editing_fonok_retri" in st.session_state:
    st.text_input("Edit item:",
                  value=st.session_state["editing_fonok_retri"].strip(),
                  on_change=save_edit,
                  key="edit_input_fonok_retri")
    if st.button("Save", key="save_btn_fonok_retri"):
        save_edit()
        st.rerun()