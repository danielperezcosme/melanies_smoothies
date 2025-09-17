# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Pending Smoothie Orders :cup_with_straw: {st.__version__}")
st.write(
  """Orders to be prepared
  """
)


#Show list
from snowflake.snowpark.functions import col 

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:

    my_dataframe_editable = st.data_editor(my_dataframe)
    button_submitted = st.button('Submit')
    
    if button_submitted:
        og_dataset  = session.table("smoothies.public.orders")
        edited_dataset  = session.create_dataframe(my_dataframe_editable)
    
        try:
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
        except:
            st.write('ERROR')


else:    
    st.success('there are no pending orders')
