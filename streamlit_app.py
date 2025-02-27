# Import python packages
import streamlit as st
#removing next to change from SnowFlake to streamlit og
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

websiteToUse = "https://my.smoothiefroot.com/api/fruit/"


# Write directly to the app
st.title(":cocktail: Customise Your Smoothie!" )
st.write(
    """Choose the fruits you want in your custom Smoothie!!!!
    """
)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#have is as pandas
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)




if ingredients_list:

    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        smoothiefroot_response = requests.get(websiteToUse + search_on)
        sf_df_A = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    ingredients_string = ingredients_string[:-1]
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
