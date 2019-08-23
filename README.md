## Email Parser and Username Generation - Burp Suite Extension

Burp Suite allows for extensions to be created in Python.  This is a Python extension that will parse email addresses out of selected URLs from the target tab and display them in the output window of the Extensions tab.  It will also generate a list of usernames from the emails found with basic permutations.

# Demo / More Information

[Blog Post - OxEvilC0de.com](https://0xevilc0de.com/finding-usernames-with-burp-extensions/)
[Demo - YouTube](https://youtu.be/Yf92sZ1sx6o)

# Dependencies

Download the latest version of [jython](http://www.jython.org) and configure Burp to use under Extender->Options->Python Environment.

# Installation

Add the Python script under Extender->Extensions.  During loading there is an output window that will inform you of any errors.

# Usage

From the Target tab, select any URLs that you have visited, right-click and select "Get Emails" or "Generate Usernames" from the context menu.

 Enjoy!