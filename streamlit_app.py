# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(":cup_with_straw: Example Streamlit App :cup_with_straw:")
st.write(
    """Choose Your own Smoothie.
    """
)

name_on_order = st.text_input('Name on Order:')
st.write('Your name on the order will be :',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'), col('SEARCH_ON') )
#st.my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'), col('SEARCH_ON') )
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()                               


ingredients_list = st.multiselect(
    "Choose upto 5 ingredients"
    ,my_dataframe
    ,max_selections=5)

ingredients_string = ''

if ingredients_list:
    ingredients_string = ''

for fruits_chosen in ingredients_list:
    ingredients_string += fruits_chosen + ' '
    
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruits_chosen,' is ', search_on, '.')

    st.subheader(fruits_chosen + ' Nutrition Information')
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruits_chosen)
    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    
#st.write(ingredients_string)


my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#st.write(my_insert_stmt)

#st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order') 
if time_to_insert:

        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+ ' ' + name_on_order, icon="✅")
   


