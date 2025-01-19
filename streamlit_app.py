import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load data
population_data = pd.read_csv('data/population/Statistical table.csv')
unemployment_data = pd.read_csv('data/unemployment/Statistical table.csv')
income_data = pd.read_csv('data/Mean gross income per person (€)/Statistical table.csv')
transactions_data = pd.read_csv('data/number of transactions/Statistical table.csv')
rental_data = pd.read_csv('data/average rental price per area (€_m²)/Statistical table.csv')
transaction_data = pd.read_csv('data/average transaction price per surface area (€_m²)/Statistical table.csv')

# Filter data for districts and Barcelona
population_data = population_data[population_data['Location type'].isin(['Districte', 'Municipi'])]
unemployment_data = unemployment_data[unemployment_data['Location type'].isin(['Districte', 'Municipi'])]
income_data = income_data[income_data['Location type'].isin(['Districte', 'Municipi'])]
transactions_data = transactions_data[transactions_data['Location type'].isin(['Districte', 'Municipi'])]
rental_data = rental_data[rental_data['Location type'].isin(['Districte', 'Municipi'])]
transaction_data = transaction_data[transaction_data['Location type'].isin(['Districte', 'Municipi'])]

# Prepare list of districts including 'Barcelona'
districts = sorted(population_data['Territory'].unique())

st.set_page_config(layout="wide")
st.title('Barcelona Data Analysis')

# Move selection into the sidebar
selected_district = st.sidebar.selectbox('Select District or Municipality', options=districts, key='selected_district')
show_relative_change = st.sidebar.checkbox('Show Relative Change')

# add map to sidebar from 'bcn_map'
st.sidebar.image('data/bcn_map.png', use_container_width=True)

# Function to calculate CAGR
def calculate_cagr(start_value, end_value, periods):
    if periods == 0 or pd.isna(start_value) or pd.isna(end_value) or start_value == 0:
        return np.nan
    else:
        return ((end_value / start_value) ** (1 / periods) - 1) * 100

# Create layout with 2 rows and 3 columns
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)

### Population Analysis ###
with row1_col1:
    st.subheader('Population Development')

    # Get district data
    district_data = population_data[population_data['Territory'] == selected_district]
    # Get Barcelona municipality data
    municipality_data = population_data[population_data['Territory'] == 'Barcelona']

    if not district_data.empty and not municipality_data.empty:
        # Identify the year columns
        columns_to_exclude = ['Territory', 'Location type']
        years = [col for col in district_data.columns if col not in columns_to_exclude]
        district_population_counts = district_data[years].iloc[0].apply(pd.to_numeric, errors='coerce')
        municipality_population_counts = municipality_data[years].iloc[0].apply(pd.to_numeric, errors='coerce')

        # Ensure we have the same years
        common_years = list(set(district_population_counts.index) & set(municipality_population_counts.index))
        common_years.sort(key=lambda x: int(x[-4:]))

        district_population_counts = district_population_counts[common_years]
        municipality_population_counts = municipality_population_counts[common_years]

        # Extract and aggregate data to ensure one data point per year
        common_years = [year[-4:] if ' ' in year else year for year in common_years]
        common_years = sorted(set(common_years), key=int)

        district_population_counts = district_population_counts.groupby(district_population_counts.index.str[-4:]).first()
        municipality_population_counts = municipality_population_counts.groupby(municipality_population_counts.index.str[-4:]).first()

        # Prepare DataFrame
        df_population = pd.DataFrame({
            'Year': common_years,
            selected_district: district_population_counts.values,
            'Barcelona': municipality_population_counts.values
        })

        if show_relative_change:
            # Calculate relative change
            df_population[selected_district] = df_population[selected_district].pct_change() * 100
            df_population['Barcelona'] = df_population['Barcelona'].pct_change() * 100
            y_axis_title = 'Relative Change (%)'
            title_suffix = ' (Relative Change)'
        else:
            y_axis_title = 'Population'
            title_suffix = ''

        # Remove NaN values
        df_population.dropna(inplace=True)

        if not df_population.empty and len(df_population) >= 2:
            
            df_population['Year'] = df_population['Year'].astype(int)
            df_population.sort_values('Year', inplace=True)
            if show_relative_change:
                cagr_text = ''
            else:
                start_value = df_population[selected_district].iloc[0]
                end_value = df_population[selected_district].iloc[-1]
                periods = len(df_population) - 1
                cagr = calculate_cagr(start_value, end_value, periods)

                start_value_bcn = df_population['Barcelona'].iloc[0]
                end_value_bcn = df_population['Barcelona'].iloc[-1]
                cagr_bcn = calculate_cagr(start_value_bcn, end_value_bcn, periods)

            # Include CAGR in the title
            if selected_district == 'Barcelona':
                cagr_text = f'CAGR: {cagr:.2f}%'
            else:
                cagr_text = f'CAGR: {cagr:.2f}% vs Barcelona: {cagr_bcn:.2f}%'
            fig = px.line(df_population, x='Year', y=[selected_district, 'Barcelona'],
                          title=f'Population in {selected_district}{title_suffix}<br>'
                                f'{cagr_text}',
                          labels={'value': y_axis_title})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data available for the selected district and year range.')
    else:
        st.write('No data available for the selected district and year range.')

