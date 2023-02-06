import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import time
from pathlib import Path


#  ---- settings ----
page_title = "Financial Visualiser"
page_icon = ":chart_with_upwards_trend:"   #emoji from https://www.webfx.com/tools/emoji-cheat-sheet/ 
layout = "wide" 
#  ----          ----

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.header(page_icon + " " + page_title)

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

# load the style data from css file
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir/"page_style.css"

with open(css_file) as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# Input at sidebar
# Input text box
ticker = st.sidebar.text_input('Enter ant ticker to display their financial statistics', 'AAPL')
st.sidebar.write('The current selected ticker is:', ticker.upper()) 
data_selection = st.sidebar.multiselect('Select displayed data', ['Stock Price','Income Statement'], default = 'Income Statement') # default='Stock Price'
if 'Income Statement' in data_selection:
    df_is_select = st.sidebar.radio('Display the source data:', ('Yes', 'No'), horizontal=True, index=(1))
# Display warning if ticker is not found
try:
    stock = yf.Ticker(ticker)
    # Perform task A here
except Exception as e:
    st.warning('This is a warning', icon="⚠️")

stock_data = stock.history(period="max")

# Heading 
st.markdown("##### An interactive financial dash board to display the financial situation of any listed company with an intuitive GUI.") 
st.caption("### The Financial Visualiser does not support ETF, support for the balance sheet and the cash flow statement coming soon.")
st.caption('---')
st.markdown(f'#### The current selected ticker is: {ticker.upper()}')     
st.caption('### Open the side bar to change ticker and settings')

if ticker:
    # Loading screen
    with st.spinner('Retrieving data...'):
        # Get the balance sheet data
        balance_sheet_data = stock.balance_sheet 
        income_statement_data = stock.income_stmt
        cashflow_data = stock.cash_flow

        # Get the financial data Cant USEEEEEEEEEEEEEEEEEEEEEE
        financial_data = stock.info

        # Income statement dataframe
        data = {
            'Total Revenue': income_statement_data.loc['Total Revenue'],
            'Cost of revenue': income_statement_data.loc['Cost Of Revenue'],
            'Gross profit': income_statement_data.loc['Gross Profit'],
            'Operating expenses': income_statement_data.loc['Operating Expense'],
            'Operating income': income_statement_data.loc['Operating Income'],
            'Interest expense': income_statement_data.loc['Net Non Operating Interest Income Expense'],
            'Other Income Expense': income_statement_data.loc['Other Income Expense'],
            'Other Non Operating Income Expenses': income_statement_data.loc['Other Non Operating Income Expenses'] if 'Other Non Operating Income Expenses' in income_statement_data.index else 0,
            'Pretax Income': income_statement_data.loc['Pretax Income'],
            'Tax Provision': income_statement_data.loc['Tax Provision'],
            'Net income': income_statement_data.loc['Net Income']
        }

        data=pd.DataFrame(data)

def format_number(number):
    if number >= 1000000000:
        return '{:.2f}B'.format(number / 1000000000)
    elif number >= 1000000:
        return '{:.2f}M'.format(number / 1000000)
    elif number >= 1000:
        return '{:.2f}K'.format(number / 1000)
    elif number <= -1000000000:
        return '{:.2f}B'.format(number / 1000000000)
    elif number <= -1000000:
        return '{:.2f}M'.format(number / 1000000)
    elif number <= -1000:
        return '{:.2f}K'.format(number / 1000)
    else:
        return '{:.2f}'.format(number)


