<h1>Pay Tracker Application</h1>
<p>
My Pay Tracker app is a python terminal project, which aids users to track their worked hours and how much they are due to be paid for that day. This app is targeted at average hospitability, workers, care worker or someone who is in need to track a dayshift which is paid hourly with unpaid breaks. 
Users enter the of there shift, start time, end time, breaks and hourly wage. The application will return to the user how much they are due to be paid for the day shift. It will also log it to a google sheet for storage. The user has the option to recall the last 7 entries. This is ideally so the user can pull the last weeks’ worth of data and check their pay., worked hours and breaks.
The user follows the prompts to get to the calculated results. 
I designed this application with someone like me in mind. After a few work collages and I were paid incorrectly. I started to track my worked hours.
I needed to track my working hours for each day and calculate my days pay. I created an excel spreadsheet and had to manually enter the data and set the functions for each item list I wanted to enter. This was taking a bit of time, was really small on my phone. I thought this would be easier if there was an application to do the work for me and possibly an application my work collages could use to track their own working days too.
</p>
<img src ="/workspace/Working-Hours-Tracker-PP3/views/images/ppemain.png">

<h2>Features</h2>

<p>
When the program is loaded
The user can see a welcome message with prompts for the user to follow.

<img src = "views/images/Auto Pay Tracking App. 1.png">
At this stage, the user will need to enter a valid date. This cannot be in the future, as the app is tracked worked days only. The app will only take data that is less than 5 years old. This app is designed for more current data, not historical dates. For this reason, I set the limit for no more then 5 years past. 

<img src = "/workspace/Working-Hours-Tracker-PP3/views/images/Auto Pay Tracking App 2.png">
After you enter a valid date, the user is asked to enter a start time followed by an end time These need to be with the 24-hour format and must run within that daytime frame, it does not support night shifts. 

<img src = /workspace/Working-Hours-Tracker-PP3/views/images/pp3 4.png>
Now the user is asked to enter their break duration. This app will deduct the break time form the total worked hour to calculate their pay. If someone’s breaks are paid, then this app is not for that type of user.
From here the user is asked to enter their hourly wage. I set a limit of £1-250. This helps stick to the applications targeted audience.

<img src = "/workspace/Working-Hours-Tracker-PP3/views/images/pp7.png">

From here the data is logged to the google sheet and the user is given the option to enter more shifts. If the user enters no, they can check the last 7 entries then exit the application.

<img src = /workspace/Working-Hours-Tracker-PP3/views/images/pp3 final.png>
</p>
<h2>Flow Chart</h2>

<p>
I brainstormed using lucid chats to understand what I need to do and how to get the idea into working code. 
<img src = /workspace/Working-Hours-Tracker-PP3/views/images/flow.png>
</p>

<h2>Future Features</h2>
<p>
On the google sheet there is a work sheet called commission. I would like to add code to have the user enter how much commission they did earn on each shift.
</p>

<h2>Testing</h2>
<p>
I have manually tested the project by doing the following:
<ul>
	<li>Passed the code through a PEP8 linter and confirmed there are no problems.</li>
	<li>Tested in my local terminal and within the Heroku terminal.</li>
	<li>Made sure invalid user inputs are identified and promoted to be corrected.</li>
    </ul>
</p>
<h2>Bugs</h2>

<h3>Solved bugs</h3>
When I was writing the code I went through some changes to remove any buys I found. The main bugs I found are as follows:
<ul>
<li>Users were being able to enter times that were outside a 24-hour time frame, that resulted in negative hours worked and a negative pay amount. I correct this by checking the start time is before the end time and shifts are within the same 24-hour time frame.</li>
<li>You could enter a longer break time then the length of the shift time. I corrected this by setting a realistic break time limit of 120 minutes.</li>
<li>You could enter white space in the inputs and crash the programme. I made sure to add if/else statements to check for white space and loops to make sure the user enters the correct data.</li>
</ul>

<h2>Validator Testing</h2>
<p>
Pep8 – No errors were found 
<img src = /workspace/Working-Hours-Tracker-PP3/views/images/Python PEP8 check.png>
</p>


<h2>Deployment</h2>
This project was deployed using Code Institute’s mock terminal for Heroku and GitHb.
Steps for deployment:
<ul>
<li>Fork or clone this repository.</li>
<li>Make sure you create a requirements.txt. for your dependencies</li>
<li>Your code must be placed in the `run.py` file.</li>
<li>Push to GitHub.</li>
<li>Sign into Heroku or create an account.</li>
<li>Create a new Heroku app.</li>
<li>Set up configuration Variables.</li>
<li>Make sure to add key as ‘port’ and value is ‘8000’.</li>
<li>Set the buildpacks to Python 1st and NodeJS 2nd.</li>
<li>Connect GitHub repository.</li>
<li>Link the Heroku app to the repository.<li>
<li>Choose deployment method, this can be manual or automatic.</li>
<li>Click on Deploy.</li>
</ul>

<h2>Credits</h2>
<p>
Content – The content, idea, and code to make the project was created by myself. I sourced help from online platforms like YouTube to search for coding problem solving and more python coding videos to help me problem solve, I found Kayle Yang was really helpful.
I would like to thank Google for making the APIs and Google Worksheets for making the project possible. I would like to thank my Mentor Juilia, She has guided me through this project.
</p>