### Unemployment Analysis ###
with row1_col2:
    st.subheader('Unemployment Development')

    # Get district data
    district_data = unemployment_data[unemployment_data['Territory'] == selected_district]
    # Get Barcelona municipality data
    municipality_data = unemployment_data[unemployment_data['Territory'] == 'Barcelona']

    if not district_data.empty and not municipality_data.empty:
        # Identify the year columns
        columns_to_exclude = ['Territory', 'Location type']
        years = [col for col in district_data.columns if col not in columns_to_exclude]
        district_unemployment = district_data[years].iloc[0].apply(pd.to_numeric, errors='coerce')
        municipality_unemployment = municipality_data[years].iloc[0].apply(pd.to_numeric, errors='coerce')

        # Ensure we have the same years
        common_years = list(set(district_unemployment.index) & set(municipality_unemployment.index))
        common_years.sort(key=lambda x: int(x[-4:]))

        district_unemployment = district_unemployment[common_years]
        municipality_unemployment = municipality_unemployment[common_years]

        # Extract and aggregate data to ensure one data point per year
        common_years = [year[-4:] if ' ' in year else year for year in common_years]
        common_years = sorted(set(common_years), key=int)

        district_unemployment = district_unemployment.groupby(district_unemployment.index.str[-4:]).first()
        municipality_unemployment = municipality_unemployment.groupby(municipality_unemployment.index.str[-4:]).first()

        # Prepare DataFrame
        df_unemployment = pd.DataFrame({
            'Year': common_years,
            selected_district: district_unemployment.values,
            'Barcelona': municipality_unemployment.values
        })

        if show_relative_change:
            # Calculate relative change
            df_unemployment[selected_district] = df_unemployment[selected_district].pct_change() * 100
            df_unemployment['Barcelona'] = df_unemployment['Barcelona'].pct_change() * 100
            y_axis_title = 'Relative Change (%)'
            title_suffix = ' (Relative Change)'
        else:
            y_axis_title = 'Number of Unemployed Persons'
            title_suffix = ''

        # Remove NaN values
        df_unemployment.dropna(inplace=True)

        if not df_unemployment.empty and len(df_unemployment) >= 2:
            df_unemployment['Year'] = df_unemployment['Year'].astype(int)
            df_unemployment.sort_values('Year', inplace=True)
            if show_relative_change:
                cagr_text = ''
            else:
                start_value = df_unemployment[selected_district].iloc[0]
                end_value = df_unemployment[selected_district].iloc[-1]
                periods = len(df_unemployment) - 1
                cagr = calculate_cagr(start_value, end_value, periods)

                start_value_bcn = df_unemployment['Barcelona'].iloc[0]
                end_value_bcn = df_unemployment['Barcelona'].iloc[-1]
                cagr_bcn = calculate_cagr(start_value_bcn, end_value_bcn, periods)

            # Include CAGR in the title
            if selected_district == 'Barcelona':
                cagr_text = f'CAGR: {cagr:.2f}%'
            else:
                cagr_text = f'CAGR: {cagr:.2f}% vs Barcelona: {cagr_bcn:.2f}%'
            fig = px.line(df_unemployment, x='Year', y=[selected_district, 'Barcelona'],
                          title=f'Unemployment in {selected_district}{title_suffix}<br>'
                                f'{cagr_text}',
                          labels={'value': y_axis_title})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data available for the selected district and year range.')
    else:
        st.write('No data available for the selected district and year range.')

