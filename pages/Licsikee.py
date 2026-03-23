import streamlit as st
import functions
import bg_func

bg_func.set_background("images\\hunter.jpg", darkness=0.6)

missing_items = functions.get_todos("texts\\licsikee.txt")
found_items = functions.get_todos("texts\\completed_licsikee.txt")

def add_missing_item():
    local_missing_item = st.session_state["new_item"] + "\n"
    missing_items.append(local_missing_item)
    functions.write_todos(missing_items,"texts\\licsikee.txt")
    st.session_state["new_item"] = ""

def save_edit():
    if "editing" in st.session_state and "edit_input" in st.session_state:
        new_value = st.session_state["edit_input"]
        index = found_items.index(st.session_state["editing"])
        found_items[index] = new_value + "\n"
        functions.write_todos(found_items, "texts\\completed_licsikee.txt")
        del st.session_state["editing"]


st.title("Fonok Prot Paladin BIS Checklist (Midnight Season 1)")
st.text_input(label ="Enter the item and the dungeon name here to upload your list!",
              placeholder="e.g. Ring 1 - WORK",
              on_change=add_missing_item,
              key="new_item")
st.write("Missing Items:")

for index, missing_item in enumerate(missing_items):
    checkbox = st.checkbox(missing_item, key=missing_item)
    if checkbox:
        found_items.append(missing_item)
        functions.write_todos(found_items,"texts\\completed_licsikee.txt")
        missing_items.pop(index)
        functions.write_todos(missing_items,"texts\\licsikee.txt" )
        del st.session_state[missing_item]
        st.rerun()

st.write("Equipped Items:")
selected_item = st.radio(label="Item Select",options=found_items, index=None, label_visibility="hidden")

col1, col2 = st.columns(2)

with col1:
    if st.button("Edit", disabled=selected_item is None):
        st.session_state["editing"] = selected_item

with col2:
    if st.button("Delete", disabled=selected_item is None):
        found_items.remove(selected_item)
        functions.write_todos(found_items, "texts\\completed_licsikee.txt")
        st.rerun()

if "editing" in st.session_state:
    st.text_input("Edit item:",
                  value=st.session_state["editing"].strip(),
                  on_change=save_edit,
                  key="edit_input")
    if st.button("Save"):
        save_edit()
        st.rerun()