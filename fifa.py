import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

# Load your cleaned and refined dataset
df = pd.read_pickle("fifa_data.pkl")  # Replace with your .pkl file path

# Initialize the session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "main"

# Main Page
if st.session_state.page == "main":
    # Set the title and description
    st.title("Ultimate FIFA Player Analysis")
    st.subheader("Dive into the world of football stats and create your dream team!")

    # Welcome banner (you can use images or text)
    st.image("https://i.imgur.com/y2il3yk.jpeg", use_column_width=True)  # Replace with your image


    st.markdown(
    """
    <style>
    .feature-card {
        background-color: #4c496f;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        transition: transform 0.2s;
    }
    .feature-card:hover {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Feature Cards
    st.write("### Explore Our Features")
    features = {
        "Player Search": "Search and view detailed stats of football players.",
        "Player Comparison": "Compare players using radar charts.",
        "Market Value": "Discover top-valued and undervalued players.",
        "Dream Team Creator": "Build and visualize your dream team."
    }

    # Create columns for the feature cards
    cols = st.columns(2)  # Create 2 columns for the cards

    # Loop through features and create cards
    for index, (feature, description) in enumerate(features.items()):
        with cols[index % 2]:  # Use modulo to rotate columns
            st.markdown(
               f"""
            <div class="feature-card">
                <h4>{feature}</h4>
                <p>{description}</p>
                
            </div>
            """,
            unsafe_allow_html=True
            )
            st.write(description)
            if st.button(f"Go to {feature}", key=index):
                st.session_state.page = feature.lower().replace(" ", "_")  # Navigate to the selected feature

    # About Me Section
    st.markdown("<h2 style='text-align: center;'>About Me</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center;'>
        Hey there! This is my first project, and I'm super excited to share it with you all. 
        I'm currently exploring the world of data science and machine learning. 
        Your feedback would mean a lot to me, as I'm constantly looking to improve and grow. 
        Feel free to reach out and connect!
    </p>
    """, unsafe_allow_html=True)

    # Social Media Links
    st.markdown("<h3 style='text-align: center;'>Connect with Me</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<a href='https://www.instagram.com/omkarrharyan/' target='_blank'>Instagram</a>", unsafe_allow_html=True)
    with col2:
        st.markdown("<a href='https://github.com/Meanwhile-omkar' target='_blank'>GitHub</a>", unsafe_allow_html=True)
    with col3:
        st.markdown("<a href='https://www.linkedin.com/in/omkar-haryan-596a33280/' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align: center;'>
        Thanks for visiting! 🌟
    </p>
    """, unsafe_allow_html=True)



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
                st.markdown(
                    f"<h2 style='color: #2E8B57;'>{player_info['short_name']}</h2>", unsafe_allow_html=True
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Full Name:** {player_info['long_name']}")
                    st.markdown(f"**Age:** {player_info['age']}")
                    st.markdown(f"**Nationality:** {player_info['nationality']}")
                    st.markdown(f"**Club:** {player_info['club_name']}")
                    st.markdown(f"**League:** {player_info['league_name']}")
    
                with col2:
                    st.markdown(f"**Overall Rating:** :star: {player_info['overall']}")
                    st.markdown(f"**Potential Rating:** :star2: {player_info['potential']}")
                    st.markdown(f"**Value (EUR):** :moneybag: {player_info['value_eur']:,}")
                    st.markdown(f"**Wage (EUR):** :dollar: {player_info['wage_eur']:,}")
                    st.markdown(f"**Positions:** {player_info['player_positions']}")

                st.write("---")

                # Display attributes in a horizontal layout
                st.markdown("<h4 style='color: #FFA07A;'>Player Attributes:</h4>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Pace:** {player_info['pace']} :dash:")
                    st.markdown(f"**Shooting:** {player_info['shooting']} :soccer:")
                with col2:
                    st.markdown(f"**Passing:** {player_info['passing']} :dart:")
                    st.markdown(f"**Dribbling:** {player_info['dribbling']} :basketball:")
                with col3:
                    st.markdown(f"**Defending:** {player_info['defending']} :shield:")
                    st.markdown(f"**Physicality:** {player_info['physic']} :muscle:")


        else:
            st.write("No players found. Please try another search.")

    if st.button("Back to Main Page"):
        st.session_state.page = "main"  # Navigate back to main page

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
        st.session_state.page = "main"  # Navigate back to main page


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
        st.session_state.page = "main"  # Navigate back to main page


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
        st.session_state.page = "main"  # Navigate back to main page



elif st.session_state.page == "dream_team_creator":
    st.title("Dream Team Creator")
    st.subheader("Select players to create your dream football team!")

    # Create a dictionary to store selected players by position
    selected_players = {
        "Goalkeeper": [],
        "Defender": [],
        "Midfielder": [],
        "Forward": []
    }

    # Limitations for each position
    position_limits = {
        "Goalkeeper": 1,
        "Defender": 4,
        "Midfielder": 3,
        "Forward": 3
    }

    # Dropdowns for selecting players by position
    for position, limit in position_limits.items():
        if position == "Goalkeeper":
            available_players = df[df['player_positions'].str.contains('GK')]
        elif position == "Defender":
            available_players = df[df['player_positions'].str.contains('CB|LB|RB|LWB|RWB')]
        elif position == "Midfielder":
            available_players = df[df['player_positions'].str.contains('CM|CDM|CAM|LM|RM|LAM|RAM')]
        elif position == "Forward":
            available_players = df[df['player_positions'].str.contains('ST|CF|LW|RW|LF|RF')]

        player_names = available_players['short_name'].tolist()

        # Select multiple players
        selected = st.multiselect(f"Select up to {limit} {position}s:", player_names, max_selections=limit)

        # Add selected player to the list
        selected_players[position] += selected

    # Create a button to visualize the dream team
    if st.button("Visualize Dream Team"):
        # Prepare player positions for plotting
        positions_on_pitch = {
            "Goalkeeper": [(0.5, 0.9)],
            "Defender": [(0.2, 0.7), (0.4, 0.7), (0.6, 0.7), (0.8, 0.7)],
            "Midfielder": [(0.3, 0.5), (0.5, 0.5), (0.7, 0.5)],
            "Forward": [(0.3, 0.3), (0.5, 0.3),(0.7,0.3)]
        }
        
        # Set up the pitch with a green background
        fig = go.Figure()

        # Add a green rectangle to represent the pitch
        fig.add_shape(type="rect", x0=0, x1=1, y0=0, y1=1,
                      line=dict(color="green"),fillcolor="rgba(144, 238, 144, 0.3)")

        # Plot players based on their positions
        colors = {
            "Goalkeeper": "blue",
            "Defender": "green",
            "Midfielder": "orange",
            "Forward": "red"
        }
        dot_size = 20  # Adjusted size for visibility
        opacity = 1  # Increased opacity

        for position, players in selected_players.items():
            for i, player in enumerate(players):
                if i < len(positions_on_pitch[position]):  # Ensure there's a position for the player
                    x, y = positions_on_pitch[position][i]
                    fig.add_trace(go.Scatter(
                        x=[x], y=[y],
                        mode='markers+text',
                        marker=dict(size=dot_size, color=colors[position], opacity=opacity),
                        text=[player],
                        textposition="bottom center",
                        name=player
                    ))

        # Pitch layout
        fig.update_layout(
            title="Your Dream Team",
            xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
            yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
            showlegend=True
        )
        
        st.plotly_chart(fig)

        st.write("📸 Don't forget to download a picture of your dream team and share it with your friends!")


    if st.button("Back to Main Page"):
        st.session_state.page = "main"  # Navigate back to main page