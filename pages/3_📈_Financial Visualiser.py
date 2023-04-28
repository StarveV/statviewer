import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from pathlib import Path
from yahooquery import Ticker

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
ticker = st.sidebar.text_input('Enter any ticker to display their financial statistics', 'AAPL')
st.sidebar.write('The current selected ticker is:', ticker.upper()) 
data_selection = st.sidebar.multiselect('Select displayed data', ['Stock Price','Income Statement','Balance Sheet'], default = 'Income Statement') # default='Stock Price'
annual_or_quarter = st.sidebar.radio('Annual or Quarter Data:', ('Annual', 'Quarter '), horizontal=True, index=(0))
if 'Income Statement' in data_selection:
    df_is_select = st.sidebar.radio('Display the source data:', ('Yes', 'No'), horizontal=True, index=(1))
# Display warning if ticker is not found

stock = Ticker(ticker)

# Heading 
st.markdown("##### An interactive financial dash board to display the financial situation of any listed company with an intuitive GUI.") 
st.caption("### The Financial Visualiser does not support ETF, support for the the cash flow statement coming soon.")
st.caption('---')
st.markdown(f'#### The current selected ticker is: {ticker.upper()}')     
st.caption('### Open the side bar to change ticker and settings')
st.caption('### This page is optimized for use with larger screens, making it most effective when accessed via a tablet or PC for an optimal user experience.')

if ticker:
    # Loading screen
    with st.spinner('Retrieving data...'):
        # Get the balance sheet data
        if annual_or_quarter == 'Annual':
            income_stmt = stock.income_statement(frequency='a')
        else:
            income_stmt = stock.income_statement(frequency='q')

        income_stmt = income_stmt.reset_index()
        income_stmt = income_stmt.drop(income_stmt.columns[0], axis=1)
        income_stmt = income_stmt[income_stmt["periodType"] != "TTM"] #weird bug
        income_stmt = income_stmt.set_index(income_stmt.columns[0])
        income_stmt =income_stmt
        income_stmt = income_stmt.transpose()
        income_statement_data = income_stmt

        
        # Income statement dataframe
        data = {
            'Total Revenue': income_statement_data.loc['TotalRevenue'],
            'Cost of revenue': income_statement_data.loc['CostOfRevenue'],
            'Gross profit': income_statement_data.loc['GrossProfit'],
            'Operating expenses': income_statement_data.loc['OperatingExpense'],
            'Operating income': income_statement_data.loc['OperatingIncome'],
            'Interest expense': income_statement_data.loc['NetNonOperatingInterestIncomeExpense'],
            'Other Income Expense': income_statement_data.loc['OtherIncomeExpense'],
            'Other Non Operating Income Expenses': income_statement_data.loc['OtherNonOperatingIncomeExpenses'] if 'OtherNonOperatingIncomeExpenses' in income_statement_data.index else 0,
            'Pretax Income': income_statement_data.loc['PretaxIncome'],
            'Tax Provision': income_statement_data.loc['TaxProvision'],
            'Net income': income_statement_data.loc['NetIncome']
        }

        data=pd.DataFrame(data)
        data = data.rename(columns={'TotalRevenue':'Total Revenue', 
                                    'CostOfRevenue':'Cost of revenue',
                                    'GrossProfit':'Gross profit',
                                    'OperatingExpense': 'Operating expenses',
                                    'OperatingIncome': 'Operating income',
                                    'NetNonOperatingInterestIncomeExpense': 'Interest expense',
                                    'OtherIncomeExpense':'Other Income Expense',
                                    'OtherNonOperatingIncomeExpenses':'Other Non Operating Income Expenses',
                                    'PretaxIncome': 'Pretax Income',
                                    'NetIncome':'Net income'}) 
        data = data.replace('nan', 0)
        data = data.astype(float)
   
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


