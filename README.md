# Discord Bot

## About this Bot


**Description**


A python Discord Bot connects with the MongoDB with the ability to record time from any Discord voice channel
The Bot monitor any Discord text channels and message back with the checked members a world of blessing for today
User can customize the records with a 'tag' which will be graphed by the Bot in line, bar or histogram chart


**Requirement**


 - Python
 - Discord
 

## Key Features


 - STUDY ROOM
     - Watch any Discord Voice Channels with key world 'Study Room'
     - Record users' stand time in such voice channel
     - Customizable 'tag' to the tracking time
     - Members' time from the Voice Channels will be saved to the database
     
 - CHECK IN   
     - Watch any Discord Text Channels with key world 'check-in'
     - Message back to the 'check-in' Channel daily at 5:00 AM CST with list of checked members
     - A world for blessing comes with the check message from the Bot
     - Checked data will be saved to the database daily
     
 - PRESENTATION
     - Presentation the 'tag' and 'time' with LINE chart, PIE chart and HISTOGRAM chart
     - Data will be grouped by day, week or month interval
     
 - DATABASE
     - MongoDB data warehouse
     

## Current Function (current Beta v0.4)


 - -help: help feature
 - -hi or -hello: say hi to the Bot
 - -roll: roll a dice between 1 and 100
 - -tag XXX: tag the time with customize focus
 - -get details: grab the historical data in table view
 - -get graph OPTIONAL1 OPTIONAL2
    - OPTIONAL1: time interval (day/week/month) (default: day)
    - OPTIONAL2: chart type (line/bar) (default: line)  
 - -get date OPTIONAL1: get the date's data via pie chart

- Example of the Line Chart

![image](https://user-images.githubusercontent.com/19805677/211453713-48ad667a-5d57-47b7-b64c-87acd90d97be.png)

- Example of the Bar Chart

![image](https://user-images.githubusercontent.com/19805677/211453737-d8e56b77-181f-463a-95f2-10cde5fa31c4.png)

- Example of the Pie Chart

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


## Authors


Mai He [https://github.com/mablic/]
## Acknowledgments
N/A
