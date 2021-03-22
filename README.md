# insparty
Inspire / In Party

Inspire others by your ideas

Find teams that you want to contribute to

## Running locally
Clone the repo to your machine:
```console
$ git clone git@github.com:adinsoon/insparty.git
```
Then setup .env.template file and re-name it to .env
```env
#example
DEBUG=1

SERVER_IP=domain.tld
DEV_IP=0.0.0.0
DJANGO_PORT=8080
DJANGO_SETTINGS_MODULE=config.settings

SECRET_KEY=!!pleasechangeme!!

POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=!!pleasechangeme!!
POSTGRES_SERVICE=postgres
POSTGRES_PORT=5432
DATABASE=postgres

EMAIL_BACKEND=some-backend
EMAIL_HOST=some-host
EMAIL_HOST_USER=yourmail@example.com
EMAIL_HOST_PASSWORD=!!pleasechangeme!!
EMAIL_PORT=587
EMAIL_USE_TLS=True
```
In the main directory, open your terminal and run container
```console
$ docker-compose up
```
After building the image if needed and passing tests, you should be ready to open the server in your browser:
```console
ins_back    | Ran XXX tests in XX.XXXs
ins_back    | 
ins_back    | OK
ins_back    | --------------------------
ins_back    | Fixing ownership of files
ins_back    | --------------------------
ins_back    | --------------------------
ins_back    | Run command
ins_back    | runserver X.X.X.X:xxxx
ins_back    | --------------------------
ins_back    | Watching for file changes with StatReloader
ins_back    | Performing system checks...
ins_back    | 
ins_back    | System check identified no issues (0 silenced).
ins_back    | MM - DD, YYYY - HH:mm:ss
ins_back    | Django version 3.x.x, using settings 'config.settings'
ins_back    | Starting development server at http://X.X.X.X:xxxx/
ins_back    | Quit the server with CONTROL-C.
```

## Q&A Collection
### Technical section  
In this part I would like to explain some of my technical decisions during development. Like why I did this instead of that and etc.  
Some of them are already explained in the code but some of them might be interesting for further discussion.

- #### Why are you using Docker and Docker-compose?  
Docker containers encapsulate everything an application needs to run (and those things only) and allow applications to be shuttled easily between environments.
And in accordance to this great [Docker documentation](https://docs.docker.com/compose/#development-environments):  
> The Compose file provides a way to document and configure all of the application’s service dependencies (databases, queues, caches, web service APIs, etc). 
> Using the Compose command line tool you can create and start one or more containers for each dependency with a single command (docker-compose up).    
 
So, instead of having to run each component individually, worry about their up-to-date status or installation, I use Docker.
- #### Why did you decide on a custom user model?
For example, I was able to adjust the user model to my own preferences, including logging in via e-mail.  
Using your own user model makes it much easier to extend in the future.  
It is important to set **AUTH_USER_MODEL** in settings.py to the new custom user model.
- #### Why there is set_new_username and set_new_email methods in your user model?  
Based on the concept of custom user model, email and username for each user must be unique. These methods allow you to validate field changes for username and email.
- #### Why are you using Faker and Factories?   
Faker and Factories enable comprehensive testing without the need to create static names, passwords, or strings. It's very convenient.
- #### Why is the programmic experience a choice field?
Due to simplicity and ease of choice. And, like with real job offers or interviews, one senior's experience may be different from another, a junior's differ from another, and so on. They are rather loose estimates of advancement.
- #### Why Experience class landed in techstack?
It turned out that its use will be in at least two places: for the user and idea. So it would be strange to import it from the user app for the idea, while it would be pointless to initiate it twice throught the whole project. As all models imported from techstack appear in both the user and idea models, the additional one import of Experience was just cherry on top. 
- #### Why did you decide to go for abstract tech class in techstack?  
I wanted to put some common data formats into a number of other models and it was a great opportunity to take advantage of abstract class use.   
Meanwhile, I expanded the choice of available "properties" of idea or user, so I was able to conveniently extend them using inheritance.
- #### Why SlugField in the idea?   
SlugField is a more human-readable form of identifying idea that works well as a part of url (way better than yoursite.xyz/idea/120). Going a little ahead with thoughts it's also better processed by SEO.
- #### Should you change title_slug value every time title is changed?
This is probably not a good idea. Taking into account the url mechanism for a given idea, slug is its integral part. If it changes every time, potential visitors will have trouble finding the idea next time, let alone adding it to their bookmarks! I thought about implementing a slugfield change, but these issues made me dismiss it. So, think twice before creating a title for an idea! Or create a new one.
- #### Why is the programmic experience a multichoice field in idea model unlike the user?  
The user is responsible only for himself, while the idea may consist of a group of various people, whose experience may differ as well. Hence the founder can choose what range of experience he expects in people who would like to join his idea.
- #### Why description is required for Idea model?  
I assume that if someone came up with an idea and is looking for people willing to join it, one should take care of its description, which will explain his point of view and attract interested people. The title of the idea itself is not very encouraging to participate and doesn't really prove that the idea is innovative, does it?
- #### Why creating Ideas is limited per user?
Quality over quantity. And to prevent from uncontrolled amount of creating Ideas that are unlikely to be groundbreaking every time.
- #### Why Redis?
Redis can function both as broker, database and cache. It's very light and fas, hence grabbed my attention. But I do not rule out changing to RabbitMQ in the future due to its large task handling and SSL configuration.
- #### How do you want to use Celery?
Celery is a great tool for handling background tasks. Its use will surely be found in sending activation links for newly created accounts. There is also a lot of potential to use it to support the Idea invitation system.
- #### What are you using signals for?
Not everything can be done by overriding the save method, and it's not always a viable choice. I use signals for example to conveniently set up Founder and Finder models for each created account.
- #### How do you make sure your code is covered by tests?
I use cool feature named coverage for this, which reports for me every time the docker is up. I try to keep the whole project in around 90% coverage. Not every code line is needed for coverage.
