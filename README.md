# magonote

A recommender for [itch.io](https://itch.io/), a platform for 
small/indie/experimental games

## Background

I am fond of video games but find myself struggling to find ones that satisfy 
my specific interests.

Itch.io is a distubution service/platform that serves smaller independent 
creators and studios, and as such tends to have more interesting experimental 
types of games. The upshot of this is that games don't fall into traditional
categories (fighting/racing/rpg/etc) as much which can make discovery more 
difficult. 

magonote attempts to address that difficulty by using the game description text
to organize games into clusters, and measuring relative popularity with 
user-game interaction.

There are several challenges. Most notably the fact that Itch.io does not 
publish specific user-game interactions (eg purchase, playtime, rating) 
publicly means that determining those interactions requires making some 
assumptions. Furthermore, the game descriptions are not always as helpful as
we would like in determining the nature of the game and in some cases are 
absent altogether. This is in keeping with the nature of Itch.io, and should 
be expected.

The one (and only) place where user-game interaction is explicit is in 
comments. Comments are not always specific to a game but when they are they can
be useful in approximating a rating-- in general the longer comments are more
positive. Sentiment analysis was not performed on comments but that is 
certainly something that could be useful in the future. Fortunately comments 
are indexed sequentially which makes retrieval fairly straightforward.

## Tools

Magonote is written in python and relies on requests, Beautiful Soup, 
SciKit-learn, psycopg2, pandas, numpy &c.

Some of the scraping was attempted first using cURL but 
throttling/rate-limiting became an issue and requests was used instead.

PostgreSQL provides the DB, and it is hosted on an AWS EC2 Ubuntu instance with 
some S3 storage.

## Outcomes

The matricies are pretty sparse and it was difficult to determine how useful 
the predictions were. Validation for recommenders is difficult under the best 
of circumstances and so attempting to do so was postponed pending new data 
being made available.

Anecdotal evidence suggests that while recommendations are better than random 
there is some room for improvement.

## Future work

Possibilities for improvements include

- sentiment analysis
- better use of tags, weighting
- scheduled/automatic updating
- incorporate new/better data

## Name

From [magonote](https://jisho.org/search/%E5%AD%AB%E3%81%AE%E6%89%8B)





