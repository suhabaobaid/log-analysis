# Log Analysis

## Project Overview
This is the third project for the course[ FullStack Nanodegree by Udacity](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004 " FullStack Nanodegree by Udacity")
### Objective
The objective is to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like. The database and data are provided and mimic real-world data.
### Given
The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.
### Questions to be Answered
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?
## Running the Project
### What you need
- Python
- Vagrant
- Virtual Box
##### Installing dependencies and Downloading data
1. Install [Vagrant](https://www.vagrantup.com "Vagrant")
2. Install [VirtualBox](https://www.virtualbox.org "VirtualBox")
3. Download or clone [fullStack repo](https://github.com/udacity/fullstack-nanodegree-vm "fullStack repo")
4. Download the [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip "data") folder here
5. Unzip this folder after downloading it. The file inside is called newsdata.sql
6. Copy the newsdata.sql file and content of this current repository in the directory \vagrant in the FullStackRepo directory downloaded, from step 3 (there should be catalog, forum, tournaments in the same directory)
#### Launching the virtual machine
1. Open the terminal and head to the vagrant directry fullstack-nanodegree-vm folder. Launch the Vagrant VM using command:
```
vagrant up
```
2. After the setup is done, log into the VM using this command:
```
vagrant ssh
```
3. Change the directory to vagrant(this is the shared folder, use ls command):
```
cd /vagrant
```
4. To log out of the VM use ctrl-C or the command (it may be needed to be done twice):
```
exit
```
#### Setup the database
1. Load the data, while being logged in the VM, with this command:
```
psql -d news -f newsdata.sql
```
2. The news database includes three tables, mainly log, authors and articles. Check their details by connecting to the database:
```
psql -d news
```
3. Create Views, while connected to the news database:
This a view needed for the running of the program
```
CREATE VIEW articles_view AS
SELECT title, author, count(log.id) AS views
FROM articles, log where log.path LIKE concat('%', articles.slug)
GROUP BY title, author 
ORDER BY views DESC;
```
#### Running the queries
1. From the vagrant directory (within the virtual machine) run the program by:
`python logAnalysis.py`

#### Output
You should get an output as logAnalysisOutput.txt in your terminal


