![ICO](/static/og-image.ico)
# CS50x-final-project

I am Amirali and this is my CS50 final project.

#### the languages that I used are:
- python for server side using flask framework
- html, CSS, and JavaScript
- SQLite for managing the databases
<hr>
This app is a TODO website. Via this web application, you can manage your daily tasks and organise them. You can also have your tasks as groups. This helps you to find your tasks faster.

You need to first login to your account, or, if you do not have one you need to register.
When you register, in the server side, the app stores the details that you have entered, but it just stores the hash of your password which is more secure.

When you login, the app looks for username and password that you typed in in the database, and none of them matches, it redirects you to the login page and shows you error.

You can even change your password.

The app email you by doing any of these operations:
- registering a new account
- changing password

After logging in, you can start using this app by adding your tasks.
> you can specify:
> - date of the task
> - time of the task
> - task group or type of the task

After adding a task, you can delete it, and mark it as done or to-do, by checking the check box.
