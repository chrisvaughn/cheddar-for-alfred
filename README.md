We love using [Cheddar](https://cheddarapp.com/) and [Alfred](http://www.alfredapp.com/) and thought why not bring these two together! Cheddar for Alfred does just that.

## Installing the Extension

* [Download](https://github.com/downloads/chrisvaughn/cheddar-for-alfred/CheddarForAlfred.alfredextension) the extension file
* Open the downloaded CheddarForAlfred.alfredextension to import it into Alfred

_Note: Alfred extensions are available for Alfred PowerPack users._

## Using Cheddar For Alfred

For Cheddar For Alfred (CA) to create tasks in Cheddar you must connect the extension to your Cheddar account. CA tries to make this easy for you by automatically starting the process the first time you create a task. A browser window will open, asking you to allow Cheddar For Alfred to connect to your Cheddar account.

CA is set up to use the Alfred keyword 'ca'. It also uses Growl notifications for alerts. If you don't have Growl installed and enabled, CA will work, but you will not get any notification that the action is completed.

##Commands

To create a task (where mylist is the name of your list):

	ca mylist "what do want the task to say"


CA tries to match the list you want. If you have a list called "Things to do Tomorrow" you can create a task with

	ca tomorrow "This is something I should do tomorrow"

	ca tomor "This is something I should do tomorrow"

	ca "things to do" "this is something I should do tomorrow"

Quotes are required around the the list name and task content if multiple words are used.

Other Commands

  *help* - display help menu

  *lists* - display all your lists

  *reset* - remove stored data to reset CA to new install

---

Want to contribute to the development of Cheddar for Alfred? Submit a pull request!

##Change Log
* July 17, 2012 - v1.0 - Inital Release