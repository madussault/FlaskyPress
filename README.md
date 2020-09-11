FlaskyPress is a basic blogging application written in python and powered by
 the Flask framework. The project was started to learn back-end web
  development.
 
 To see a live demo of the application click [here.](https://www.madussault.dev/demos/flaskypress/)
 
 ## Features:
 
 - Can write posts using the [markdown language](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).
 - Can preview posts before saving.
 - Can save posts as drafts.
 - Posts can be classified by categories.
 - Converts URLs into embeds from pages containing rich medias
  (Youtube, Flickr, Twitter, etc..) for use in the creation of posts.
 - Search engine to find specific posts.
 - Can display any text or medias in the sidebar using content widgets.
 - Can re-order widgets in the sidebar.
 - Link to social accounts in the footer.
 - Can add new pages and link to them in the navigation bar.
 - Dynamically generated sitemap.
 - Can be set to send error reports by email.
 - Made fully responsive using Bootstrap 4.
    
## Configuring the app

To configure this application we recommend using an `.env` file. The attributes to set can be found in the `Config` class. Below we give explanations about some of these attributes.

- **SECRET_KEY**: Input your own unique and secret key here. It will be used
 to protect against CSRF attack and to cryptographically sign cookies.

- **SQLALCHEMY_DATABASE_URI**: For storing the posts and passwords of the users into a
 database we use SQLAlchemy, which is a program allowing us to manage a
  database in a more pythonic way than using raw SQL queries. SQLAlchemy 
  supports a variety of relational databases ( Postgresql, MySQL
  , etc...) but out of the box FlaskyPress is configured to use SQLite.
  If you are fine with using this database you can omit the `DATABASE_URL`
   attribute from your .env file. But if you would prefer to use an other
    database, like let's say Postgresql, you would need to specify the path
     to the database in the .env file so it can be connected to SQLAlchemy.
      Example:
     
     ```SQLALCHEMY_DATABASE_URI = postgres+psycopg2://postgres:password@localhost:5432/books```
     
- **SITE_NAME**: Will show up as site branding in the menu. It will also be
 used by the mail logger to identify our app when an error message is being
  sent.
  
- **COPYRIGHT**: Copyright info that will be shown in the footer.

- **URL_PREFIX**: Only needed when we want to run our app from a domain subdirectory,
            ex: `www.my_website.com/subfolder/` instead of `www.my_website.com`.

The next attributes from **MAIL_SERVER** to **FROM_ADDRESS** only need to be
 set if we want to be informed by email when the application crashes. These
 attributes are used to configure the mail logger sending us error reports :

- **MAIL_SERVER**: Address of the email server our mail logger is going to
 use to send our email reports (ex, `smtp.googlemail.com`). If this value is
  not
  set the mail logger will be disabled.
    
- **MAIL_PORT**: Port used by the mail server of your email service provider. Consult their website to find out.

- **MAIL_USE_TLS**: Enable encryption when sending email, which prevent
 eavesdropping. Set to `True` or `False`.
 
- **MAIL_USERNAME**: Username for the email account sending the error reports.

- **MAIL_PASSWORD**: Password for the email account sending the error reports.

- **ADMINS**: Here we store a list of the email addresses that will receive
 the error reports, so your own email address should be in that list.
 
- **FROM_ADDRESS**: Email address of the account sending the error reports.

The other configuration attributes can be left at their default values.
 If there's a need to know what role each of them are playing, documentation 
 can be found in the `Config` class of the `config.py` file.

## Usage

- #### Register:
    To be capable to post using the app we first need to register as an admin.
    To do so we simply go to the `/register` page and enter a new password.
    After logging in we'll have full privilege.

    ```
    http://127.0.0.1:5000/register
    ```
    **Note**: For the moment the registration system can only accept one user.
    Multi-user registration will be implemented in the future.
    
- #### Login:
    The web interface of the app does not include an hyperlink to the `/login`
    page. To reach the login form that will allow us to log in as an admin we instead
    type the address in the browser: 
     ```
     http://127.0.0.1:5000/login
     ``` 
- #### Adding Pages To The Navigation Bar:
    New pages can be created and their link added to the navigation bar by 
    going to to the following page: first we click on the `Pages` dropdown menu
    in the sidebar and then after we click on `Create Page`. If we want to 
    list all the published and unpublished pages we have created so far, we choose 
    `Pages Index` in the same dropdown menu.

    
- #### Drafts:
    Posts and pages can be saved as drafts. While creating or editing a 
    post/page, f the `Publish Now` box is left unchecked at the moment of 
    saving, the post/page will be saved as a draft instead of being published. 
    Drafts can be viewed by a logged-in user by clicking on the `Drafts` 
    hyperlink in the menu.
  
- #### URL to Embeds:
    To embed rich medias from select providers (Youtube, Twitter, Flickr, etc...) 
    we can simply copy/paste the web address to the media in the body of our
    post and FlaskyPress will convert it into an embed when rendering the post.
   
    **Note:** For this feature to work the URL must be placed in it's own
    paragraph without any text surrounding it. Example:
    ```
    text here...

    https://youtu.be/LembwKDo1Dk

    text here...
    ```
- #### URL to Hyperlink:
    The URLs typed in the body of our posts will be rendered by the application
    as clickable links instead of plain text at the moment of viewing. This
    feature will not be applied to URLs of pages hosting select rich medias
   (Youtube videos, Flickr images, etc...).
   
- #### Changing Search Bar Placement:
    If we want to move the search bar from the navigation bar to the sidebar or
    vice-versa, the configuration page for this feature can be accessed by first 
    clicking on the `Controls` dropdown menu in the sidebar and then after 
    clicking on `Search Bar`.
    
- #### Configuring The Use Of Categories:
    Categories can be displayed in two different ways by our app. The first one is on 
    the post itself in it's header section. The second one is by listing all
    the blog categories in a sidebar widget. It also possible not to use 
    any category at all by disabling the feature. These choices can all be made 
    on the configuration page that we reach by first clicking on the `Controls` 
    dropdown menu in the sidebar and then after clicking on `Categories`.
    
- #### Displaying Social Addresses:
    To access the page allowing us to add social addresses in the footer, we must
    first click on the `Controls` dropdown menu in the sidebar and then after 
    click on `Social`.
    
- #### Changing Sidebar Widget Orders:
    To access the page letting us reorder the widgets in the sidebar we first 
    click on the `Controls` dropdown menu in the sidebar and then after on 
    `Widget Orders`.