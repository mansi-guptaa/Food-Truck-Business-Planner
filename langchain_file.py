from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import streamlit as st


llm = AzureChatOpenAI(
    deployment_name = st.secrets['AZURE_DEPLOYEMENT'] , # Azure deployment name                 
    azure_endpoint =  st.secrets['AZURE_ENDPOINT'],  # Your Azure endpoint
    api_key = st.secrets['AZURE_OPENAI_API_KEY'],          # API key from Azure portal
    api_version = st.secrets['AZURE_API_VERSION'] # Use the correct API version
)



def generate_truckname_menu_location(cuisine, theme, budget, location):

  # Prompt for generating a food truck name
    name_prompt = PromptTemplate(
        input_variables=["cuisine", "theme"],
        template="""
            Generate a creative name for a {cuisine} food truck for a {theme} theme.
            Only food truck name, no description.
            Use icons if relevant.
        """
    )

    # Prompt for designing a menu
    menu_prompt = PromptTemplate(
        input_variables=["cuisine", "budget"],
        template="""
            Design a menu for a {cuisine} food truck within a {budget} budget.
            Use INR and rupee symbol. 
            Don't give any header only subheader for menu.
            Output in well presentable markdown.
        """
    )

    # Prompt for suggesting locations
    location_prompt = PromptTemplate(
        input_variables=["cuisine", "target_location"],
        template="""
            Suggest the best locations for a {cuisine} food truck in {target_location}.
        """
    )


        # Chains for each task
    name_chain = LLMChain(llm=llm, prompt=name_prompt, output_key = "truck_name")
    menu_chain = LLMChain(llm=llm, prompt=menu_prompt, output_key = "menu")
    location_chain = LLMChain(llm=llm, prompt=location_prompt, output_key = "location")


        # Combining them into a sequential chain
    food_truck_chain = SequentialChain(
        chains=[name_chain, menu_chain, location_chain],
        input_variables=["cuisine", "theme", "budget", "target_location"],
        output_variables=["truck_name", "menu", "location"]
    )

    response = food_truck_chain({'cuisine': cuisine, 'theme': theme, 'budget': budget, 'target_location': location })

    return response

# if __name__ == "__main__":
    
#     print(generate_truckname_menu_location("Korean", "Summer Party", 5000, "Delhi"))
