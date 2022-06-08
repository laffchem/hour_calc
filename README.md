# hour_calc!

View requirements.txt to see all required python packages.

This will eventually be deployed to a live webapp as it is still a work in progress. Right now you can run this locally and you can keep track of hours for any certification you may be working on. Keep in mind this was designed for a specific certification so not all attributes on the hours form will apply.

# Features:

User is able to add hours and denote if they were indepenedent or supervised as well as direct or indirect. This feature is mainly due to the nature of my wife's certification program in which she needs a certain number of hours that are supervised / independent as well as direct / indirect. If you don't need supervision, you probably don't need this app in the first place. You can leave it blank if you don't need it, but I haven't verified that it calculates correctly yet as that wasn't the focus in making this. That will come in future when I have a little more time.

This is the home page where you are able to view hours stored in the database that you input. From here you are able to delete any that were input by error.

![home page!](/images/home_page.png "Home Page")

This is the hours page where you are able to input any hours you are tracking. User is unable to input a start time that is greater
than the end time. This is validated server side so you'll have to redo the form if you commit that error. It's annoying but keeps your
database tidy.

![hours page!](/images/hour-sub.png "Hours Page")

After an hour is added, it is saved to the user's database using sql. The user is able to navigate to the hours page and pull up whichever month / year going as far back as 2000, and up to 2022 since we can't time travel forward. 

The hours in the table will be in 24 hour format as that was the easiest for me to have python do the calculations.

# To be added:
1. Password Reset (I lose mine all the time)
2. Change Password while logged in (If you want to for some reason)
3. Save data as a csv file

