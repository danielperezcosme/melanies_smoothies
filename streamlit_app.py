# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize your Smoothie App :cup_with_straw: {st.__version__}")
st.write(
  """Customize your Smoothie
  **Check the fruits wanted in it!!!** 
  """
)


#Name of Smoothie - Order
name_of_order = st.text_input('Name of Smoothie')
st.write('The name of your Smoothie - Order will be: ',name_of_order)


# List of ingredients

from snowflake.snowpark.functions import col 

 
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe, max_selections=5)





if ingredients_list:

    ingredients_String = ''

    for fruits_chosen in ingredients_list:
        ingredients_String = ingredients_String + fruits_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruits_chosen,' is ', search_on, '.')

        st.subheader(fruits_chosen + " nutrition information")
        smoothiefroot_response = requests.get("https://my.fruityvice.com/api/fruit/" + search_on ) 
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

    #st.write(ingredients_String)

    my_insert_stmt = """insert into smoothies.public.orders(name_on_order,ingredients) 
                      values ('""" + name_of_order + """',   
                              '""" + ingredients_String + """'
                              )""" 
    
    #st.write(my_insert_stmt)
    time_to_insert = st.button('submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



