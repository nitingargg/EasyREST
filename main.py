import ttkbootstrap as tb
import requests
import json

root = tb.Window(themename="superhero")
root.title("EasyRestClient")
root.geometry("800x800")
root.maxsize(800,800)
root.minsize(800,800)

# all vars
selected = tb.StringVar()
url = tb.StringVar()

# all functions

def getHeaderJSON():
    data = t1.get(1.0,"end-1c")
    if(data==""):
        a = dict()
        return a
    try:
        myjson = json.loads(data)
        return myjson
    except:
        stat.configure(text="Invalid Headers")
        return 0


def getJSONbody():
    data = t2.get(1.0,"end-1c")
    if(data==""):
        a = dict()
        return a
    try:
        myjson = json.loads(data)
        return myjson
    except:
        stat.configure(text="Invalid JSON")
        return 0

def prettifyHeaders():
    data = t1.get(1.0,"end-1c")
    try:
        myjson = json.loads(data)
        t1.delete('1.0',tb.END)
        formatted = json.dumps(myjson,sort_keys=True, indent=2)
        t1.insert(tb.END,formatted)
        stat.configure(text="Headers Prettified")
    except:
        stat.configure(text="Invalid Headers")

def prettifyJSON():
    data = t2.get(1.0,"end-1c")
    try:
        myjson = json.loads(data)
        t2.delete('1.0',tb.END)
        formatted = json.dumps(myjson,sort_keys=True, indent=2)
        t2.insert(tb.END,formatted)
        stat.configure(text="JSON Prettified")
    except:
        stat.configure(text="Invalid JSON")


def clear_output():
    body_txt.delete('1.0',tb.END)

def displayJSON(myJSON):
    clear_output()
    json_formatted_str = json.dumps(myJSON,sort_keys=True, indent=2)
    body_txt.insert(tb.END,json_formatted_str)


def handle_request():
    
    clear_output()
    
    url_ = url.get()
    method = selected.get()
    headers = getHeaderJSON()
    jsonBody = getJSONbody()

    if(headers==0 or jsonBody==0):
        return 

    if(url_==""):
        stat.configure(text="Empty URL!")
        return

    if(method=="GET"):
        try:
            r = requests.get(url_, headers=headers, json=jsonBody)
        except:
            clear_output()
            stat.configure(text="Invalid URL")
            return
    elif(method=="POST"):
        try:
            r = requests.post(url_, headers=headers, json=jsonBody)
        except:
            clear_output()
            stat.configure(text="Invalid URL")
            return
    elif(method=="PUT"):
        try:
            r = requests.put(url_, headers=headers, json=jsonBody)
        except:
            clear_output()
            stat.configure(text="Invalid URL")
            return
    elif(method=="DELETE"):
        try:
            r = requests.delete(url_, headers=headers, json=jsonBody)
        except:
            clear_output()
            stat.configure(text="Invalid URL")
            return
    else:
        print("Invalid Method")
    
    try:
        output = json.loads(r.content)
        displayJSON(output)
        stat.configure(text=r.status_code)
    except:
        clear_output()
        body_txt.insert(tb.END,r.content)
        stat.configure(text="Cannot Decode JSON")

def close():
    root.destroy()

def about():
    sub = tb.Toplevel()
    sub.geometry("400x200")
    sub.title("About")
    sub.maxsize(400,200)
    sub.minsize(400,200)
    l1 = tb.Label(sub,text="EasyREST Client", font=("Inter",16,"bold"), bootstyle="info")
    l1.place(relx=0.5, rely=0.2, anchor="center")
    l1 = tb.Label(sub,text="Developed with love by Nitin Garg", font=("Inter",10,"italic"), bootstyle="info")
    l1.place(relx=0.5, rely=0.4, anchor="center")
    b1 = tb.Button(sub, text="Linkedin", width=15, bootstyle="info-outline")
    b1.place(relx = 0.3, rely=0.6, anchor="center")
    b2 = tb.Button(sub, text="Github", width=15, bootstyle="info-outline")
    b2.place(relx = 0.7, rely=0.6, anchor="center")
    l2 = tb.Label(sub,text="Copyright © 2023 Nitin Garg", font=("Inter",12,"bold"), bootstyle="light")
    l2.place(relx=0.5, rely=0.85, anchor="center")


#menubar and title
title = tb.Label(root,text="Easy Rest Client", font=("Inter",15,"bold"),border=15,bootstyle="light" )
title.place(x=10,y=0)

menuBar = tb.Frame(root,bootstyle="info", width=550, height=50)
menuBar.place(x=250, y=0)

#menubar options

byText = tb.Label(menuBar, text="by Nitin Garg", bootstyle="info", font=("Inter",16,"bold"))
byText.place(anchor="center", rely=0.5, relx=0.18)

mb1 = tb.Button(menuBar,width=10, text="About", bootstyle="dark", command=about)
mb1.place(relx=0.6, rely=0.5, anchor="center")

mb2 = tb.Button(menuBar,width=15, text="Close Application",  bootstyle="dark", command=close)
mb2.place(relx=0.85, rely=0.5, anchor="center")


options= ["GET","POST","PUT","DELETE"]

type = tb.OptionMenu(root, selected, "GET", *options, bootstyle="info")
type.place(relx=0.2, rely=0.14, anchor="center")

txt = tb.Entry(root,width=40, textvariable=url)
txt.place(relx=0.5, rely=0.14, anchor="center")

bt = tb.Button(root,text="Send", width=10, command=handle_request,bootstyle="info")
bt.place(relx=0.8,rely=0.14,anchor="center")



nb = tb.Notebook(root,bootstyle="dark")
nb.place(relx=0.5, rely=0.35, anchor="center")

# frame1 (Headers)

frame1 = tb.Frame(nb)
frame1.pack()

t1 = tb.Text(frame1, width=40, height=10)
t1.pack()

# frame2 (Body)

frame2 = tb.Frame(nb)
frame2.pack()

t2 = tb.Text(frame2, width=40, height=10)
t2.pack()

nb.add(frame1, text="Headers")
nb.add(frame2,text="Body")

bt1=tb.Button(root,bootstyle="info", text="Prettify Headers", command=prettifyHeaders)
bt1.place(anchor="center", relx=0.15, rely=0.4)

bt2=tb.Button(root,bootstyle="info", text="Prettify JSON", command=prettifyJSON)
bt2.place(anchor="center", relx=0.85, rely=0.4)

stat_frame = tb.LabelFrame(root,bootstyle="info", text="Status Bar")
stat_frame.place(anchor="center", rely=0.55, relx=0.5)

stat = tb.Label(stat_frame,text="",bootstyle="info", font=("Inter",14, "bold"), width=30)
stat.pack(padx=8, pady=4)

outputFrame = tb.LabelFrame(root,bootstyle="info", text="Response")
outputFrame.place(anchor="center", rely=0.8, relx=0.5)

body_txt = tb.Text(outputFrame,width=60, height=9,font=("Consolas",10,""), wrap="word")
body_txt.pack(padx=8, pady=8)


root.mainloop()