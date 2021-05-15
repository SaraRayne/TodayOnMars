Welcome to Today On Mars.

Today on Mars is a mock website for a Mars colony. It features daily weather updates, images of the red planet captured by rovers, and forums for colonists to collaborate and connect.
The goal was to make the website look and feel like something that could actually be utilized by Mars colonists as a central site.

Necessity of project: You'll need an API key to get photos from NASA, which you can do here: https://api.nasa.gov/. Set your API key as an environment variable named "NASA_API",
or manually add it to the code here: TodayOnMars/Mars/views.py --> just under includes --> API_KEY= {enter your key here}
You should also select Register in the navigation bar, and create an account in order to be able to create forum threads and reply to existing ones.

The navigation of the site is fairly simple:
1. The main page (index.html) features an artist's rendition image of a Mars rover, three of the latest forum threads, and a weather widget displaying the most recent weather on Mars
(averaged out using the max and min temps for the day),provided by the Perseverance rover. The widget also shows the sol date (number of "Mars days" the rover has been on the planet),
and the corresponding day on Earth.
2. The forums page (forums.html) contains, you guessed it, forums. You can filter by the topic of the forum threads, search keywords in the forums with the search bar, and create a new
post using the "Create a Post" button (but only if you're logged in), which when clicked will reveal a form. Clicking on the title of any of the forum posts will take you to that posts's page,
where you can see the full thread content, including any replies. You can also add your own reply, provided you're logged in. The forum threads cannot be deleted or edited, and this was
done purposefully with the idea that if this is a colony run by an official agency, all posts should be visible to that agency and no one should be able to hide anything (full transparency).
Though my original intention was to keep things serious, the forums do take on a somewhat silly feel as it's much easier to come up with humorous rather than serious mock posts.
3. The page "Image of the Day" will retrieve an image taken by the Mars Curiosity rover. If there was no photo taken on a particular day by the rover, a "No Image Available" photo will appear.

File Contents:
1. views.py
The views.py file contains all the views and functions necessary for rendering the pages. The index page has the ability to pull weather data as well as render recent forum threads.
The day retrieved by the weather code will not correspond perfectly to the "actual" date; I've set the function to retrieve the first item in the list, which will be the weather
data for 7 days previous, so as not to encounter an Index Error if the list shortens up unexpectedly (the API isn't published publicly, I retrieved it from the source code of NASA's
weather page, so I'm not certain of its behavior). Most of the other views handle the forums and thread pages, with the exception of 'image', which retrieves an image from NASA's API.

2. models.py
The models.py file contains 4 models: one for Users, one for Threads, one for Replies, and one for Categories. Replies are connected to their corresponding Thread via ForeignKey.

3. Templates Folder
The templates folder contains all the necessary html pages: layout (for the navigation bar and heading picture + title), index (for the home page), forums (for the forums page),
images (to render an image of the day), thread (for individual threads), login, and register.

4. Static Folder
Static contains two images, one that is present on each page (the Mars rover), and one that renders in images.html if an image for the day can't be found. It also has a styles.css file,
and two Javascript files. I decided against making this a single page app as I felt it would add unnecessary complications, so I have two Javascript files for the two pages that have JS logic.
Index.js is for the forums page (I didn't change the name of the file after deciding not to use just one JS file, but it really should be forums.js). The purpose of this JS file is to
show the forum categories when the filter button is clicked, as well as show/hide the "Create a Post" form. The form appears when the "Create a Post" button is clicked, but if the user
clicks outside of the form (for instance, if they've decided against writing a post), the form will be hidden again and the button will appear. The second JS file, thread.js, has the same
show/hide functionality, but for the "Reply" button and form.

I abandoned the idea of adding a news section because I wanted to put more effort into styling than I normally do. I felt that the News page would be fun but unnecessary if I put more effort
into other parts of the site. Given the amount of time it took me to get the look just right, I'm happy with that decision.

I don't think there are any other details that need to be shared. The site is fairly simplistic, perhaps more simplistic than I had hoped, but I had fun playing around with NASA APIs, which
is really what I wanted to be able to do with this project. I am also very proud of the styling; that is my least favorite part (I prefer to make it work, not make it look good), and I
spent a lot of time tweaking this and that and reading up on better ways to style everything from a simple div to the sometimes confusing flex boxes. Hope you enjoy!
