# Reddit Joke Bot
==============

Queries /r/jokes.json?top&limit=10&t=hour (human readable: get the top 10 of the hour) and posts the jokes that are <140 char to twitter using Python 2,7 (sorry, wrote this on a machine where I couldn't install 3,5, maybe one day I'll change it!)

## Requirements
+ requests
+ yaml
+ twython
+ Twitter OAUTH keys, see [here](https://dev.twitter.com) 

## How to use
Fill in your OAUTH keys in options.yaml and run! Chuck this in a cronjob that runs hourly and you'll be good to go.

## Timing

The timing is determined on 
1. How many jokes are in the queue
2. How many of those jokes are <140 char

Timing between each tweet == (amount of jokes based on above) / 3600

If you want a longer interval, either change the limit in your get request from 10 to a lower number, or increase 3600 to a higher number and increase the interval your cronjob

## ToDo
Fix any exceptions that may occur (probably in requests if there is a connectivity issue)
