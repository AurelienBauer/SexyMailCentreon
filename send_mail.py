#!/usr/bin/env python3

from jinja2 import Environment, select_autoescape, FileSystemLoader, exceptions
import sys, os


def get_template():
    path = "mail.hmtl"
    if len(sys.argv) > 3 and sys.argv[2] == "-f":
        path = sys.argv[3]
    env = Environment(
        loader=FileSystemLoader('%s/' % os.path.dirname(__file__)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env.get_template(path)


def help():
    print("./send_mail -service|-host|-h options values\n"
          "\t-service #for services notifications\n"
          "\t-host #for hosts notifications\n"
          "\t-h #display command details\n"
          "Options :\n"
          "\t-f <path> #mail pattern, must be a HTML file."
          " If this option isn't used, the script will search for a file named \"mail.html\"\n"
          "Values :\n"
          "\t--notificationtype <value> #for hosts and services notifications\n"
          "\t--hostname <value> #for hosts and services notifications\n"
          "\t--hostaddress <value> #for hosts and services notifications\n"
          "\t--hoststate CRITICAL|WARNING|OK #for hosts notifications only\n"
          "\t--hostoutput <value> #for hosts notifications only\n"
          "\t--hostalias <value> #for services notifications only\n"
          "\t--servicedesc <value> #for services notifications only\n"
          "\t--servicestate UP|DOWN #for services notifications only\n"
          "\t--serviceoutput <value> #for services notifications only\n"
          "\t--contactmail <value> #for hosts and services notifications\n"
          "\t--date <value> #for hosts and services notifications\n"
          "If one or more values are not set, They'll take the empty string value (\"\")."
          )
    exit(1)


def parseHost():
    keys = ["--notificationtype", "--hostname", "--hostaddress", "--hoststate", "--hostoutput",
            "--contactmail", "--date"]
    values = {"notificationtype": "", "hostname": "", "hostaddress": "", "hoststate": "", "hostoutput": "",
              "contactmail": "", "date": ""}
    i = 0
    for arg in sys.argv:
        if arg in keys:
            values[arg[2:]] = sys.argv[i+1]
        i += 1
    if values['hoststate']:
        values['color'] = {"DOWN": "#E53935", "UP": "#43A047"}[values['hoststate']]
    return values


def parseService():
    keys = ["--notificationtype", "--hostname", "--hostaddress", "--hostalias", "--servicedesc",
            "--servicestate", "--serviceoutput", "--contactmail", "--date"]
    values = {"notificationtype": "", "hostname": "", "hostaddress": "", "hostalias": "",
              "servicedesc": "", "servicestate": "", "serviceoutput": "", "contactmail": "", "date": ""}
    i = 0
    for arg in sys.argv:
        if arg in keys:
            values[arg[2:]] = sys.argv[i+1]
        i += 1
    if values['servicestate']:
        values['color'] = {"CRITICAL": "#E53935", "WARNING": "#FB8C00", "OK": "#43A047"}[values['servicestate']]
    return values


def main():
    try:
        values = ({"-h": help, "-host": parseHost, "-service": parseService}[sys.argv[1]])()
        template = get_template()
        print(template.render(values))
    except KeyError:
        print ("A bad value has been used.\nUse send_mail -h")
        return 0
    except exceptions.TemplateNotFound:
        print ("HTML file not found, Use -f option for specify a path.")
        return 0
    return 1


if __name__=="__main__":
    main()


    #HOST : UP/DOWN
    #SERVICES : CRITICAL/WARNING/OK