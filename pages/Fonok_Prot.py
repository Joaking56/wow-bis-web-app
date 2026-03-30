import streamlit as st
import github_functions
import bg_func

bg_func.set_background("images/prot.jpg", darkness=0.6)

# ✅ Csak egyszer tölti be a GitHub API-ból
if "missing_items_fonok_prot" not in st.session_state:
    st.session_state["missing_items_fonok_prot"] = github_functions.get_github_file("texts/fonok_prot.txt")
if "found_items_fonok_prot" not in st.session_state:
    st.session_state["found_items_fonok_prot"] = github_functions.get_github_file("texts/completed_fonok_prot.txt")

missing_items = st.session_state["missing_items_fonok_prot"]
found_items = st.session_state["found_items_fonok_prot"]

def clear_all():
    for i in range(len(missing_items) + 1):
        if f"missing_fonok_prot_{i}" in st.session_state:
            del st.session_state[f"missing_fonok_prot_{i}"]
    if "missing_items_fonok_prot" in st.session_state:
        del st.session_state["missing_items_fonok_prot"]
    if "found_items_fonok_prot" in st.session_state:
        del st.session_state["found_items_fonok_prot"]

def save_edit():
    if "editing_fonok_prot" in st.session_state and "edit_input_fonok_prot" in st.session_state:
        new_value = st.session_state["edit_input_fonok_prot"]
        index = found_items.index(st.session_state["editing_fonok_prot"])
        found_items[index] = new_value + "\n"
        github_functions.write_github_file("texts/completed_fonok_prot.txt", found_items)
        del st.session_state["editing_fonok_prot"]
        del st.session_state["found_items_fonok_prot"]

st.title("Fonokvagyok Prot BIS Checklist (Midnight Season 1)")

col_input, col_add = st.columns([4, 1])
with col_input:
    st.text_input(label="Enter the item and the dungeon name here to upload your list!",
                  placeholder="e.g. Ring 1 - WORK",
                  key="new_item_fonok_prot")
with col_add:
    st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
    if st.button("Add", key="add_fonok_prot"):
        if st.session_state["new_item_fonok_prot"] != "":
            missing_items.append(st.session_state["new_item_fonok_prot"] + "\n")
            github_functions.write_github_file("texts/fonok_prot.txt", missing_items)
            del st.session_state["missing_items_fonok_prot"]  # ✅ cache törlés
            del st.session_state["new_item_fonok_prot"]  # ✅ input törlés
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("Missing Items:")
for index, missing_item in enumerate(missing_items):
    checkbox = st.checkbox(missing_item, key=f"missing_fonok_prot_{index}")
    if checkbox:
        found_items.append(missing_item)
        github_functions.write_github_file("texts/completed_fonok_prot.txt", found_items)
        missing_items.pop(index)
        github_functions.write_github_file("texts/fonok_prot.txt", missing_items)
        clear_all()  # ✅ minden törlése
        st.rerun()

st.write("Equipped Items:")
selected_item = st.radio(label="Item Select", options=found_items, index=None, label_visibility="hidden", key="radio_fonok_prot")

col1, col2 = st.columns(2)
with col1:
    if st.button("Edit", disabled=selected_item is None, key="edit_btn_fonok_prot"):
        st.session_state["editing_fonok_prot"] = selected_item
with col2:
    if st.button("Delete", disabled=selected_item is None, key="delete_btn_fonok_prot"):
        found_items.remove(selected_item)
        github_functions.write_github_file("texts/completed_fonok_prot.txt", found_items)
        del st.session_state["found_items_fonok_prot"]  # ✅ cache törlés
        st.rerun()

if "editing_fonok_prot" in st.session_state:
    st.text_input("Edit item:",
                  value=st.session_state["editing_fonok_prot"].strip(),
                  on_change=save_edit,
                  key="edit_input_fonok_prot")
    if st.button("Save", key="save_btn_fonok_prot"):
        save_edit()
        st.rerun()