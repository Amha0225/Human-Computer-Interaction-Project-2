# Human-Computer-Interaction-Project-2

a. Introduction: 
My web app is a event planner that allows users to input and see events, show a map of a location, and shows a forcast of the following days.

b. Usability goals:
-Inputting events: App will get user input on the name, date, time, and the place the event will take place in.
-Displaying Planned Events: App will display planned events, then they are apended in a JSON file. Then they are displayed in a table.
-Forecast: Ask user for location, as well as how many forecast days they want to see and if hourly. Then show a bar graph with parameters.
-Map: Using location given and its lat and lon create a map.

c. Design process: 
I sketched the basic elements of the site, I originally was going to use a sidebar, but decided to use tabs instead to naturally guide the user. I also had making and displaying the events separetly but decided to impliment them in the same tab so they are clearly shown. 

d. API integration: 
I utilized APIs both in creating the map and in forecast, I faced heavy challenges in the forecast as due to how the response is gathered I was unable to effectivly gather the information for the bargraph.

e. Interactive widgets:
-slider: Used to select how many days to see in forecast.
-select: Used to select parameter viewed in bargraph.
-text input: Allowed name and place of the event.
-date input: Allowed user to input date of the event.
-time input: Allowed user to input time of the event.

f. HCI design principles: Discuss how your web app adheres to HCI design principles.
  a. Information architecture: Tabs are clearly visible, described and labeled. Information needed for that section of the site are limited to those tabs.
  b. Navigation: Tabs are easily navigatable and widgits are .
  c. User feedback: Used various info and success messages to help guide and inform the user.
  d. Aesthetics: Maintain a visually appealing and professional design.

h. Conclusion: 
I struggled a lot with the API's, getting them to fuction and getting certain pieces of information out of them, expecially with the bargraph which I wasn't able to figure out.
