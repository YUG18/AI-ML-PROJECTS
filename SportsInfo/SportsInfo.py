import requests
import streamlit as st

#sports whose details to be displayed
SPORTS = ["Cricket","Soccer","Basketball","Tennis","Hockey"]
API_KEY = "123"

#function to get informations about sports which takes country name as argument
def get_sports_info(country):
    st.subheader(f"Showing recent matches for {country.upper()}")
    found_any = False
    for sport in SPORTS:
        team_url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/search_all_teams.php?s={sport}&c={country}"
        res = requests.get(team_url)
        if res.status_code != 200:
            st.warning(f" Request failed with status code {res.status_code}")
            return
        try:
            data = res.json()
        except ValueError:
            st.warning(" Response was not valid JSON.")
            return

        teams = data.get("teams")

        if not teams:
            st.warning(f"No {sport} teams found for {country}")
            continue

        with st.expander(f"{sport} teams"):
            for team in teams:
                team_name = team.get("strTeam")
                st.markdown(f"{team_name}")
                match_url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventslast.php?id={team['idTeam']}"
                match_response = requests.get(match_url)

                if match_response.status_code != 200:
                    st.warning("⚠️ Failed to fetch match data.")
                    continue

                try:
                    match_data = match_response.json()
                except ValueError:
                    st.warning("⚠️ API did not return valid JSON.")
                    continue

                if 'results' not in match_data or not match_data['results']:
                    st.info("No recent match available.")
                    continue
                found_any = True
                from datetime import datetime
                recent_matches = [m for m in match_data['results'] if m.get('dateEvent') and m['dateEvent'].startswith("2025")]
                if not recent_matches:
                    st.warning("No matches found for current year")
                    continue
                for match in recent_matches:
                    st.markdown(f"**Match:** {match.get('strEvent', 'N/A')}")
                    st.write(f"📅 Date: {match.get('dateEvent', 'N/A')} | 🕒 Time: {match.get('strTime', 'N/A')}")
                    st.write(f"🏟️ Venue: {match.get('strVenue', 'Unknown')}")
                    st.write(f"🎯 Score: {match.get('intHomeScore', '?')} - {match.get('intAwayScore', '?')}")
                    st.write(f"🔁 Status: {match.get('strStatus', 'Unknown')}")

                    # Scorecard (Mini table)
                    st.table({
                        "Team": [match.get('strHomeTeam', 'N/A'), match.get('strAwayTeam', 'N/A')],
                        "Score": [match.get('intHomeScore', '?'), match.get('intAwayScore', '?')]
                    })

                    st.markdown("---")
    if not found_any:
        st.info("No matches found across all sports")

st.title("Multi-Sports live tracker")
country_name = st.text_input("Enter a country name.")

if __name__=="__main__":
    if country_name:
        get_sports_info(country_name)