### Income Analysis ###
with row1_col3:
    st.subheader('Income Development')

    # Get district data
    district_data = income_data[income_data['Territory'] == selected_district]
    # Get Barcelona municipality data
    municipality_data = income_data[income_data['Territory'] == 'Barcelona']

    if not district_data.empty and not municipality_data.empty:
        # Identify the year columns
        columns_to_exclude = ['Territory', 'Location type']
        years = [col for col in district_data.columns if col not in columns_to_exclude]
        district_income_values = district_data[years].iloc[0].apply(pd.to_numeric, errors='coerce')
        municipality_income_values = municipality_data[years].iloc[0].apply(pd.to_numeric, errors='coerce')

        # Ensure we have the same years
        common_years = list(set(years) & set(years))
        common_years.sort()

        district_income_values = district_income_values[common_years]
        municipality_income_values = municipality_income_values[common_years]

        # Extract and aggregate data to ensure one data point per year
        common_years = [year for year in common_years if year[-4:].isdigit()]
        common_years = sorted(set(common_years), key=int)

        district_income_values = district_income_values.groupby(district_income_values.index.str[-4:]).first()
        municipality_income_values = municipality_income_values.groupby(municipality_income_values.index.str[-4:]).first()

        # Prepare DataFrame
        df_income = pd.DataFrame({
            'Year': common_years,
            selected_district: district_income_values.values,
            'Barcelona': municipality_income_values.values
        })

        if show_relative_change:
            # Calculate relative change
            df_income[selected_district] = df_income[selected_district].pct_change() * 100
            df_income['Barcelona'] = df_income['Barcelona'].pct_change() * 100
            y_axis_title = 'Relative Change (%)'
            title_suffix = ' (Relative Change)'
        else:
            y_axis_title = 'Mean Gross Income (€)'
            title_suffix = ''

        # Remove NaN values
        df_income.dropna(inplace=True)

        if not df_income.empty and len(df_income) >= 2:
            df_income['Year'] = df_income['Year'].astype(int)
            df_income.sort_values('Year', inplace=True)

            if show_relative_change:
                cagr_text = ''
            else:
                start_value = df_income[selected_district].iloc[0]
                end_value = df_income[selected_district].iloc[-1]
                periods = len(df_income) - 1
                cagr = calculate_cagr(start_value, end_value, periods)

                start_value_bcn = df_income['Barcelona'].iloc[0]
                end_value_bcn = df_income['Barcelona'].iloc[-1]
                cagr_bcn = calculate_cagr(start_value_bcn, end_value_bcn, periods)

            # Include CAGR in the title
            if selected_district == 'Barcelona':
                cagr_text = f'CAGR: {cagr:.2f}%'
            else:
                cagr_text = f'CAGR: {cagr:.2f}% vs Barcelona: {cagr_bcn:.2f}%'
            fig = px.line(df_income, x='Year', y=[selected_district, 'Barcelona'],
                          title=f'Income in {selected_district}{title_suffix}<br>'
                                f'{cagr_text}',
                          labels={'value': y_axis_title})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data available for the selected district and year range.')
    else:
        st.write('No data available for the selected district.')

### Transactions Analysis ###
with row2_col1:
    st.subheader('Residential Transactions Volume')

    # Get district data
    district_data = transactions_data[transactions_data['Territory'] == selected_district]
    # Get Barcelona municipality data
    municipality_data = transactions_data[transactions_data['Territory'] == 'Barcelona']

    if not district_data.empty and not municipality_data.empty:
        # Identify the year columns
        columns_to_exclude = ['Territory', 'Location type']
        years = [col for col in district_data.columns if col not in columns_to_exclude]
        district_transactions_counts = district_data[years].iloc[0].apply(pd.to_numeric, errors='coerce')
        municipality_transactions_counts = municipality_data[years].iloc[0].apply(pd.to_numeric, errors='coerce')

        # Ensure we have the same years
        common_years = list(set(years) & set(years))
        common_years.sort()

        district_transactions_counts = district_transactions_counts[common_years]
        municipality_transactions_counts = municipality_transactions_counts[common_years]

        # Extract and aggregate data to ensure one data point per year
        common_years = [year for year in common_years if year[-4:].isdigit()]
        common_years = sorted(set(common_years), key=int)

        district_transactions_counts = district_transactions_counts.groupby(district_transactions_counts.index.str[-4:]).first()
        municipality_transactions_counts = municipality_transactions_counts.groupby(municipality_transactions_counts.index.str[-4:]).first()

        # Ensure all arrays have the same length
        min_length = min(len(common_years), len(district_transactions_counts), len(municipality_transactions_counts))
        common_years = common_years[:min_length]
        district_transactions_counts = district_transactions_counts[:min_length]
        municipality_transactions_counts = municipality_transactions_counts[:min_length]

        # Prepare DataFrame
        df_transactions = pd.DataFrame({
            'Year': common_years,
            selected_district: district_transactions_counts,
            'Barcelona': municipality_transactions_counts
        })

        if show_relative_change:
            # Calculate relative change
            df_transactions[selected_district] = df_transactions[selected_district].pct_change() * 100
            df_transactions['Barcelona'] = df_transactions['Barcelona'].pct_change() * 100
            y_axis_title = 'Relative Change (%)'
            title_suffix = ' (Relative Change)'
        else:
            y_axis_title = 'Number of Transactions'
            title_suffix = ''

        # Remove NaN values
        df_transactions.dropna(inplace=True)

        if not df_transactions.empty and len(df_transactions) >= 2:
            df_transactions['Year'] = df_transactions['Year'].astype(int)
            df_transactions.sort_values('Year', inplace=True)
            
            if show_relative_change:
                cagr_text = ''
            else:
                start_value = df_transactions[selected_district].iloc[0]
                end_value = df_transactions[selected_district].iloc[-1]
                periods = len(df_transactions) - 1
                cagr = calculate_cagr(start_value, end_value, periods)

                start_value_bcn = df_transactions['Barcelona'].iloc[0]
                end_value_bcn = df_transactions['Barcelona'].iloc[-1]
                cagr_bcn = calculate_cagr(start_value_bcn, end_value_bcn, periods)

            # Include CAGR in the title
            if selected_district == 'Barcelona':
                cagr_text = f'CAGR: {cagr:.2f}%'
            else:
                cagr_text = f'CAGR: {cagr:.2f}% vs Barcelona: {cagr_bcn:.2f}%'
            fig = px.line(df_transactions, x='Year', y=[selected_district, 'Barcelona'],
                          title=f'Transactions in {selected_district}{title_suffix}<br>'
                                f'{cagr_text}',
                          labels={'value': y_axis_title})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('No data available for the selected district and year range.')
    else:
        st.write('No data available for the selected district and year range.')

