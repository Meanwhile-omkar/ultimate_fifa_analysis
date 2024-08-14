import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load your cleaned and refined dataset
df = pd.read_pickle("fifa_data.pkl")  # Replace with your .pkl file path

# Initialize the session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "main"

# Function to navigate to a feature
def goto_feature(feature):
    st.session_state.page = feature.lower().replace(" ", "_")  # Navigate to the selected feature

# Main Page
if st.session_state.page == "main":
    # Set the title and description
    st.title("Ultimate Football Player Analysis")
    st.subheader("Dive into the world of football stats and create your dream team!")

    # Welcome banner (you can use images or text)
    st.image("https://images.app.goo.gl/wr6bW7fETut44fGeA", use_column_width=True)  # Replace with your image

    # Feature Cards
    st.write("### Explore Our Features")
    features = {
        "Player Search": "Search and view detailed stats of football players.",
        "Player Comparison": "Compare players using radar charts.",
        "Squad Visualization": "Visualize your team lineup and ratings.",
        "Market Value": "Discover top-valued and undervalued players.",
        "Best Players by Position": "Find the best players for each position.",
        "Dream Team Creator": "Build and visualize your dream team."
    }

    # Create columns for the feature cards
    cols = st.columns(3)  # Create 3 columns for the cards

    # Loop through features and create cards
    for index, (feature, description) in enumerate(features.items()):
        with cols[index % 3]:  # Use modulo to rotate columns
            st.markdown(f"### {feature}")
            st.write(description)
            if st.button(f"Go to {feature}", key=index):
                goto_feature(feature)  # Navigate to the selected feature

# Player Search Page
elif st.session_state.page == "player_search":
    st.title("Player Search")
    search_query = st.text_input("Enter the player name:")

    if search_query:
        # Filter the DataFrame based on the search query (partial matching)
        filtered_df = df[df['short_name'].str.contains(search_query, case=False)]

        if not filtered_df.empty:
            st.write(f"### Results for '{search_query}':")

            # Dropdown menu for selecting a player
            player_names = filtered_df['short_name'].tolist()
            selected_player = st.selectbox("Select a player from the suggestions:", player_names)

            # Display player details for the selected player
            if selected_player:
                player_info = filtered_df[filtered_df['short_name'] == selected_player].iloc[0]
                st.markdown(f"**{player_info['short_name']}**")
                st.write(f"**Name:** {player_info['short_name']}")
                st.write(f"**Full Name:** {player_info['long_name']}")
                st.write(f"**Age:** {player_info['age']}")
                st.write(f"**Nationality:** {player_info['nationality']}")
                st.write(f"**Club:** {player_info['club_name']}")
                st.write(f"**League:** {player_info['league_name']}")
                st.write(f"**Overall Rating:** {player_info['overall']}")
                st.write(f"**Potential Rating:** {player_info['potential']}")
                st.write(f"**Value (EUR):** {player_info['value_eur']}")
                st.write(f"**Wage (EUR):** {player_info['wage_eur']}")
                st.write(f"**Positions:** {player_info['player_positions']}")
                st.write(f"**Pace:** {player_info['pace']}")
                st.write(f"**Shooting:** {player_info['shooting']}")
                st.write(f"**Passing:** {player_info['passing']}")
                st.write(f"**Dribbling:** {player_info['dribbling']}")
                st.write(f"**Defending:** {player_info['defending']}")
                st.write(f"**Physicality:** {player_info['physic']}")
                
        else:
            st.write("No players found. Please try another search.")

    if st.button("Back to Main Page"):
        goto_feature("main")  # Navigate back to main page

# Player Comparison Page
elif st.session_state.page == "player_comparison":
    st.title("Player Comparison")

    # Dropdown for selecting players
    player1 = st.selectbox("Select Player 1", df['short_name'].tolist())
    player2 = st.selectbox("Select Player 2", df['short_name'].tolist())

    if st.button("Compare Players"):
        # Get the data for the selected players
        player1_data = df[df['short_name'] == player1].iloc[0]
        player2_data = df[df['short_name'] == player2].iloc[0]

        categories = ['overall', 'potential', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']

        # Create radar chart
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=player1_data[categories].values.tolist(),
            theta=categories,
            fill='toself',
            name=player1_data['short_name']
        ))
        fig.add_trace(go.Scatterpolar(
            r=player2_data[categories].values.tolist(),
            theta=categories,
            fill='toself',
            name=player2_data['short_name']
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    showticklabels=True,
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=10)
                )
            ),
            showlegend=True,
            title="Player Comparison Radar Chart"
        )

        # Display the radar chart
        st.plotly_chart(fig)

    if st.button("Back to Main Page"):
        goto_feature("main")  # Navigate back to main page


