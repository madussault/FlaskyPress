FlaskyPress is a lightweight content management system (CMS) built with Flask.
It was initially developed as a personal project to learn and practice modern web development, while creating a functional and extensible platform for managing website content.

The goal of FlaskyPress is to provide a streamlined blogging and publishing experience without the complexity of larger platforms like WordPress. It’s a great starting point for developers who want to:

- Experiment with building a CMS from the ground up.
- Customize and extend a web application using Flask’s modular architecture.
- Quickly set up a simple blog or content-driven site.
 
 To see a live demo of the application click [here.](https://www.madussault.dev/demos/flaskypress/)
 
## Features

- **Markdown Support** – Write posts using the [Markdown language](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) for clean and easy formatting.  
- **Post Preview** – Preview posts before saving to ensure they look exactly as intended.  
- **Draft Management** – Save posts as drafts and publish them later when ready.  
- **Categorization** – Organize posts by assigning them to categories.  
- **Rich Media Embeds** – Automatically convert URLs from platforms like YouTube, Flickr, and Twitter into embedded content for seamless integration.  
- **Search Functionality** – Quickly find specific posts using the built-in search engine.  
- **Custom Sidebar Widgets** – Display any text or media in the sidebar using content widgets.  
- **Widget Ordering** – Easily reorder sidebar widgets to customize their layout.  
- **Social Media Links** – Add links to social accounts in the site footer.  
- **Custom Pages** – Create additional pages and link to them in the navigation bar.  
- **Dynamic Sitemap** – Automatically generate a sitemap for better site indexing.  
- **Error Reporting** – Configure the app to send error reports via email.  
- **Responsive Design** – Built with Bootstrap 4 to ensure a fully responsive layout across devices.

    
## Configuring the app

Before running FlaskyPress, you need to configure a few settings. All configuration values are stored in a `config.py` file located at the root of the project.

- **SECRET_KEY**: Set a secret key to enable session management and secure cookies.

- **SQLALCHEMY_DATABASE_URI**:  FlaskyPress uses the **SQLAlchemy ORM** for database management. SQLAlchemy supports a variety of relational databases such as **PostgreSQL**, **MySQL**, and more.  

  By default, FlaskyPress is configured to use **SQLite**, which works out of the box without additional setup.  
  If you’re fine with using SQLite, you can **omit** the `DATABASE_URL` entry from your `.env` file.

  However, if you prefer to use another database (for example, PostgreSQL), you must specify the connection URL in your `.env` file so FlaskyPress can connect through SQLAlchemy.
     
    ```SQLALCHEMY_DATABASE_URI = postgres+psycopg2://postgres:password@localhost:5432/books```
     
- **SITE_NAME**:  Defines the name of your site. This value is displayed as the **site branding** in the navigation menu. It is also used by the email error logger to **identify the application** when sending error notifications.

- **COPYRIGHT**:  Specifies the copyright information displayed in the **site footer**.

- **URL_PREFIX**:  Used when running the app from a **subdirectory** of your domain. For example, if your site is accessed at `www.my_website.com/subfolder/` instead of `www.my_website.com`, set this value to the subdirectory path.


The following settings, from **MAIL_SERVER** to **FROM_ADDRESS**, are only required if you want to receive email notifications when the application encounters an error. These values configure the **mail logger** that sends error reports:

- **MAIL_SERVER**: The address of the email server used to send error reports (e.g., `smtp.googlemail.com`). If this value is not set, the mail logger will be disabled.

- **MAIL_PORT**: The port used by your email service provider’s server. Check their documentation for the correct value.

- **MAIL_USE_TLS**: Enable encryption for outgoing emails to prevent eavesdropping. Set to `True` or `False`.

- **MAIL_USERNAME**: The username of the email account that will send the error reports.

- **MAIL_PASSWORD**: The password of the email account that will send the error reports.

- **ADMINS**: A list of email addresses that will receive error reports. Include your own email address here to receive notifications.

- **FROM_ADDRESS**: The email address used as the sender for error reports.


The remaining configuration attributes can typically be left at their **default values**. If you want to understand the purpose of each setting, detailed documentation is available in the **`Config`** class inside the `config.py` file.


## Usage

- #### Register:
    To be capable to post using the app we first need to register as an admin.
    To do so we simply go to the `/register` page and enter a new password.
    After logging in we'll have full privilege.

    ```
    http://127.0.0.1:5000/register
    ```
    
- #### Login:
    The web interface of the app does not include an hyperlink to the `/login`
    page. To reach the login form that will allow us to log in as an admin we instead
    type the address in the browser: 
     ```
     http://127.0.0.1:5000/login
     ```
     
- #### Adding Pages To The Navigation Bar:
    New pages can be created and their link added to the navigation bar by 
    going to `Pages` > `Create Page` in the navigation bar. If we want to 
    list all the published and unpublished pages we have created so far, we go
    to `Pages` > `Pages Index`.

    
- #### Drafts:
    Posts and pages can be saved as drafts. While creating or editing a 
    post/page, if the `Publish Now` box is left unchecked at the moment of 
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
    vice-versa, the configuration page for this feature can be accessed by 
    clicking on `Controls` > `Search Bar` in the navigation bar.
    
- #### Configuring The Use Of Categories:
    Categories can be displayed in two different ways by our app. The first one is on 
    the post itself in it's header section. The second one is by listing all
    the blog categories in a sidebar widget. It is also possible not to use 
    any category at all by disabling the feature. These choices can all be made 
    on the configuration page that we reach by clicking on `Controls` > `Categories` in the navigation bar.
    
- #### Displaying Social Addresses:
    To access the page allowing us to add social addresses in the footer, we click on `Controls` > `Social` in the
     navigation bar.
    
- #### Changing Sidebar Widget Orders:
    To access the page letting us reorder the widgets in the sidebar we 
    click on `Controls` > `Widget Orders` in the navigation bar.
