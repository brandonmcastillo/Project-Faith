# Project-Faith

## Demo
Email: demo@gmail.com<br>
Password: 123

## Links
<a href="https://faith-community.herokuapp.com/">Faith (Heroku Version) </a> Note: May contain bugs due to heroku. I suggest running on local machine. (instructions below)  
<br>
<a href="https://github.com/brandonmcastillo/Project-Faith">Github Repo</a> 
<br>
<a href="https://trello.com/b/qzbvwKuk/faith">Trello Board</a>

## Summary
Faith is a mental health community application created by Brandon Castillo where users can browse articles or ask questions and receive advice from other users in the community. The users of Faith are individuals who are seeking advice or motivation and want to learn or talk about mental health issues they, a friend or family member may have.The application was created using a Flask stack involving HTML, SASS, Bulma.io, Python, Flask, Peewee and SQLite which has migrated to Postgres.

## Screenshots
![](assets/Landing.png)
![](assets/Main.png)
![](assets/Profile.png)

## Technologies Used
Languages
- HTML5
- CSS3 with SASS
- Python
- JavaScript

Frameworks
- Flask
- Bulma.css

Libraries
- jQuery

Other
- Heroku

## Wireframes and User Stories
Database contains four relational models which consists of a User, Post, Reply and Replythread.
Wireframes are linked in trello board link above. Users will be able to sign up/login, view daily written articles by medical news today, edit their profile, see a quote of the day and gain access to the community board where they can posts or start a reply thread to other users.  

## Current Bugs / Unresolved Issues
- jQuery scroll down on main page does not work on mobile
- Heroku sometimes crashes the app when deleting

## Future Features
- Upvoting a post or comment
- Personal Journal 


## Installation Steps
- Clone down repo
- Run a terminal and cd to folder
- Run npm i to install SASS dependencies and run 'npm start' (Used for SASS updates)
- Open a new terminal (CMD+T) and run 'pip3 install virtualenv' followed by 'virtualenv .env -p python3'
- Run 'source .env/bin/activate' in the same terminal to activate environment
- Run pip install -r requirements.txt to install depenendcies
- To switch from Heroku to Sqlite, comment in line 276-288 in app.py and line 15 in models.py. Comment out other code to switch it.
- Run 'python3 app.py' to run application
- Open browser and go to http://127.0.0.1:8000 to run on local machine





