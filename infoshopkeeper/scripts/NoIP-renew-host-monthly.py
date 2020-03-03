#!/usr/bin/python

from robobrowser import RoboBrowser

browser = RoboBrowser()
browser.open("https://www.noip.com/members/dns/host.php?host_id=48545720")
browser.get_form(id="clogs")
form = browser.get_form(id="clogs")
form["username"] = "woodenshoebooks"
form["password"] = "woodenshoe"
browser.submit_form(form)
browser.get_forms()
browser.submit_form(browser.get_forms()[0])
