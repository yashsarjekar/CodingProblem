# Problem 1
There are 1,00,000 images. We need to find the width and height of each image. Depending on the dimensions we would need to resize it down to 600 x 480. We have a machine which has 4gb Ram and 2 core vcpu. What is the fastest way to go through the 1L images?

# Problem 2
There is a manual QC process which happens. There is a portal from which each individual qc task is assigned. The portal needs to check how many qc persons are logged in and which of the logged in persons are free, as in not on a task, and automatically assign tasks. Once the task is finished the person will automatically get assigned the next task if any is pending. How would you architect this? I want to understand step by step the methodology you used to come to the final solution. Can you illustrate a basic API framework written in Python using Flask and SQLite as the database.