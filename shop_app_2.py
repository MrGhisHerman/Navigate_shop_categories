# app.py
import streamlit as st
import pandas as pd




def filter_data(selected_models, selected_categories, search_query):
    #data
    df =pd.read_csv("data_shops_cat.csv")

    # Apply filters
    filtered_df = df
    if selected_models:
        filtered_df = filtered_df[filtered_df['Model'].isin(selected_models)]
        
    if selected_categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]
        
    if search_query:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_query, case=False)]
        
    #we take the initial df, and filter the shops again. The aim is to get all the possible categories for those shops w.r.t. the selected models.
    list_shops_ = list(filtered_df.Name)
    filtered_df_2 = df
    if selected_models:
        filtered_df_2 = filtered_df_2[filtered_df_2['Model'].isin(selected_models)]
    filtered_df_2 = filtered_df_2[filtered_df_2.Name.isin(list_shops_)]
     
    list_shop_name = []
    list_urls = []
    list_categories_json = []
    list_shop_name_initial = list(set(filtered_df_2.Name))
    
    for name_ in list_shop_name_initial:
        try:
            filtered_df_temp = filtered_df_2[filtered_df_2.Name == name_]
            url = list(filtered_df_temp.URL)[0]
            categories = set(filtered_df_temp.Category)


            list_shop_name.append(name_)
            list_urls.append(url)
            list_categories_json.append(list(categories))   
        except:
            pass
        
    res_df = pd.DataFrame({"Name":list_shop_name, "Category":list_categories_json,"URL":list_urls})
    
    
    return res_df

def main():
    st.title("NAVIGATING THE SHOP CATEGORIES")
    #data
    df =pd.read_csv("data_shops_cat.csv")

    # Sidebar filters
    selected_models = st.sidebar.multiselect("Select Model(s)", df['Model'].unique())
    selected_categories = st.sidebar.multiselect("Select Category(ies)", df['Category'].unique())

    # Main content
    st.subheader("Search and Filter Shops")

    # Search bar with real-time updates
    search_query = st.text_input("Search by Shop Name:", key='search_input')
    
    # Apply filters
    filtered_df = filter_data(selected_models, selected_categories, search_query)

    #drop the duplicates
    #filtered_df = filtered_df.drop_duplicates(subset=['Name', 'URL'])
    filtered_df = filtered_df.drop_duplicates(subset=['Name'])

    
    # Display filtered results
    if not filtered_df.empty:
        #st.dataframe(filtered_df.set_index('Name'))
        
        df_display = filtered_df.copy()
        df_display['Name_c'] = df_display.apply(lambda row: f'<a href="{row["URL"]}" target="_blank">{row["Name"]}</a>', axis=1)

        # Display the DataFrame with clickable links
        #st.write(df_display,unsafe_allow_html=True)


        for index, row in filtered_df.iterrows():
            st.markdown(f"[{row['Name']}]({row['URL']})"+" ".join([f" - {item}" for item in row["Category"]]))
            #st.markdown(str(row["Category"]))
            
            #st.write("<ul>" + "".join([f"<li>{item}</li>" for item in row["Category"]]) + "</ul>", unsafe_allow_html=True)
            #st.markdown(", ".join([f"- {item}" for item in row["Category"]]))
            

            
    else:
        st.warning("No matching shops found.")

if __name__ == "__main__":
    main()
