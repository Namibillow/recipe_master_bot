RECIPE MASTER - A FACEBOOK MESSENGER CHAT BOT -

- Go to my facebook page and talk to recipe-master bot simply by tellig ingredients you want and it will generate 10 recipes for you. 
- Still on going, planning on expand to do process more conplex request 

- Since EDMAM API only allows 5 calls per minutes, please be aware that chat bot might not giving you the results


- Although EDMAM API is pretty good at generating food recipes with even some food ingridients typo, but I decided to write my own script that will autocorrect the name of the

.gitignore contains
    - all the files that needs to be ignored or hidden from others

Procfile (Required for Heroku)
    - tells Heroku how to run various pieces of your app

requirements.txt (Required for Heroku)
    - all packages used in this app
    - RESOURCES:
            https://gist.github.com/pratos/e167d4b002f5d888d0726a5b5ddcca57
            https://www.technologyscout.net/2017/11/how-to-install-dependencies-from-a-requirements-txt-file-with-conda/
            https://stackoverflow.com/questions/47445426/conda-keeps-trying-to-install-all-optional-dependencies

app.py
    - a main file where it receives the user's response and returns generated response

.env
    - stores environment variables (private keys)

settings.py
    - reads all the environment variables
    - RESOURCES: https://robinislam.me/blog/reading-environment-variables-in-python/

recipe.py
    - contains recipe class where returns the recipe search results
