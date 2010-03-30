#!/usr/bin/env python

import cgi
import numpy


data = {"Cs" : [8.22127, -4006.048, -0.00060194, -0.19623]}
# One unit is this many torr
units = {"torr": 1.0, "Pa" : 7.5006e-3, "bar" : 750.06, "at" : 735.56, "atm": 760.0, "psi": 51.715}

def calcp(element, T):
    global data, units
    if not data.has_key(element):
        return 0
    p = pv(T, data[element])
    print "<table>"
    print "<tr><td class=\"resultheader\">Vapour pressure of %s @ %d K:</tr></td>" %(element, T)
    showresult(p,"torr")
    for k in units.keys():
        if k != "torr":
            showresult(convert(p, "torr", k), k)
    print "</table>"

def showresult(value, unit):
    print "<tr><td class=\"result\"><font class=\"value\">%.3e</font> <font class=\"unit\">%s</font> </tr></td>" %(value, unit)

def convert(value, fromunit, tounit):
    global units
    temp = value * units[fromunit]
    return temp / units[tounit]

def pv(T,C):
    return 10**(C[0] + C[1]/T + C[2] * T + C[3] * numpy.log10(T))

def main():
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    print "<html><header><link rel=\"stylesheet\" type=\"text/css\" href=\"/vapourdata/show.css\" /></header><body>"
    print "<h2>Vapour pressure</h2>"
    if form.has_key("element")  and (form["element"].value != ''):
        if form.has_key("temperature"):
            try:
                T = int(form["temperature"].value)
                if (T > 0):
                    calcp(form["element"].value, T)
            except:
                pass

    print "<br><br>"
    print "<form action=\"\">"
    print "Select element: <select name=\"element\">"
    for k in data.keys():
	if form.has_key("element") and form["element"].value == k:
		sel = 'selected'
	else:
		sel = ''
        print "<option value=\"%s\" %s>%s</option>" %(k, sel, k)
    print "</select><br>"
    print "Temperature: <input type=\"text\" name=\"temperature\"> K<br>"
    print "<input type=\"Submit\" value=\"let's go\">"
    print "</form>"
    print "</body></html>"

main()