# display the selected graph
# Show chart under the option of income statement
if 'Income Statement' in data_selection:
    # Loading screen
    with st.spinner('Generating the dashboard...'):
        # 3 card for total revenue, cost of revenue, net income
        is1,is2, is3 = st.columns(3)
        # Total revenue
        with is1:
            # Calculate the change in value compared to the previous year
            value_change_tr = data['Total Revenue'][0] - data['Total Revenue'][1]
            # Calculate the percentage change compared to the previous year
            tr_percent_change = (value_change_tr / data['Total Revenue'][2]) * 100
            tr_percent_change = round(tr_percent_change,2)

            tr_display = data['Total Revenue'][0]
            tr_display = format_number(tr_display)
            st.metric("Total Revenue:", tr_display,f"{tr_percent_change}%")
        
        # Cost of revenue
        with is2:
            # Calculate the change in value compared to the previous year
            value_change_cor = data['Cost of revenue'][0] - data['Cost of revenue'][1]
            # Calculate the percentage change compared to the previous year
            cor_percent_change = (value_change_cor / data['Cost of revenue'][2]) * 100
            cor_percent_change = round(cor_percent_change,2)

            cor_display = data['Cost of revenue'][0]
            cor_display = format_number(cor_display)
            st.metric("Cost of Revenue:", cor_display,f"{cor_percent_change}%")
        
        # Net income
        with is3:
            # Calculate the change in value compared to the previous year
            value_change_ni = data['Net income'][0] - data['Net income'][1]
            # Calculate the percentage change compared to the previous year
            ni_percent_change = (value_change_ni / data['Net income'][2]) * 100
            ni_percent_change = round(ni_percent_change,2)

            ni_display = data['Net income'][0]
            ni_display = format_number(ni_display)
            st.metric("Net Income:", ni_display,f"{ni_percent_change}%")

        # Income Statement at a Glance
        # 2 Columns for overall chart
        tr4, tr5,tr6 =st.columns([2,1,1])
        with tr4:
            st.markdown("### Income Statement at a Glance: ")
            st.markdown("Click on the legend to hide any unwanted variables")
        with tr5:
            st.markdown(' ')
            st.markdown(' ')
            overall_choice = st.radio('Choose a graph type ', ('Bar ', 'Area '), horizontal=True)

        data_plot = data[['Total Revenue', 'Cost of revenue', 'Gross profit','Operating expenses', 'Operating income','Other Income Expense','Other Non Operating Income Expenses','Net income']].reset_index()
        data_plot = data_plot.melt(id_vars='index', value_vars=['Total Revenue', 'Cost of revenue', 'Gross profit','Operating expenses', 'Operating income','Other Income Expense','Other Non Operating Income Expenses','Net income'])
        if overall_choice == 'Bar ':
            overall_fig_bar = px.bar(data_plot, x='index', y='value', color='variable', barmode='group', height=350)
            overall_fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(overall_fig_bar, use_container_width=True)
        else:
            overall_fig_line = px.area(data_plot, x='index', y='value', color='variable', height=350)
            overall_fig_line.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(overall_fig_line, use_container_width=True)

        # Diagram for total revenue break down
        # Stack bar chart for total revenue
        trbd1, trbd2 = st.columns([7,3])
        with trbd1:
            # Total revenue break down
            st.markdown('### Total Revenue Break Down:')
            st.markdown("Click on the legend to hide any unwanted variables")
            tr_break_plot = data[['Cost of revenue','Operating expenses','Other Income Expense','Other Non Operating Income Expenses','Tax Provision','Net income']].reset_index()
            tr_break_plot = tr_break_plot.melt(id_vars='index', value_vars=['Cost of revenue','Operating expenses', 'Other Income Expense','Other Non Operating Income Expenses','Tax Provision','Net income'])

            tr_break_bar = px.bar(tr_break_plot, x='index', y='value', color='variable', barmode='stack', height=350, width=200)
            tr_break_bar.update_layout(
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=0.9),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                bargap=0.5
            )
            st.plotly_chart(tr_break_bar, use_container_width=True)

        with trbd2:
            st.markdown(' ')
            st.markdown(' ')
            st.markdown(' ')
            # Doughnut chart for the break down of total revenue
            tr_break_donut = tr_break_plot

            tr_break_donut = px.pie(tr_break_donut, values='value', names='variable', color='variable', hole=0.4, height=400, width=200)
            tr_break_donut.update_layout(
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=0.9),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(tr_break_donut, use_container_width=True)

        # Sankey diagram for income statement
        Gross_profit = income_statement_data.loc['Gross Profit'][1]
        cost_of_revenue = income_statement_data.loc['Cost Of Revenue'][1]
        opt_exp = income_statement_data.loc['Operating Expense'][1]
        opt_income = income_statement_data.loc['Operating Income'][1]
        pretax_income = income_statement_data.loc['Pretax Income'][1]
        interest_exp = income_statement_data.loc['Net Non Operating Interest Income Expense'][1]
        other_nonincome_exp = income_statement_data.loc['Other Income Expense'][1]
        other_non_opt_income_exp = income_statement_data.loc['Other Non Operating Income Expenses'][1] if 'Other Non Operating Income Expenses' in income_statement_data.index else 0
        net_income = income_statement_data.loc['Net Income'][1]
        tax_provision =  income_statement_data.loc['Tax Provision'][1]

        # Sankey diagram for income statement
        df = pd.DataFrame({'From': ['Total Revenue', 'Total Revenue', 'Gross profit', 'Gross profit', 'Operating income', 'Operating income', 'Operating income', 'Operating income', 'Pretax Income', 'Pretax Income'], 
                        'To': ['Gross profit', 'Cost of revenue', 'Operating expenses', 'Operating income', 'Pretax Income', 'Interest expense', 'Other Income Expense', 'Other Non Operating Income Expenses', 'Net income', 'Tax Provision'], 
                        'Value': [Gross_profit, cost_of_revenue, opt_exp, opt_income, pretax_income, interest_exp, other_nonincome_exp, other_non_opt_income_exp, net_income, tax_provision]})

        node_label = df['From'].append(df['To']).unique()
        nodes = [{'label': label} for label in node_label]

        source_indices = df['From'].map(lambda label: node_label.tolist().index(label))
        target_indices = df['To'].map(lambda label: node_label.tolist().index(label))

        sankey = go.Sankey(node=dict(label=node_label,
                                    x=[0.1,0.23,0.4,0.6,0.65,0.45,0.65,0.65,0.65,0.97,0.87],
                                    y=[0.5,0.7,0.6,0.5,0.1,0.8,0.7,0.75,0.8,0.5,0.65]),
                        link=dict(arrowlen=15,
                                    source=source_indices,
                                    target=target_indices,
                                    value=df['Value']))

        layout = go.Layout(width=800, height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

        st.markdown('### Sankey Diagram:')
        st.plotly_chart(go.Figure(data=[sankey], layout=layout)) 

        if df_is_select == 'Yes':
            st.dataframe(income_statement_data)




# Stock Price options
if 'Stock Price' in data_selection:
    # Loading screen
    with st.spinner('Generating the dashboard...'):
        st.markdown('### Stock Price History:')
        # Create a date selector to select start and end date
        start_date = st.sidebar.date_input("Start date", stock_data.index[0], min_value=stock_data.index[0], max_value=stock_data.index[-1])
        end_date = st.sidebar.date_input("End date", stock_data.index[-1], min_value=stock_data.index[0], max_value=stock_data.index[-1])
        #---------
        stock_data = stock_data[start_date:end_date]

        # Display candle stick chart
        fig_candlestick = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                                        open=stock_data['Open'],
                                                        high=stock_data['High'],
                                                        low=stock_data['Low'],
                                                        close=stock_data['Close'])])
        fig_candlestick.update_layout(title=f"{ticker} Stock Price", width=800,plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')
        #-----------
        # create a toggle button to switch between bar, candle and line graph
        graph_type = st.radio('Choose a graph type', ('Candle Stick', 'Line'), horizontal=True)
        if graph_type == 'Candle Stick':
            st.plotly_chart(fig_candlestick)
        else:
            fig_line = px.line(stock_data, x=stock_data.index, y='Close', title=f"{ticker} Stock Price")
            fig_line.update_layout(title=f"{ticker} Stock Price", width=800,plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_line)
        
        # Calculate the 1 day change
        close_1d = stock_data['Close'].iloc[-1]
        close_prev_1d = stock_data['Close'].iloc[-2]
        pct_change_1d = (close_1d - close_prev_1d) / close_prev_1d

        # Calculate the 1 month change
        close_1m = stock_data['Close'].iloc[-1]
        close_prev_1m = stock_data['Close'].iloc[-30]
        pct_change_1m = (close_1m - close_prev_1m) / close_prev_1m

        # Calculate the YTD change
        close_ytd = stock_data['Close'].iloc[-1]
        close_prev_ytd = stock_data['Close'][stock_data.index.year == stock_data.index[-1].year].iloc[0]
        pct_change_ytd = (close_ytd - close_prev_ytd) / close_prev_ytd

        # Round the numbers to 1 decimal place
        pct_change_1d = round(pct_change_1d * 100, 2)
        pct_change_1m = round(pct_change_1m * 100, 2)
        pct_change_ytd = round(pct_change_ytd * 100, 2) 

        close_1d = round(close_1d)
        change_1m = round((close_1m - close_prev_1m))
        change_ytd= round((close_ytd - close_prev_ytd))

        col1, col2, col3 = st.columns(3)
        col1.metric("Closed Price:", close_1d, f"{pct_change_1d}%")
        col2.metric("1M Price Change:", f"{'+' if change_1m > 0 else '-'}{change_1m}", f"{pct_change_1m}%")
        col3.metric("YTD Price Change:", f"{'+' if change_ytd > 0 else '-'}{change_ytd}", f"{pct_change_ytd}%")
