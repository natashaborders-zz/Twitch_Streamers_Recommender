## Twitch Recommender for Streamers ##

For this project, we analyze the Twitch stream data to determine two things:

* First step - which games are rising in popularity and have gaps in the streamer availability to be able to recommend new streamers what to begin streaming.
* Second step - for those streamers who already stream their favorite games we intend to recommend other similarly appealing games for them to try and stream.

### Acquisition of the Data ###

We used the Twitch API to pull in the live stream data from the Twitch website using our AWS EC2 instance and funneling the data into a POSTGRESQL database using Amazon RDS services.

We collected the stream level information for top 100 games and their top 100 streamers over the course of approximately two weeks, sending the requests to Twitch every 1 hour.

Our resulting dataset consisted of three PostgreSQL tables which included:

##### stream_data #####

 * stream_id text
 * user_id text
 * user_name text
 * game_id text
 * stream_type text
 * title text
 * viewer_count int
 * started_at timestamp
 * language text
 * time_logged timestamp

##### game_information #####

 * game_id text
 * game_name text
 * pic_url

##### game_genres #####

 * game_name text
 * game_genres text

 ### Analysis Step 1: Go for the low hanging fruit ###

To calculate which games are going to be on the rise, we first analyzed which games appeared to be increasing in viewership compared to channels providing the said games.

The general metric to evaluate the trending games was change in viewership for each game, more specifically:

* average number of viewers per stream featuring the game during a day/average number of viewers per stream featuring this game the previous day

* average number of channels streaming the game during a day/average number of channels streaming the game during the previous day

As these rolling averages are computed for each of the top 100 games, they will reflect the potential for a new channel to join in streaming the trending games which are not scaling the number of channels in proportion with increasing viewership.

### Analysis Step 2: Genre is king ###

The next argument in picking what to stream comes with the fact that the majority of streamers coming to Twitch have a favorite genre or a type of game they enjoy playing. To address the desire to stream games in one's genre of choice or similar to the games one prefers, we applied natural language processing to evaluate queries submitted in a search bar to produce recommendations based on genre/games similar to the subject of the query.

For example, if a person queries: "Rpg, or something like Wow", we need to be able to parse this query to determine that they are looking for a "role playing game" genre or a game similar to World of Warcraft, which is a popular online multiplayer game, so we would need to include suggestions in the MMORG space, but also suggest single-player RPGs as an alternative.

The suggested games, while specific to the genre they requested, would still be those trending in terms of viewers relative to channels over time as predicted by our algorithms.

To be able to use the game attributes for suggestions, we used the scraped descriptions of the top games and their differentiating features.

### Analysis Step 3: You're already in the game ###

The most granular level of recommendations would apply to those who are already a streamer on the platform, and are looking for advice on what to try perhaps as a change from their existing game or content. For these streamers, we would see if their user_id is already contained in our database of top 100 streamers of top 100 games. If it is, we can use their existing streaming history to recommend a game that they have not yet streamed but which is trending and is similar to their existing stream history.

To check for this, we might ask them to fill out a short form asking for their twitch sign-in name and the list of games they already stream. Then based on their answers, produce results for this person, suggesting games they have not yet streamed that are similar to those they have streamed but are more likely to increase their viewership.

The package used for this piece of the analysis is the Surprise recommender system. (https://surprise.readthedocs.io/en/stable/index.html)
