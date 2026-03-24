import streamlit as st
import functions
import bg_func

bg_func.set_background("images/hunter.jpg", darkness=0.6)

missing_items = functions.get_todos("texts/rudzi.txt")
found_items = functions.get_todos("texts/completed_rudzi.txt")

def save_edit():
    if "editing" in st.session_state and "edit_input" in st.session_state:
        new_value = st.session_state["edit_input"]
        index = found_items.index(st.session_state["editing"])
        found_items[index] = new_value + "\n"
        functions.write_todos(found_items, "texts/completed_rudzi.txt")
        del st.session_state["editing"]

st.title("Rudzi KPOP Demon Hunter BIS Checklist (Midnight Season 1)")

col_input, col_add = st.columns([4, 1])
with col_input:
    st.text_input(label="Enter the item and the dungeon name here to upload your list!",
                  placeholder="e.g. Ring 1 - WORK",
                  key="new_item")
with col_add:
    st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
    if st.button("Add"):
        if st.session_state["new_item"] != "":
            missing_items.append(st.session_state["new_item"] + "\n")
            functions.write_todos(missing_items, "texts/rudzi.txt")
            del st.session_state["new_item"]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("Missing Items:")
for index, missing_item in enumerate(missing_items):
    checkbox = st.checkbox(missing_item, key=f"missing_{index}")
    if checkbox:
        found_items.append(missing_item)
        functions.write_todos(found_items, "texts/completed_rudzi.txt")
        missing_items.pop(index)
        functions.write_todos(missing_items, "texts/rudzi.txt")
        del st.session_state[f"missing_{index}"]
        st.rerun()

st.write("Equipped Items:")
selected_item = st.radio(label="Item Select", options=found_items, index=None, label_visibility="hidden")

col1, col2 = st.columns(2)
with col1:
    if st.button("Edit", disabled=selected_item is None):
        st.session_state["editing"] = selected_item
with col2:
    if st.button("Delete", disabled=selected_item is None):
        found_items.remove(selected_item)
        functions.write_todos(found_items, "texts/completed_rudzi.txt")
        st.rerun()

if "editing" in st.session_state:
    st.text_input("Edit item:",
                  value=st.session_state["editing"].strip(),
                  on_change=save_edit,
                  key="edit_input")
    if st.button("Save"):
        save_edit()
        st.rerun()