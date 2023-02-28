from matplotlib import pyplot as plt
import streamlit as st
import seaborn as sns
















# streamlit_app.py

import streamlit as st
import mysql.connector

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from mytable;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")











    



data = sns.load_dataset("penguins")

xvar = "bill_length_mm"
yvar = "body_mass_g"
huevar = "species"

fig = plt.figure()
sns.scatterplot(data=data, x=xvar, y=yvar, hue=huevar, alpha=0.75)
st.pyplot(fig)

def plot_regression(df, x, y, hue, regression=True):
    """Create (colored) scatter plot with optional regression line.
    """
    fig = plt.figure()
    palette = "mako" if hue in df.select_dtypes("number") else None
    sns.scatterplot(data=df, x=x, y=y, hue=hue, alpha=0.75, palette=palette)

    if regression:
        sns.regplot(data=df, x=x, y=y, scatter=False, line_kws={"color": ".3"})

    return fig

fig = plot_regression(data, x=xvar, y=yvar, hue=huevar)
st.pyplot(fig)

numeric_vars = data.select_dtypes("number").columns
if len(numeric_vars) < 1:
    st.warning("No numeric columns found for plotting.")
    st.stop()

leftcol, rightcol = st.columns([2, 1])

with rightcol:  # plot setup selectors on the right
    xvar = st.selectbox("X variable", numeric_vars)
    yvar = st.selectbox("Y variable", numeric_vars, index=len(numeric_vars)-1)

    # hue column is optional - the "None" string is replaced by actual None
    huevar = st.selectbox("Color by", ["None"] + data.columns.tolist())
    if huevar == "None":
        huevar = None

with leftcol:
    fig = plot_regression(data, x=xvar, y=yvar, hue=huevar)
    st.pyplot(fig)


import pandas as pd

@st.cache
def read_data(uploaded_file):
    return pd.read_csv(uploaded_file)


datafile = st.sidebar.file_uploader("Upload dataset", ["csv"])
if datafile is None:
    st.info("""Upload a dataset (.csv) in the sidebar to get started.""")
    st.stop()

data = read_data(datafile).copy()

categories = data.select_dtypes(exclude=["number", "datetime"]).columns
filter_cols = st.sidebar.multiselect("Filter columns", categories)
print(categories)
filters = {}
with st.sidebar.expander("Filters", expanded=True):
    for col in filter_cols:
        options = data[col].dropna().unique()
        selection = st.multiselect(col, options, default=options)
        if selection:
            filters[col] = selection

for col, selection in filters.items():
    data = data.query(f"`{col}` in @selection")
    st.write(f"*`{col}` in {selection}*")