# display the selected graph.
# Show chart under the option of income statement
if 'Income Statement' in data_selection:
    # Loading screen
    with st.spinner('Generating the dashboard...'):
        # 3 card for total revenue, cost of revenue, net income
        is1,is2, is3 = st.columns(3)
        # Total revenue
        with is1:
            # Calculate the change in value compared to the previous year
            value_change_tr = data['Total Revenue'][-1] - data['Total Revenue'][-2]
            # Calculate the percentage change compared to the previous year
            tr_percent_change = (value_change_tr / data['Total Revenue'][-2]) * 100
            tr_percent_change = round(tr_percent_change,2)

            tr_display = data['Total Revenue'][-1]
            tr_display = format_number(tr_display)
            st.metric("Total Revenue:", tr_display,f"{tr_percent_change}%")
        
        # Cost of revenue
        with is2:
            # Calculate the change in value compared to the previous year
            value_change_cor = data['Cost of revenue'][-1] - data['Cost of revenue'][-2]
            # Calculate the percentage change compared to the previous year
            cor_percent_change = (value_change_cor / data['Cost of revenue'][-2]) * 100
            cor_percent_change = round(cor_percent_change,2)

            cor_display = data['Cost of revenue'][-1]
            cor_display = format_number(cor_display)
            st.metric("Cost of Revenue:", cor_display,f"{cor_percent_change}%")
        
        # Net income
        with is3:
            # Calculate the change in value compared to the previous year
            value_change_ni = data['Net income'][-1] - data['Net income'][-2]
            # Calculate the percentage change compared to the previous year
            ni_percent_change = (value_change_ni / data['Net income'][-2]) * 100
            ni_percent_change = round(ni_percent_change,2)

            ni_display = data['Net income'][-1]
            ni_display = format_number(ni_display)
            st.metric("Net Income:", ni_display,f"{ni_percent_change}%") 
        
        # 4 card for ratios:
        is_ratio1,is_ratio2,is_ratio3,is_ratio4 = st.columns(4)
        with is_ratio1:
            # Gross profit margin
            tr_is = data['Total Revenue'][-1] 
            cogs_is = data['Cost of revenue'][-1]
            GrossMargin_ratio = ((tr_is - cogs_is)/tr_is)* 100
            GrossMargin_ratio = round(GrossMargin_ratio,2)
            # gauge chart of gross margin
            GM_ratio = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = GrossMargin_ratio,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Gross Margin"},
                gauge = {'axis': {'range': [None, 100]}}))

            GM_ratio.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=250,
                autosize=True
            )
            st.plotly_chart(GM_ratio, use_container_width=True)
        
        with is_ratio2:
            # Opersting expense ratio
            ope_is = data['Operating expenses'][-1]
            OPE_ratio = (ope_is/tr_is)* 100
            OPE_ratio = round(OPE_ratio,2)

            # gauge chart of ope
            OPE_ratio = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = OPE_ratio,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "OPE Ratio"},
                gauge = {'axis': {'range': [None, 100]}}
                ))

            OPE_ratio.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=250,
                autosize=True,
                
            )
            st.plotly_chart(OPE_ratio, use_container_width=True)


        with is_ratio3:
            # Operating margin 
            oi_is = data['Operating income'][-1]
            oi_ratio = (oi_is/tr_is)* 100
            op_ratio =round(oi_ratio,2)

            # gauge chart of net profit margin
            op_chart = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = op_ratio,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Operating Margin"},
                gauge = {'axis': {'range': [None, 100]}}
                ))

            op_chart.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=250,
                autosize=True,
                
            )
            st.plotly_chart(op_chart, use_container_width=True)


        with is_ratio4:
            # Net profit margin 
            np_is = data['Net income'][-1]
            np_ratio = (np_is/tr_is)* 100
            np_ratio =round(np_ratio,2)

            # gauge chart of net profit margin
            pm_chart = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = np_ratio,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Net Profit Margin"},
                gauge = {'axis': {'range': [None, 100]}}
                ))

            pm_chart.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=250,
                autosize=True,
                
            )
            st.plotly_chart(pm_chart, use_container_width=True)

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
        
        
        data_plot = data_plot.melt(id_vars='asOfDate', value_vars=['Total Revenue', 'Cost of revenue', 'Gross profit','Operating expenses', 'Operating income','Other Income Expense','Other Non Operating Income Expenses','Net income'])
        if overall_choice == 'Bar ':
            overall_fig_bar = px.bar(data_plot, x='asOfDate', y='value', color='variable', barmode='group', height=350)
            overall_fig_bar.update_layout(
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=0.9),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(overall_fig_bar, use_container_width=True)
        else:
            overall_fig_line = px.area(data_plot, x='asOfDate', y='value', color='variable', height=350)
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
            tr_break_plot = tr_break_plot.melt(id_vars='asOfDate', value_vars=['Cost of revenue','Operating expenses', 'Other Income Expense','Other Non Operating Income Expenses','Tax Provision','Net income'])

            tr_break_bar = px.bar(tr_break_plot, x='asOfDate', y='value', color='variable', barmode='stack', height=350, width=200)
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
            # Doghnut chart for the break down of total revenue
            tr_break_donut = tr_break_plot

            tr_break_donut = px.pie(tr_break_donut, values='value', names='variable', color='variable', hole=0.4, height=400, width=200)
            tr_break_donut.update_layout(
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=0.9),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(tr_break_donut, use_container_width=True)

        # Sankey diagram for income statement
        Gross_profit = income_statement_data.loc['GrossProfit'][1]
        cost_of_revenue = income_statement_data.loc['CostOfRevenue'][1]
        opt_exp = income_statement_data.loc['OperatingExpense'][1]
        opt_income = income_statement_data.loc['OperatingIncome'][1]
        pretax_income = income_statement_data.loc['PretaxIncome'][1]
        interest_exp = income_statement_data.loc['NetNonOperatingInterestIncomeExpense'][1]
        other_nonincome_exp = income_statement_data.loc['OtherIncomeExpense'][1]
        other_non_opt_income_exp = income_statement_data.loc['OtherNonOperatingIncomeExpenses'][1] if 'OtherNonOperatingIncomeExpenses' in income_statement_data.index else 0
        net_income = income_statement_data.loc['NetIncome'][1]
        tax_provision =  income_statement_data.loc['TaxProvision'][1]

        # Sankey diagram for income statement
        df = pd.DataFrame({'From': ['Total Revenue', 'Total Revenue', 'Gross profit', 'Gross profit', 'Operating income', 'Operating income', 'Operating income', 'Operating income', 'Pretax Income', 'Pretax Income'], 
                        'To': ['Gross profit', 'Cost of revenue', 'Operating expenses', 'Operating income', 'Pretax Income', 'Interest expense', 'Other Income Expense', 'Other Non Operating Income Expenses', 'Net income', 'Tax Provision'], 
                        'Value': [Gross_profit, cost_of_revenue, opt_exp, opt_income, pretax_income, interest_exp, other_nonincome_exp, other_non_opt_income_exp, net_income, tax_provision]})

        node_label = df['From'].append(df['To']).unique()
        nodes = [{'label': label} for label in node_label]

        source_indices = df['From'].map(lambda label: node_label.tolist().index(label))
        target_indices = df['To'].map(lambda label: node_label.tolist().index(label))

        sankey = go.Sankey(node=dict(label=node_label,
                                    x=[0.1,0.23,0.4,0.6,0.65,0.45,0.65,0.97,0.65,0.97,0.87],
                                    y=[0.5,0.7,0.6,0.5,0.1,0.8,0.7,0.45,0.8,0.5,0.65]),
                        link=dict(arrowlen=15,
                                    source=source_indices,
                                    target=target_indices,
                                    value=df['Value']))

        layout = go.Layout(width=800, height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

        st.markdown('### Sankey Diagram:')
        st.plotly_chart(go.Figure(data=[sankey], layout=layout)) 

        if df_is_select == 'Yes':
            st.dataframe(income_statement_data)

        st.markdown('---')

if 'Balance Sheet' in data_selection:
    with st.spinner('Retrieving data...'):
        # Get the balance sheet data
        if annual_or_quarter == 'Annual':
            balance_sheet = stock.balance_sheet(frequency='a')
            income_stmt = stock.income_statement(frequency='a')
        else:
            balance_sheet = stock.balance_sheet(frequency='q')
            income_stmt = stock.income_statement(frequency='q')

        balance_sheet = balance_sheet.reset_index()
        balance_sheet = balance_sheet.drop(balance_sheet.columns[0], axis=1)
        balance_sheet = balance_sheet[balance_sheet["periodType"] != "TTM"] #weird bug
        balance_sheet = balance_sheet.set_index(balance_sheet.columns[0])
        balance_sheet = balance_sheet.transpose()

        income_stmt = income_stmt.reset_index()
        income_stmt = income_stmt.drop(income_stmt.columns[0], axis=1)
        income_stmt = income_stmt[income_stmt["periodType"] != "TTM"] #weird bug
        income_stmt = income_stmt.set_index(income_stmt.columns[0])
        income_stmt = income_stmt.transpose()
        
        

        # Get the needed data from the balance sheet
        balance_sheet_data = {
                    'Current Assets': balance_sheet.loc['CurrentAssets'] if 'CurrentAssets' in balance_sheet.index else 0,
                    'Inventory': balance_sheet.loc['Inventory'] if 'Inventory' in balance_sheet.index else 0,
                    'Current Liabilities': balance_sheet.loc['CurrentLiabilities'] if 'CurrentLiabilities' in balance_sheet.index else 0,
                    'Total Cash': balance_sheet.loc['CashCashEquivalentsAndShortTermInvestments'] if 'CashCashEquivalentsAndShortTermInvestments' in balance_sheet.index else 0,
                    'Account Receivables': balance_sheet.loc['AccountsReceivable'] if 'AccountsReceivable' in balance_sheet.index else 0,
                    'Inventory': balance_sheet.loc['Inventory'] if 'Inventory' in balance_sheet.index else 0,
                    'Receivables': balance_sheet.loc['Receivables'] if 'Receivables' in balance_sheet.index else 0,
                    'Other Current Assets': balance_sheet.loc['OtherCurrentAssets'] if 'OtherCurrentAssets' in balance_sheet.index else 0,
                    'Net PPE': balance_sheet.loc['NetPPE'] if 'NetPPE' in balance_sheet.index else 0,
                    'Other Investments': balance_sheet.loc['OtherInvestments'] if 'OtherInvestments' in balance_sheet.index else 0,
                    'Other Non Current Assets': balance_sheet.loc['OtherNonCurrentAssets'] if 'OtherNonCurrentAssets' in balance_sheet.index else 0,
                    'Current Debt': balance_sheet.loc['CurrentDebt'] if 'CurrentDebt' in balance_sheet.index else 0,
                    'Accounts Payable': balance_sheet.loc['AccountsPayable'] if 'AccountsPayable' in balance_sheet.index else 0,
                    'Deferred Revenue': balance_sheet.loc['CurrentDeferredRevenue'] if 'CurrentDeferredRevenue' in balance_sheet.index else 0,
                    'Other Current Liabilities': balance_sheet.loc['OtherCurrentLiabilities'] if 'OtherCurrentLiabilities' in balance_sheet.index else 0,
                    'Long Term Debt': balance_sheet.loc['LongTermDebt'] if 'LongTermDebt' in balance_sheet.index else 0,
                    'Other Non Current Liabilities': balance_sheet.loc['OtherNonCurrentLiabilities'] if 'OtherNonCurrentLiabilities' in balance_sheet.index else 0,
                    'Other Non Current Payables': balance_sheet.loc['TradeandOtherPayablesNonCurrent'] if 'TradeandOtherPayablesNonCurrent' in balance_sheet.index else 0,
                    'Stockholders Equity': balance_sheet.loc['StockholdersEquity'] if 'StockholdersEquity' in balance_sheet.index else 0,
                    'Net Income': income_stmt.loc['NetIncome'] if 'NetIncome' in income_stmt.index else 0,
                    'Total Assets': balance_sheet.loc['TotalAssets'],
                    'Total Debt': balance_sheet.loc['TotalDebt'],

                }    
     
        balance_sheet_data=pd.DataFrame(balance_sheet_data)
        balance_sheet_data=balance_sheet_data
        

        balance_sheet_data = balance_sheet_data.astype(float)

            
        # Quick ratio  
        value_change_quick = balance_sheet_data['Current Assets'][-1] - balance_sheet_data['Inventory'][-1]
        quick_ratio = value_change_quick/balance_sheet_data['Current Liabilities'][-1]
        quick_ratio = round(quick_ratio,2)

        prev_quick_value = balance_sheet_data['Current Assets'][-2] - balance_sheet_data['Inventory'][-2]
        prev_quick = prev_quick_value/balance_sheet_data['Current Liabilities'][-2]
        prev_quick = round(prev_quick,2)
        quick_change = quick_ratio-prev_quick
        quick_change = round(quick_change,2)


        # Extract the quick ratio data for the past 4 years
        quick_ratio_data = {'CurrentAssets': balance_sheet.loc['CurrentAssets'] if 'CurrentAssets' in balance_sheet.index else 0,
                            'Inventory': balance_sheet.loc['Inventory'] if 'Inventory' in balance_sheet.index else 0,
                            'CurrentLiabilities': balance_sheet.loc['CurrentLiabilities'] if 'CurrentLiabilities' in balance_sheet.index else 0,
                            }
        
        quick_ratio_data = pd.DataFrame(quick_ratio_data)
        quick_ratio_data = quick_ratio_data.astype(float)
        quick_ratio_data['QuickRatio'] = (quick_ratio_data['CurrentAssets'] - quick_ratio_data['Inventory'])/quick_ratio_data['CurrentLiabilities']
        
        

        # Define the color palette
        quick_ratio_colour = ['rgb(70, 210, 210)']

        # Create the area graph for current ratio
        quick_ratio_area = px.area(quick_ratio_data, x=quick_ratio_data.index, y='QuickRatio', color_discrete_sequence=quick_ratio_colour)
        quick_ratio_area.update_xaxes(title_text='Date')
        quick_ratio_area.update_yaxes(title_text='Quick Ratio')
        quick_ratio_area.update_layout(
                margin=dict(l=10, r=10, t=10, b=3),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=170,
                width = 100,
                autosize=True
            )         

        
        # Current Ratio
        current_ratio = balance_sheet_data['Current Assets'][-1] / balance_sheet_data['Current Liabilities'][-1] 
        prev_current_ratio = balance_sheet_data['Current Assets'][-2] / balance_sheet_data['Current Liabilities'][-2]
        current_ratio_change = current_ratio-prev_current_ratio

        current_ratio = round(current_ratio,2)
        current_ratio_change = round(current_ratio_change,2) 

        # Extract the current ratio data for the past 4 years
        current_ratio_data = balance_sheet.loc[['CurrentAssets', 'CurrentLiabilities'], :].transpose()
        current_ratio_data = current_ratio_data.astype(float)
        current_ratio_data['CurrentRatio'] = current_ratio_data['CurrentAssets'] / current_ratio_data['CurrentLiabilities']
        current_ratio_data = current_ratio_data.tail(4)


        

        # Define the color palette
        current_ratio_colour = ['rgb(128, 177, 211)']

        # Create the area graph for current ratio
        current_ratio_area = px.area(current_ratio_data, x=current_ratio_data.index, y='CurrentRatio', color_discrete_sequence=current_ratio_colour)
        current_ratio_area.update_xaxes(title_text='Date')
        current_ratio_area.update_yaxes(title_text='Current Ratio')
        current_ratio_area.update_layout(
                margin=dict(l=10, r=10, t=10, b=3),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=170,
                width = 100,
                autosize=True
            )

        # ROE
        roe = balance_sheet_data['Net Income'][-1]/balance_sheet_data['Stockholders Equity'][-1]
        prev_roe = balance_sheet_data['Net Income'][-2]/balance_sheet_data['Stockholders Equity'][-2]
        roe_change = roe-prev_roe

        roe = round(roe,2)
        roe_change = round(roe_change,2)

        # Extract the ROE for the past 4 years
        roe_data = balance_sheet_data['Net Income']/balance_sheet_data['Stockholders Equity']
        
        
        # Create the area graph for ROE
        roe_colour = ['#AEDF9B']
        roe_area = px.area(roe_data, x=roe_data.index, y=roe_data, color_discrete_sequence=roe_colour)
        roe_area.update_xaxes(title_text='Date')
        roe_area.update_yaxes(title_text='ROE')
        roe_area.update_layout(
                margin=dict(l=10, r=10, t=10, b=3),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=170,
                width = 100,
                autosize=True
            )

        # Debt to Asset Ratio
        debt_to_assets = balance_sheet_data['Total Debt'][-1]/balance_sheet_data['Total Assets'][-1]
        prev_debt_to_assets = balance_sheet_data['Total Debt'][-2]/balance_sheet_data['Total Assets'][-2]
        debt_to_assets_change = debt_to_assets-prev_debt_to_assets

        debt_to_assets = round(debt_to_assets,2)
        debt_to_assets_change = round(debt_to_assets_change,2)

        # Extract the Debt to Asset Ratio for the past 4 years
        debt_to_assets_data = balance_sheet_data['Total Debt']/balance_sheet_data['Total Assets']
        
        
        # Create the area graph for Debt to Asset Ratio
        debt_to_assets_colour = ['#DFCF9B']
        debt_to_assets_area = px.area(debt_to_assets_data, x=debt_to_assets_data.index, y=debt_to_assets_data, color_discrete_sequence=debt_to_assets_colour)
        debt_to_assets_area.update_xaxes(title_text='Date')
        debt_to_assets_area.update_yaxes(title_text='Debt to Asset Ratio')
        debt_to_assets_area.update_layout(
                margin=dict(l=10, r=10, t=10, b=3),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=170,
                width = 100,
                autosize=True
            )
        # display card for quick ratio, current ratio, roe, debt to asset ratio
        balance_sheet_metric1, balance_sheet_metric2, balance_sheet_metric3= st.columns(3)
        with balance_sheet_metric1:
            # display card for quick ratio
            st.metric ("Quick Ratio", quick_ratio,quick_change)
        with balance_sheet_metric2:
            # display card for current ratio
            st.metric ("Current Ratio", current_ratio,current_ratio_change)
        with balance_sheet_metric3:
            # display card for ROE
            st.metric("ROE",roe,roe_change)
        

        

        #display the area chart for quick rato and current ratio

        qr_tab,cr_tab,roe_tab,debt_to_assets_tab = st.tabs(["Quick Ratio", "Current Ratio","ROE","Debt to Asset Ratio"])
        with qr_tab:
            st.plotly_chart(quick_ratio_area,use_container_width=True)
        with cr_tab:
            st.plotly_chart(current_ratio_area,use_container_width=True)
        with roe_tab:
            st.plotly_chart(roe_area,use_container_width=True)
        with debt_to_assets_tab:
            st.plotly_chart(debt_to_assets_area,use_container_width=True)
                
        
        # Colour palette
        colors_palette = ['#87bdd8','#daebe8','#cfe0e8','#667292','#77a8a8','#b9b0b0','#e3e0cc','#fefbd8','#fb967f','#e3eaa7']

        # Doghnut Chart for Assets
        asset_doghnut = balance_sheet_data[['Total Cash','Account Receivables','Inventory','Receivables','Other Current Assets','Net PPE','Other Investments','Other Non Current Assets']].reset_index()
        asset_doghnut = asset_doghnut.melt(id_vars='asOfDate', value_vars=['Total Cash','Account Receivables','Inventory','Receivables','Other Current Assets','Net PPE','Other Investments','Other Non Current Assets'])

        asset_doghnut_chart = px.pie(asset_doghnut, values='value', names='variable', color='variable', hole=0.4, 
                                     height=450, width=200, color_discrete_sequence=colors_palette)
        asset_doghnut_chart.update_layout(
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=0.6),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )       


        # Asset break down bar chart
        asset_break_bar = px.bar(asset_doghnut, x='asOfDate', y='value', color='variable', barmode='stack', 
                                 height=350, width=200, color_discrete_sequence=colors_palette)
        asset_break_bar.update_layout(
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=0.9),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            bargap=0.5
        )
        # Assets break down
        asset1, asset2 = st.columns([7,3])
        with asset1:
            st.markdown('### Assets Break Down:')
            st.markdown("Click on the legend to hide any unwanted variables")
            st.plotly_chart(asset_break_bar, use_container_width=True)

        with asset2:
            st.plotly_chart(asset_doghnut_chart, use_container_width=True)

        # Colour palette
        colors_palette2 = ['#A86355','#C18265','#C2B099','#F0DFA7','#D8BB8F','#F2EDE9','#5A5958','#B5BDB9','#F2D0E6','#A0A3D9']
        # Liabilities donut chart
        liabilities_doghnut = balance_sheet_data[['Current Debt','Accounts Payable','Deferred Revenue','Other Current Liabilities','Long Term Debt','Other Non Current Liabilities','Other Non Current Payables','Stockholders Equity']].reset_index()
        liabilities_doghnut = liabilities_doghnut.melt(id_vars='asOfDate', value_vars=['Current Debt','Accounts Payable','Deferred Revenue','Other Current Liabilities','Long Term Debt','Other Non Current Liabilities','Other Non Current Payables','Stockholders Equity'])

        liabilities_doghnut_chart = px.pie(liabilities_doghnut, values='value', names='variable', color='variable', hole=0.4, 
                                     height=450, width=200, color_discrete_sequence=colors_palette2)
        liabilities_doghnut_chart.update_layout(
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=0.6),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
         


        # Liabilities break down bar chart
        liabilities_break_bar = px.bar(liabilities_doghnut, x='asOfDate', y='value', color='variable', barmode='stack', 
                                 height=350, width=200, color_discrete_sequence=colors_palette2)
        liabilities_break_bar.update_layout(
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=0.9),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            bargap=0.5
        )
        # Liabilities break down
        liabilities1, liabilities2 = st.columns([7,3])
        with liabilities1:
            st.markdown('### Liabilities Break Down:')
            st.markdown("Click on the legend to hide any unwanted variables")
            st.plotly_chart(liabilities_break_bar, use_container_width=True)
            

        with liabilities2:    
            st.plotly_chart(liabilities_doghnut_chart, use_container_width=True)


# Stock Price options
if 'Stock Price' in data_selection:
    stock_data = stock.history(period="max")
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