### Transaction Price Analysis ###
with row2_col2:
    st.subheader('Transaction Price Analysis (€/m²)')
    district_data = transaction_data[transaction_data['Territory'] == selected_district]
    municipality_data = transaction_data[transaction_data['Territory'] == 'Barcelona']

    if not district_data.empty and not municipality_data.empty:
        columns_to_exclude = ['Territory', 'Location type']
        years = [col for col in district_data.columns if col not in columns_to_exclude]
        dist_vals = district_data[years].iloc[0].replace('-', np.nan).astype(float)
        muni_vals = municipality_data[years].iloc[0].replace('-', np.nan).astype(float)

        # Determine shared years, sorted
        common_years = list(set(dist_vals.index) & set(muni_vals.index))
        common_years.sort()

        dist_vals = dist_vals[common_years]
        muni_vals = muni_vals[common_years]
        
        # Simplify year labels
        common_years = [year[-4:] if ' ' in year else year for year in common_years]
        common_years = [year for year in common_years if year.isdigit()]
        common_years = sorted(set(common_years), key=int)

        # Group by final 4 digits (handle weird column naming)
        dist_vals = dist_vals.groupby(dist_vals.index.str[-4:]).first()
        muni_vals = muni_vals.groupby(muni_vals.index.str[-4:]).first()

        df_price = pd.DataFrame({
            'Year': dist_vals.index,
            selected_district: dist_vals.values,
            'Barcelona': muni_vals.values
        }).dropna()

        # Basic sanity check on the prices
        # (Just an example: flag anything that looks too low or too high)
        suspicious_district = df_price[(df_price[selected_district] < 500) | (df_price[selected_district] > 20000)]
        suspicious_bcn = df_price[(df_price['Barcelona'] < 500) | (df_price['Barcelona'] > 20000)]

        if not suspicious_district.empty or not suspicious_bcn.empty:
            st.warning("Some transaction price values look suspiciously low or high. Check your data source!")

        if show_relative_change:
            df_price[selected_district] = df_price[selected_district].pct_change() * 100
            df_price['Barcelona'] = df_price['Barcelona'].pct_change() * 100
            y_axis_title = 'Relative Change (%)'
            title_suffix = ' (Relative Change)'
        else:
            y_axis_title = 'Avg. Transaction Price (€/m²)'
            title_suffix = ''

        df_price.dropna(inplace=True)
        if not df_price.empty and len(df_price) >= 2:
            df_price['Year'] = df_price['Year'].astype(int)
            df_price.sort_values('Year', inplace=True)

            if show_relative_change:
                cagr_text = ''
            else:
                start_value = df_price[selected_district].iloc[0]
                end_value = df_price[selected_district].iloc[-1]
                periods = len(df_price) - 1
                cagr = calculate_cagr(start_value, end_value, periods)

                start_value_bcn = df_price['Barcelona'].iloc[0]
                end_value_bcn = df_price['Barcelona'].iloc[-1]
                cagr_bcn = calculate_cagr(start_value_bcn, end_value_bcn, periods)

            cagr_text = (f'CAGR: {cagr:.2f}%' if selected_district == 'Barcelona'
                         else f'CAGR: {cagr:.2f}% vs Barcelona: {cagr_bcn:.2f}%')
            fig = px.line(df_price, x='Year', y=[selected_district, 'Barcelona'],
                          title=f'Transaction Price in {selected_district}{title_suffix}<br>{cagr_text}',
                          labels={'value': y_axis_title})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No transaction price data available for the selected district.")
    else:
        st.write("No transaction price data available for the selected district.")

