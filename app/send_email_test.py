from flask import Blueprint, render_template, redirect, url_for, request, flash


def send_email(to, subject, template, sender):
    msg = Message(subject, recipients=[to], html=template, sender=sender)
    mail.send(msg)


html = render_template("activate.html", confirm_url="Hello")
subject = "Please confirm your email"
send_email("jeevan.bhoot@gmail.com", subject, html, "jeevan.bhoot@yahoo.com")
