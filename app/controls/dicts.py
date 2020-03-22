"""Contains dictionaries used by the ``controls`` blueprint.

var
---
socials : dictionary
    The value of each item in the dic is a tuple containing the name of the
    service that will be shown to the users and also a brief message indicating
    what kind of information to input into the form field of the
    ``/controls/socials`` page.
"""
profile = "Enter profile URL..."

feed = "Enter feed URL..."

email = "Enter email address..."

socials = {"twitter": ("Twitter:", profile),
           "facebook": ("Facebook:", profile),
           "pinterest": ("Pinterest:", profile),
           "linkedin": ("LinkedIn:", profile),
           "rssfeed": ("RSS Feed:", feed),
           "tumblr": ("Tumblr:", profile),
           "patreon": ("Patreon:", profile),
           "telegram": ("Telegram:", profile),
           "github": ("Github:", profile),
           "instagram": ("Instagram:", profile),
           "youtube": ("Youtube:", profile),
           "email": ("Email:", email)}
