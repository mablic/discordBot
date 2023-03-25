# Discord Bot

## About this Bot


**Description**


The Discord Bot will monitor any voice Discord channel with the keyword "Study Room", which will allow it to record the study time of any user in that channel. The bot will then store this data in a MongoDB database. Later, the bot can generate a bar chart or line chart based on a specified time interval (day, week, or month) for any user's study time.

The bot will also monitor any text channel with the keyword "check-in". Whenever a user checks in, the bot will automatically generate a message that lists all of the users who checked in for the previous day.

Additionally, the bot will monitor any text channel with the keyword "mock-interview". Whenever a user types a message in this channel, the bot will generate a random behavioral question or a random Leetcode problem for the user to practice for a mock interview.

Overall, this bot will be a helpful tool for users who want to track their study time, check in with their peers, and practice for job interviews.


**Requirement**


 - Python
 - Discord
 

## Key Features


 - STUDY ROOM
     - Watch any Discord Voice Channels with key world 'Study Room'
     - Record users' stand time in such voice channel
     - Customizable 'tag' to the tracking time
     - Members' time from the Voice Channels will be saved to the database

 - MOCK INTERVIEW
     - Watch any Discord Voice Channels with key world 'Mock Interview'
     - Watch any Discord Text Channels with key world 'mock-interview'
     - Randomly generate a behavior question or a LeetCode challenge
     - Record the time for the mock interview section

 - CHECK IN   
     - Watch any Discord Text Channels with key world 'check-in'
     - Message back to the 'check-in' Channel daily at 5:00 AM CST with list of checked members
     - A world for blessing comes with the check message from the Bot
     - Checked data will be saved to the database daily

 - SCHEDULER  
     - Watch any Discord Text Channels with key world 'scheduler'
     - Customizable message to notified user to check-in in on the CHECK IN channel
     - Reminder to the user every hour if not CHECKED IN
     
 - PRESENTATION
     - Presentation the 'tag' and 'time' with LINE chart, PIE chart and HISTOGRAM chart
     - Data will be grouped by day, week or month interval
     
 - DATABASE
     - MongoDB data warehouse
     

## Current Function (current Beta v0.5)


 - -help: help feature
 - -hi or -hello: say hi to the Bot
 - -roll: roll a dice between 1 and 100
 - -tag XXX: tag the time with customize focus
 - -scheduler XXX XXX: reminder setup with the bot
    - REQUIRED: 0-23 in hours
    - OPTIONAL: A custom message to notify user check in
 - -interview REQUIRED OPTIONAL: generate an interview question
    - REQUIRED: 
      - bq: Behavior question
      - code: LeetCode question
    - OPTIONAL: easy, medium, hard: only apply if user input code on the required field
      - easy: An easy leetcode question
      - medium: A medium leetcode question
      - hard: A hard leetcode question
 - -get details: grab the historical data in table view
 - -get graph OPTIONAL1 OPTIONAL2
    - OPTIONAL1: time interval (day/week/month) (default: day)
    - OPTIONAL2: chart type (line/bar) (default: line)  
 - -get date OPTIONAL1: get the date's data via pie chart
 - -timezone REQUIRED: set the timezone for user
    - REQUIRED: the Bot default in the CST, user needs to entry the time different between their timezone and the CST
    - Example: 
       - -timezone -1: Mountain Time
       - -timezone 1 or -timezone +1: Eastern Time

## Example Chart

Example of the Line Chart

![image](https://user-images.githubusercontent.com/19805677/211453713-48ad667a-5d57-47b7-b64c-87acd90d97be.png)

Example of the Bar Chart

![image](https://user-images.githubusercontent.com/19805677/211453737-d8e56b77-181f-463a-95f2-10cde5fa31c4.png)

Example of the Pie Chart

![image](https://user-images.githubusercontent.com/19805677/211453755-22b85213-326a-43b9-9128-8d90fa39c574.png)


## Development phase (current Beta v0.1)


 - Beta v0.1:
    - Production release of the Bot
    - Live watch for two Discord group

 - Beta v0.2:
    - Bugs fix
    - Pie chart

 - Beta v0.3:
    - Bugs fix with read database error

 - Beta v0.4:
    - The newest release comes with the "check-in" function on the Bot
    - The Bot now can run with scheduler, no user interface for now
    - Bugs fix with the scheduler

 - Beta v0.5:
    - New function for the mock interviewer
    - Randomly interview question for users
    - Bugs fix

 - Beta v0.6:
    - New function for the scheduler, now the Bot can send reminder to the user
    - Bugs fix

 - Beta v0.7:
    - New function to add the time zone by user. The Bot can send reminder to the user by their time zone
    - Update the database schema of the check-in table
    - Update the notification class to include the Discord channel id
    - Restrict the asynchronous with the scheduler with one core

## Authors


Mai He [https://github.com/mablic/]
## Acknowledgments
N/A
