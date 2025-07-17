#heading
# search functionality mid
# sliders-like filtering based on year ranges
# filters
# visualizations



#import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def load_dataset():
    return pd.read_csv("data.csv")

df=load_dataset()

st.title("Indian Movies Analysid Dashboard")

    # search movie -partial or full
st.subheader("search for a mvie")
search_query=st.text_input("Enter a movie name(partial or full,case-insensitive)")

if search_query:
    search_results=df[df["Movie Name"].str.contains(search_query, case=False,na=False)]
    #filter condition = df["Movie Name"].str.contains(search_query, case=False,na=False)}
    #df[filter condition]
    #df[df["Movie Name"]]
    if not search_results.empty:
        st.write(f" Found {len(search_results)} movie(s)")
        st.dataframe(search_results[["Movie Name", "Year", "Rating(10)", "Genre", "Votes", "Language"]])
    else:
        st.write("No movies found matching your query!!!!")

# filter movies by year range
st.sidebar.header("Filters")

genre_filter=st.sidebar.multiselect("Select Genre", df["Genre"].unique(), default=[])
if genre_filter:
    # df[filter condition]
    # df ['genre'].isin["drama", "thriller"])

    df=df[df["Genre"].isin(genre_filter)]

language_filter=st.sidebar.multiselect("Select Language", df["Language"].unique(), default=[])

if language_filter:
    # df[filter condition]
    df=df[df['Language'].isin (language_filter)]

# filter by user
year_filter=st.sidebar.slider("Select Year Range", int(df["Year"].min()),int(df["Year"].max()),(1950,2025))
#st.sidebar.slider(text, min_valu, max_val, default_val)
# (2000,2005) >=2000 && <=2005
# between (2000, 2005) * and **
df=df[df["Year"].between(*year_filter)]




# filter by rating
rating_filter=st.sidebar.slider("Select Rating Range", float(df["Rating(10)"].min()),float(df["Rating(10)"].max()),(0.0,10.0))
#st.sidebar.slider(text, min_valu, max_val, default_val)
# (2000,2005) >=2000 && <=2005
# between (2000, 2005) * and **
df=df[df["Rating(10)"].between(*rating_filter)] 


#votes - filter
votes_filter=st.sidebar.slider("Select Votes Range", int(df["Votes"].min()), int(df["Votes"].max()), (int(df["Votes"].min()), int(df["Votes"].max())))
df=df[df["Votes"].between(*votes_filter)] 

st.subheader("Filtered Movies Data")
st.dataframe(df)



st.subheader("Visualizations")
visualization_option=st.selectbox("Select a visualization or analysis condition",
                [ 
                    "Top 10 Movies by Rating",
                     "Top 10 Movies by Votes"
                ])     

if visualization_option=="Top 10 Movies by Rating":
    top_rated_movies = df.nlargest(10, "Rating(10)")
    st.write("Top 10 Movies by Rating")
    st.dataframe(top_rated_movies[["Movie Name", "Year", "Rating(10)", "Genre", "Votes", "Language"]])
    
    # Bar chart for top rated movies
    fig_top_rated = px.bar(top_rated_movies, x="Movie Name", y="Rating(10)", color="Genre", title="Top 10 Movies by Rating")
    st.plotly_chart(fig_top_rated)
elif visualization_option=="Top 10 Movies by Votes":
    top_voted_movies = df.nlargest(10, "Votes")
    st.write("Top 10 Movies by Votes")
    st.dataframe(top_voted_movies[["Movie Name", "Year", "Rating(10)", "Genre", "Votes", "Language"]])
    # Bar chart for top voted movies
                
    fig_top_voted = px.bar(top_voted_movies, x="Movie Name", y="Votes", color="Genre", title="Top 10 Movies by Votes")
    st.plotly_chart(fig_top_voted)
    
# Bar chart for movies by genre
genre_counts = df["Genre"].value_counts()
fig_genre = px.bar(genre_counts, x=genre_counts.index, y=genre_counts.values, labels={'x': 'Genre', 'y': 'Number of Movies'}, title='Movies by Genre')
st.plotly_chart(fig_genre)

# Bar chart for movies by Language
language_counts= df["Language"].value_counts()
fig_language = px.bar(language_counts, x=language_counts.index, y=language_counts.values, labels={'x': 'Language', 'y': 'Number of Movies'}, title='Movies by Language')
st.plotly_chart(fig_language)

# Line chart for movies by year
year_counts = df["Year"].value_counts().sort_index()
fig_year = px.line(year_counts, x=year_counts.index, y=year_counts.values, labels={'x': 'Language', 'y': 'Number of Movies'}, title='Movies by Year')