### ROI Analysis ###
with row2_col3:
    st.subheader('Return on Investment (ROI)')

    # Get rental data
    rental_row_district = rental_data[rental_data['Territory'] == selected_district]
    rental_row_municipality = rental_data[rental_data['Territory'] == 'Barcelona']

    # Get transaction data
    transaction_row_district = transaction_data[transaction_data['Territory'] == selected_district]
    transaction_row_municipality = transaction_data[transaction_data['Territory'] == 'Barcelona']

    if not rental_row_district.empty and not transaction_row_district.empty and not rental_row_municipality.empty and not transaction_row_municipality.empty:
        # Identify the year columns
        columns_to_exclude = ['Territory', 'Location type']
        rental_years = [col for col in rental_row_district.columns if col not in columns_to_exclude]
        transaction_years = [col for col in transaction_row_district.columns if col not in columns_to_exclude]
        common_years = list(set(rental_years) & set(transaction_years))
        common_years.sort()

        # Get data for common years
        rental_prices_district = rental_row_district[common_years].replace('-', np.nan).astype(float).values.flatten()
        transaction_prices_district = transaction_row_district[common_years].replace('-', np.nan).astype(float).values.flatten()

        rental_prices_municipality = rental_row_municipality[common_years].replace('-', np.nan).astype(float).values.flatten()
        transaction_prices_municipality = transaction_row_municipality[common_years].replace('-', np.nan).astype(float).values.flatten()

        # Calculate ROI
        roi_district = (rental_prices_district * 12 / transaction_prices_district) * 100
        roi_municipality = (rental_prices_municipality * 12 / transaction_prices_municipality) * 100

        # Handle possible division by zero or NaNs
        roi_district = np.nan_to_num(roi_district, nan=np.nan, posinf=np.nan, neginf=np.nan)
        roi_municipality = np.nan_to_num(roi_municipality, nan=np.nan, posinf=np.nan, neginf=np.nan)

        df_roi = pd.DataFrame({
            'Year': common_years,
            selected_district: roi_district,
            'Barcelona': roi_municipality
        })

        if show_relative_change:
            # Calculate relative change
            df_roi[selected_district] = df_roi[selected_district].pct_change() * 100
            df_roi['Barcelona'] = df_roi['Barcelona'].pct_change() * 100
            y_axis_title = 'Relative Change (%)'
            title_suffix = ' (Relative Change)'
        else:
            y_axis_title = 'ROI (%)'
            title_suffix = ''

        # Drop rows with NaN or infinite values
        df_roi.replace([np.inf, -np.inf], np.nan, inplace=True)
        df_roi.dropna(inplace=True)

        if not df_roi.empty and len(df_roi) >= 2:
            df_roi['Year'] = df_roi['Year'].astype(int)
            df_roi.sort_values('Year', inplace=True)
            if show_relative_change:
                cagr_text = ''
            else:
                start_value = df_roi[selected_district].iloc[0]
                end_value = df_roi[selected_district].iloc[-1]
                periods = len(df_roi) - 1
                cagr = calculate_cagr(start_value, end_value, periods)

                start_value_bcn = df_roi['Barcelona'].iloc[0]
                end_value_bcn = df_roi['Barcelona'].iloc[-1]
                cagr_bcn = calculate_cagr(start_value_bcn, end_value_bcn, periods)

            # Include CAGR in the title
            if selected_district == 'Barcelona':
                cagr_text = f'CAGR: {cagr:.2f}%'
            else:
                cagr_text = f'CAGR: {cagr:.2f}% vs Barcelona: {cagr_bcn:.2f}%'
            fig = px.line(df_roi, x='Year', y=[selected_district, 'Barcelona'],
                          title=f'ROI in {selected_district}{title_suffix}<br>'
                                f'{cagr_text}',
                          labels={'value': y_axis_title})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No ROI data available for the selected district.")
    else:
        st.write("No ROI data available for the selected district.")