elif st.session_state.page == "market_value":
    st.title("Market Value Analysis")
    st.subheader("Explore the top-valued players and those with high potential but low market value.")

    # Top-Valued Players
    st.write("### Top-Valued Players")
    top_valued_players = df.sort_values(by='value_eur', ascending=False).head(10)

    # Display Top-Valued Players in a table
    st.table(top_valued_players[['short_name', 'club_name', 'value_eur', 'wage_eur', 'overall', 'potential']])

    # Undervalued High-Potential Players
    st.write("### Undervalued High-Potential Players")
    undervalued_players = df[(df['value_eur'] < 20000000) & (df['potential'] > df['overall'])].sort_values(by='potential', ascending=False).head(10)

    # Display Undervalued Players in a table
    st.table(undervalued_players[['short_name', 'club_name', 'value_eur','wage_eur', 'potential', 'overall']])

    # Visualization: Bar Chart for Top-Valued Players
    st.write("### Visualization of Top-Valued Players")
    fig_top_value = go.Figure()
    fig_top_value.add_trace(go.Bar(
        x=top_valued_players['short_name'],
        y=top_valued_players['value_eur'],
        marker_color='royalblue'
    ))
    fig_top_value.update_layout(title="Top-Valued Players", xaxis_title="Players", yaxis_title="Market Value (EUR)", xaxis_tickangle=-45)
    st.plotly_chart(fig_top_value)

    # Visualization: Bar Chart for Undervalued Players
    st.write("### Visualization of Undervalued Players")
    fig_undervalued = go.Figure()
    fig_undervalued.add_trace(go.Bar(
        x=undervalued_players['short_name'],
        y=undervalued_players['value_eur'],
        marker_color='tomato'
    ))
    fig_undervalued.update_layout(title="Undervalued High-Potential Players", xaxis_title="Players", yaxis_title="Market Value (EUR)", xaxis_tickangle=-45)
    st.plotly_chart(fig_undervalued)

    if st.button("Back to Main Page"):
        goto_feature("main")  # Navigate back to main page


elif st.session_state.page == "best_players_position":
    st.title("Best Players by Position")
    st.subheader("Explore the top players in each position, including goalkeepers.")

    # Position selection
    position = st.selectbox("Select a position:", 
                             ['Goalkeeper', 'Defender', 'Midfielder', 'Forward'])

    # Filter players based on selected position
    if position == 'Goalkeeper':
        position_filter = df['player_positions'].str.contains('GK')
    elif position == 'Defender':
        position_filter = df['player_positions'].str.contains('CB|LB|RB|LWB|RWB')
    elif position == 'Midfielder':
        position_filter = df['player_positions'].str.contains('CM|CDM|CAM|LM|RM|LAM|RAM')
    elif position == 'Forward':
        position_filter = df['player_positions'].str.contains('ST|CF|LW|RW|LF|RF')

    top_players = df[position_filter].sort_values(by='overall', ascending=False).head(10)

    # Display Top Players in a table
    st.write(f"### Top {position}s")
    st.table(top_players[['short_name', 'club_name', 'overall', 'value_eur', 'wage_eur']])

    # Visualization: Bar Chart for Top Players
    st.write(f"### Visualization of Top {position}s")
    fig_best_players = go.Figure()
    fig_best_players.add_trace(go.Bar(
        x=top_players['short_name'],
        y=top_players['overall'],
        marker_color='green'
    ))
    fig_best_players.update_layout(title=f"Top {position}s", xaxis_title="Players", yaxis_title="Overall Rating", xaxis_tickangle=-45)
    st.plotly_chart(fig_best_players)

    if st.button("Back to Main Page"):
        goto_feature("main")  # Navigate back to main page