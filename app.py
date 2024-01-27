import streamlit as st
import calendar
from datetime import datetime
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import database as db
import pandas as pd

#-----------------------------SETTING PAGE-------------------------------------
page_title = "INCOME & EXPENSE TRACKER"
page_icon = ":money_with_wings:"
layout = "centered"

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title(page_icon + " " + page_title + " " + page_icon)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#---------------------------------SETTING VARIABLES---------------------------------------------

years = [datetime.today().year-2,datetime.today().year-1,datetime.today().year,datetime.today().year+1]
months = list(calendar.month_name[1:])
incomes = ["Salary"]
expenses = ["Rent","EMIs","Miscellaneous","Mutual Funds","Stocks","RD","PPF"]

selected = option_menu(
    menu_title=None,
    options=["Data Entry","Visualization","Content"],
    icons = ["pencil-fill","bar-chart-fill","pencil-fill"],
    orientation="horizontal"
)

def get_all_periods():
    items = db.fetch_all_records()
    periods = [item["key"][0] for item in items]
    return periods

if selected == "Data Entry":
    with st.form("Entry Form",clear_on_submit=True):
        col1,col2 = st.columns(2)
        col1.selectbox("Select Months",months,key="month")
        col2.selectbox("Select Year",years,key="year")

        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:",min_value=0,step = 10,format="%i",key=income)

        with st.expander("Expense"):
            for expense in expenses:
                st.number_input(f"{expense}:",min_value=0,step = 10,format="%i",key=expense)

        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Enter a comment here ...")

        st.markdown(
        """
        <style>
            div[data-testid="stFormSubmitButton"] {
                display: flex;
                justify-content: center;
            }
        </style>
        """,
        unsafe_allow_html=True)

        submitted = st.form_submit_button("Save Data")

        if submitted:
            period = [str(st.session_state["year"]) + "_" + str(st.session_state["month"])]
            incomes = {income : st.session_state[income] for income in incomes}
            expenses = {expense : st.session_state[expense] for expense in expenses}
            db.insert_data(period,incomes,expenses,comment)
            st.success("Succesfully added data to the database")


if selected == "Visualization":
    st.header("Visualization")
    with st.form("saved_periods"):
        period = st.selectbox("Select_Period : ", get_all_periods())
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            period_data = db.get_period(period)
            comment = period_data.get("comment")
            expenses = period_data.get("expenses")
            incomes = period_data.get("incomes")

            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income-total_expense

            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())

            link = dict(source=source,target=target,value=value)
            node = dict(label=label,pad=20,thickness=30,color="#E694FF")
            data = go.Sankey(link=link,node=node)

            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0,r=0,t=0,b=5))
            st.plotly_chart(fig,use_container_width=True)

if selected == "Content":
    st.header("Records")
    period = st.selectbox("Select_Period : ", get_all_periods())
    items = db.fetch_all_records()
    for item in items:
        df = pd.DataFrame.from_dict(item,orient='index').T
        # df = df.drop('_id', axis=1, errors='ignore')
        st.table(df)

    col1,col2 = st.columns(2)
    delete = col1.button("Delete")
    update = col2.button("Update")

    if delete:
        period = db.delete(period)
    if update:
        pass