# --- Import Packages --- #
import asyncio
from datetime import datetime
import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from duckduckgo_search import DDGS
from geopy.geocoders import Nominatim
import requests
from prophet import Prophet
import streamlit as st
from streamlit_folium import st_folium
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies import (
    KernelFunctionSelectionStrategy,
    KernelFunctionTerminationStrategy
)
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents import ChatHistoryTruncationReducer
from semantic_kernel.functions import KernelFunctionFromPrompt, kernel_function
from semantic_kernel.kernel import Kernel

# --- Constants --- #
LOCATION_IDENTIFIER = "LocationIdentifier"
DATA_ANALYST = "DataAnalyst"
TERMINATION_KEYWORD = "yes"

# --- Semantic Kernel Setup --- #
def create_kernel() -> Kernel:
    """Creates a Kernel instance with an OpenAI ChatCompletion service."""
    kernel = Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            api_key=st.secrets["openai"]["api_key"],
            ai_model_id="gpt-4o-mini"
        )
    )
    return kernel

class DuckDuckGoSearchPlugin:
    """DuckDuckGo search plugin with automatic query generation based on lat/lon."""

    def __init__(self):
        self.geolocator = Nominatim(user_agent="agricultural_agentic_ai_app")

    @kernel_function(
        name="DuckDuckGoSearch",
        description="Search the web using DuckDuckGo for local climate, agriculture regulations, and market demand."
    )
    async def search(self, lat: float, lon: float) -> str:
        # Reverse geocode to get location details
        location = self.geolocator.reverse((lat, lon), language="en")
        if location is None:
            return "Unable to determine location from coordinates."

        address = location.raw.get("address", {})
        country = address.get("country", "")
        region = (
            address.get("state")
            or address.get("province")
            or address.get("region")
            or address.get("county")
            or address.get("district")
            or ""
        )

        # If neither country nor region is available, do not proceed
        if not country and not region:
            return "Unable to determine country or region from coordinates. Cannot perform search."

        region_prefix = f"{region}, " if region else ""
        location_name = location.address

        queries = [
            f"current climate in {region_prefix}{country}",
            f"agricultural regulations in {region_prefix}{country}",
            f"recommended crops and agricultural market demand in {region_prefix}{country}"
        ]

        results = []
        with DDGS() as ddgs:
            for query in queries:
                search_results = ddgs.text(query, max_results=3)
                if search_results:
                    formatted = "\n\n".join([
                        f"**{r['title']}**\n{r['body']}\n{r['href']}"
                        for r in search_results
                    ])
                    results.append(f"### Search Results for '{query}':\n{formatted}")
                else:
                    results.append(f"No results found for '{query}'.")

        return f"**Resolved location:** {location_name}\n\n" + "\n\n".join(results)

# --- NASA Data Plugin --- #
class NASADataPlugin:
    """Plugin for fetching NASA soil moisture data."""
    def __init__(self, lat: str, lon: str, parameter: str):
        self._lat = lat
        self._lon = lon
        self._parameter = parameter
        
    @kernel_function(
        name="NASADataRetriever",
        description="Fetch daily soil moisture data from NASA POWER API given latitude, longitude, and parameter name."
    )
    async def fetch_soil_moisture(self, lat: float, lon: float, parameter: str) -> dict:
        """Fetch soil moisture data from NASA POWER API."""
        start_date = "19810101"
        end_date = datetime.now().strftime("%Y%m%d")
        url = (
            f"https://power.larc.nasa.gov/api/temporal/daily/point?"
            f"parameters={parameter}&community=ag&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"
        )
        response = requests.get(url)
        if response.ok:
            data = response.json()['properties'].get('parameter', {})
            df = pd.DataFrame.from_dict(data).replace(-999, np.nan)
            df.index = pd.to_datetime(df.index, format='%Y%m%d')
            df_prophet = df[[parameter]].reset_index()
            df_prophet.columns = ['ds', 'y']
            model = Prophet(weekly_seasonality=False, yearly_seasonality=True)
            model.fit(df_prophet)
            future = model.make_future_dataframe(periods=365)
            forecast = model.predict(future)
            forecast_year = forecast.tail(365)
            forecast_year_data = forecast_year[['ds', 'yhat']]
            return dict(zip(forecast_year_data['ds'], forecast_year_data['yhat']))

# --- Asynchronous wrapper --- #
async def stream_response(chat):
    responses = []
    async for reply in chat.invoke():
        if reply:
            responses.append((reply.name, reply.content))
    return responses

