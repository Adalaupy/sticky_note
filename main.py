from flask import Flask, render_template, request

app = Flask(__name__)



my_txt_path = "note.txt"


# open the text file
def open_txt():

    with open(my_txt_path,"r") as file:
    
        note = file.read()

    
    itemList = ["Title" + x for x in note.split("Title") if x!= "\n"]

    return itemList




# convert content of the .txt into dictionary
def txt_json():
    
    itemList = open_txt()
    
    full_dict = []


    
    for i in range(len(itemList)):
    
        str = itemList[i]

        title = str[0:str.index('\nCatergory')]
        Cat = str[str.index('\nCatergory'):str.index('\nSub-Category:')]
        sub_cat = str[str.index('\nSub-Category'):str.index('\n\n')]
        content = str.replace(title,'').replace(Cat,'').replace(sub_cat,'')[1:].strip()

        record_dict = {"id": i + 1,"title": title,"category": Cat, "sub_category": sub_cat, "content" : content}

        full_dict.append(record_dict)
   
    
    return full_dict





# Filter 
def filter_list(filter,dict,type):

    
    
    
    if filter != "All":


        # For Category: Only keep the record that you want, the items inside option List for filtering is remain unchange, and the selected object will be kept in selected status
        if type == "cat":

        
        
            display_dict = [d for d in dict if d['category'].replace('\nCatergory: ','') == filter]

            filterList = list(set([d['category'].replace('\nCatergory: ','') for d in full_dict ]))
            filterList.insert(0,filterList.pop(filterList.index(filter)))
            filterList.append('All')


        # For Sub-Category: Only keep the record that you want, then items inside the option List refer to the filtered Category, and the selected object will be updated to "All" again after submit
        elif type == "sub":

            display_dict = [d for d in dict if d['sub_category'].replace('\nSub-Category: ','').replace('\nSub-Category: ','') == filter]

            filterList = list(set([d['sub_category'].replace('\nSub-Category: ','')for d in display_dict ]))

            filterList.insert(0,'All')





    # Category filter is unselected: display All records and Category filter option, 'All' is selected by default 
    elif filter == "All" and type == "cat":
        
        display_dict = full_dict.copy()
        filterList = list(set([d['category'].replace('\nCatergory: ','') for d in display_dict ]))

      

        filterList.insert(0,'All')


    # Sub-Category is unselected: All remain unchange, 'All' is selected by default 
    else:

        display_dict = dict

        filterList = list(set([d['sub_category'].replace('\nSub-Catergory: ','').replace('\nSub-Category: ','') for d in display_dict ]))

        filterList.insert(0,'All')



    
    return display_dict,filterList







# convert to html like
def to_html(cat_filter,sub_filter):

    global full_dict
    
    full_dict = txt_json()
    display_dict,category_list = filter_list(cat_filter,full_dict,"cat")
    display_dict,sub_cat_filter = filter_list(sub_filter,display_dict,"sub")



    

    post_html = ""

    for item in display_dict:
        

        
        title =        f"<div class='sticky-title'>   {item['title'].replace('Title: ','')}    </div>"
        category =     f"<div class='sticky-cat'>     {item['category']}     </div>"
        sub_category = f"<div class='sticky-subcat'>  {item['sub_category']}      </div>"
        content =      f" {item['content']}    " 
            
        

        new_content = "<br>\n  "

        for line in content.splitlines():
            
            if "->" in line:
                
                new_line = "\n <dd>" + line + "</dd> " 
            
            else:
                new_line = "<br> " + line


            new_content += new_line

        
        this_html_item = "\n\n <div class='sticky'>" + title + category + sub_category + new_content + "<br><br><br> </div>"


        post_html += this_html_item    
    
    
    
    return post_html,category_list,sub_cat_filter





# insert new record to .txt file
def write_txt(new_record,title,Catergory,Sub_Category):

    
    title = "\n\n" + "Title: " + title
    Catergory = "\n" + "Catergory: " + Catergory 
    Sub_Category = "\n" + "Sub-Category: " + Sub_Category 


    append_record = title + Catergory + Sub_Category + "\n\n"

    for line in new_record.splitlines():

        new_line = line.strip() + "\n"

        if "->" in new_line:
            new_line = "\t" + new_line
        
        append_record += new_line

   
    
    with open(my_txt_path, "a") as file:
        
        file.write(append_record)






@app.route('/', methods = ['GET','POST'])
def index():


    cat_filter = "All"
    sub_cat_filter = "All"
    

    if request.method == "POST":
        
        # Insert new item into .txt file
        new_record = request.form['text']
        title = request.form['title']
        Catergory = request.form['Catergory']
        Sub_Category = request.form['Sub-Category']
             
        if Sub_Category == "":
            Sub_Category = Catergory

        
        if new_record != "":
            write_txt(new_record,title,Catergory,Sub_Category)       

        
        
        # Get Filter        
        cat_filter = request.form['cat']
        sub_cat_filter = request.form['subcat']
      


        
    to_Html,category_list,sub_cat_filter = to_html(cat_filter,sub_cat_filter)


    return render_template('index.html', notelist = to_Html , cate_list = category_list , sub_cate_list = sub_cat_filter )








if __name__ == '__main__':
    app.run()

