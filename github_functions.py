import streamlit as st
from github import Github

def get_github_file(filename):
    g = Github(st.secrets["GITHUB_TOKEN"])
    repo = g.get_repo(st.secrets["GITHUB_REPO"])
    contents = repo.get_contents(filename)
    items = contents.decoded_content.decode("utf-8").splitlines(keepends=True)
    return items

def write_github_file(filename, items):
    g = Github(st.secrets["GITHUB_TOKEN"])
    repo = g.get_repo(st.secrets["GITHUB_REPO"])
    contents = repo.get_contents(filename)
    repo.update_file(
        path=filename,
        message=f"Update {filename}",
        content="".join(items),
        sha=contents.sha
    )