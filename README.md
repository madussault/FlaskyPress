FlaskyPress is a lightweight content management system (CMS) built with Flask.
It was initially developed as a personal project to learn and practice modern web development, while creating a functional and extensible platform for managing website content.

The goal of FlaskyPress is to provide a streamlined blogging and publishing experience without the complexity of larger platforms like WordPress. It’s a great starting point for developers who want to:

- Experiment with building a CMS from the ground up.
- Customize and extend a web application using Flask’s modular architecture.
- Quickly set up a simple blog or content-driven site.
 
 To see a live demo of the application click [here.](https://www.madussault.dev/demos/flaskypress/)
 
## Features

- **Markdown Support** – Write posts using the [Markdown language](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) for clean and easy formatting.  
- **Post Preview** – Preview posts before saving.  
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

### Register
To start posting content, you must first **register as an admin user**.  
Navigate to the `/register` page, set a new password, and log in.  
Once logged in, you will have full administrative privileges.

    ```
    http://127.0.0.1:5000/register
    ```
---
    
### Login
The web interface does **not** include a direct link to the `/login` page.  
To log in as an admin, manually enter the URL in your browser:

     ```
     http://127.0.0.1:5000/login
     ```
---

### Adding Pages to the Navigation Bar
You can create new pages and add them to the site’s navigation bar by going to:  
`Pages` > `Create Page`.

To view a list of all published and unpublished pages, navigate to:  
`Pages` > `Pages Index`.

---
    
### Drafts
Posts and pages can be saved as **drafts** instead of being immediately published.

- While creating or editing a post/page, **uncheck** the `Publish Now` box before saving.
- The item will then be saved as a draft rather than published.

To view drafts, log in and click the `Drafts` link in the menu.

---
  
### Embedding Rich Media
FlaskyPress supports automatic embedding of rich media from providers such as **YouTube**, **Twitter**, and **Flickr**.

To embed media:

1. Copy and paste the URL of the media directly into the body of your post.
2. Make sure the URL is **in its own paragraph**, with no surrounding text.

**Example:**

    ```
    text here...

    https://youtu.be/LembwKDo1Dk

    text here...
    ```
### Automatic Hyperlinks
Plain URLs included in the body of a post are automatically rendered as **clickable links** when viewed.

---

### Moving the Search Bar
You can customize where the search bar appears:

- In the **navigation bar**, or  
- In the **sidebar**.

To configure this setting, go to:  
`Controls` > `Search Bar`.

---

### Configuring Categories
FlaskyPress provides flexible options for how categories are displayed:

1. **On individual posts** – shown in the header of the post.  
2. **In the sidebar** – displayed in a dedicated category widget.  
3. **Disabled** – hide categories completely.

To choose your preferred option, go to:  
`Controls` > `Categories`.

---

### Displaying Social Links
You can add links to your social profiles, which will be displayed in the footer of the site.  
To configure these links, navigate to:  
`Controls` > `Social`.

---

### Changing Sidebar Widget Order
Reorder sidebar widgets to customize their layout by going to:  
`Controls` > `Widget Orders`.