# --- Streamlit Interface --- #
st.set_page_config(layout="wide")
st.title("🌾 Agricultural Agentic AI")
st.write("### Select a location on the map")
map = folium.Map(location=[20, 0], zoom_start=2)
map_data = st_folium(map, width=1200, height=600, returned_objects=["last_clicked"])
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    parameter = "GWETROOT"
    with st.spinner("Thinking..."):
        if "chat" not in st.session_state:
            kernel = create_kernel()
            search_results = DuckDuckGoSearchPlugin()
            kernel.add_plugin(search_results)
            data = NASADataPlugin(lat, lon, parameter)
            kernel.add_plugin(data)
            agent_location_identifier = ChatCompletionAgent(
                kernel=kernel,
                name=LOCATION_IDENTIFIER,
                instructions=f"""
You are a real-time research agent with access to the DuckSearch plugin.

To search for information, call:
DuckSearch.search({lat}, {lon})

Given the coordinates ({lat}, {lon}), your job is to:
- Use DuckSearch to search for current climate conditions.
- Use DuckSearch to search for agricultural regulations.
- Use DuckSearch to search for recommended crops and local agricultural market demand.

If DuckSearch reports 'unable to determine location' or no results for a query, explain this clearly in your response.

Always organize your findings into 4 sections:
1. Location and Climate Overview
2. Recent Climate or Environmental News
3. Agricultural Regulations
4. Best Crops to Grow and Local Demand Insights

Start each section with a heading. Always attribute findings as coming from DuckSearch results or state if they’re general knowledge due to missing data.

End your response with a summary recommendation on what the user should focus on agriculturally based on the findings.
"""
            )
            agent_data_analyst = ChatCompletionAgent(
                kernel=kernel,
                name=DATA_ANALYST,
                instructions="""
You are an agricultural soil moisture data analyst.

You have access to forecasted soil moisture data for the next 365 days through the NASADataPlugin.
The forecast is based on the 'GWETROOT' parameter (Moisture from the surface to 100 cm below the surface), processed using a time series model.

Your tasks are:
- Retrieve the forecasted daily soil moisture data (date and predicted value).
- Analyze the forecast trends over the next 12 months.

When analyzing the forecast:
- Interpret soil moisture patterns without mentioning the specific numerical values.
- Consider soil moisture as "too low" if the forecasted value is below 0.2.
- Consider soil moisture as "too high" if the forecasted value is above 0.6.
- Speak entirely in future tense when describing soil conditions.

Based on the analysis:
- Identify upcoming periods of dryness or drought risk if the soil moisture is predicted to be too low.
- Identify upcoming periods of saturation or flood risk if the soil moisture is predicted to be too high.
- Detect general trends such as increasing, decreasing, or stable soil moisture over time.

When giving recommendations:
- Offer practical irrigation strategies if dryness is expected.
- Offer drainage or water management strategies if excessive moisture is expected.
- Provide gardening and farming advice based on the projected soil moisture conditions.

If the forecast data is unavailable or insufficient to determine a trend, politely inform the user without making assumptions.

Always base your advice on the patterns observed in the forecasted data, and use clear, actionable language suitable for farmers.
"""
            )
            selection_function = KernelFunctionFromPrompt(
                function_name="select",
                prompt=f"""
Examine the provided RESPONSE and choose the next participant.
State only the name of the chosen participant without explanation.
Never choose the participant named in the RESPONSE.

Choose only from these participants:
- {LOCATION_IDENTIFIER}
- {DATA_ANALYST}

Rules:
- If RESPONSE is from user, it is {LOCATION_IDENTIFIER}'s turn.
- If RESPONSE is from {LOCATION_IDENTIFIER}, it is {DATA_ANALYST}'s turn.
- If RESPONSE is from {DATA_ANALYST}, it is {LOCATION_IDENTIFIER}'s turn.

RESPONSE:
{{{{$lastmessage}}}}
"""
            )
            termination_function = KernelFunctionFromPrompt(
                function_name="terminate",
                prompt=f"""
Examine the RESPONSE and determine whether the conversation is complete.
If complete, respond only with the keyword {TERMINATION_KEYWORD}.
Otherwise, continue.

RESPONSE:
{{{{$lastmessage}}}}
"""
            )
            agents = [agent_location_identifier, agent_data_analyst]
            chat = AgentGroupChat(
                agents=agents,
                selection_strategy=KernelFunctionSelectionStrategy(
                    initial_agent=agent_location_identifier,
                    function=selection_function,
                    kernel=kernel,
                    result_parser=lambda r: str(r.value[0]).strip(),
                    history_variable_name="lastmessage",
                    history_reducer=ChatHistoryTruncationReducer(target_count=2),
                ),
                termination_strategy=KernelFunctionTerminationStrategy(
                    agents=[agent_data_analyst],
                    function=termination_function,
                    kernel=kernel,
                    result_parser=lambda r: TERMINATION_KEYWORD in str(r.value[0]).lower(),
                    history_variable_name="lastmessage",
                    maximum_iterations=8,
                    history_reducer=ChatHistoryTruncationReducer(target_count=2),
                )
            )
            st.session_state.chat = chat
            st.session_state.history = []
            first_prompt = "Given coordinates ({lat}, {lon}), provide agricultural recommendations."
            asyncio.run(st.session_state.chat.add_chat_message(message=first_prompt))
            for name, msg in asyncio.run(stream_response(st.session_state.chat)):
                st.session_state.history.append((name, msg))

        # --- Display chat for follow-up prompts --- #
        st.markdown("### 🤖 Chat with the Agricultural AI Agent")
        for sender, msg in st.session_state.history:
            with st.chat_message(sender):
                st.markdown(msg.strip())

        # --- Handle user's follow-up prompts and display agents' responses --- #
        user_input = st.chat_input("Ask a follow-up question about farming, agricultural regulations, and soil moisture forecast...")
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            asyncio.run(st.session_state.chat.add_chat_message(message=user_input))
            st.session_state.chat.is_complete = False
            with st.spinner("Thinking..."):
                responses = asyncio.run(stream_response(st.session_state.chat))
                for name, msg in responses:
                    st.session_state.history.append((name, msg))
                    with st.chat_message(name):
                        st.markdown(msg.strip())
