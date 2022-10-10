import os
import streamlit as st
import numpy as np
from PIL import  Image
from lib import commons
import torch
from fpdf import FPDF
from torchvision import datasets, models, transforms
import datetime
import mysql.connector
from base64 import b64encode

#added later for pdf issue
from pathlib import Path

# Custom imports 
#from multipage import MultiPage

#from pages import poxAnalysis

st.set_page_config(page_title="MonkeyPox", page_icon="🧑🏽‍⚕️", layout="centered", initial_sidebar_state="collapsed", menu_items=None)

# Title of the main page
display = Image.open('cover.jpg')
display = np.array(display)
st.image(display)

#"st.session_state object:", st.session_state

#st.write(st.experimental_get_query_params())

loginCount = None

#patient = False
pdf_generated=None

@st.cache
def first_time():
    doc_id=st.session_state['luname']
    return doc_id


if st.experimental_get_query_params() :
    st.write()
#    st.write("Not Empty query")
#    st.write(st.experimental_get_query_params())

else:
    
#    st.write("Empty query")
    st.experimental_set_query_params(
        cnt = 1,
        firsttimecnt2=0
        )
#    st.write(st.experimental_get_query_params())

if st.experimental_get_query_params().get('cnt')[0] == '1' :
    if 'login' not in st.session_state:
        st.session_state['login'] = False
#        st.write('login in session set to false by cnt')
#        st.write(st.session_state)

if (st.experimental_get_query_params().get('firsttimecnt2')[0] == '0'):
    if 'login' not in st.session_state:
        st.session_state['login'] = False
#        st.write('login in session set to false by firsttimecnt2=0')
        dname1=st.experimental_get_query_params().get('dname')[0]
        st.experimental_set_query_params(
            logindone=True,
            cnt=1,
            firsttimecnt2=0,patient=None,dname=dname1,
            setup=None
            )
#        st.write(st.experimental_get_query_params())
#        st.write(st.session_state)

if (st.experimental_get_query_params().get('firsttimecnt2')[0] == '1' and st.experimental_get_query_params().get('cnt')[0] == '2'):
    if 'login' not in st.session_state:
        st.session_state['login'] = False
#        st.write('login in session set to false by firsttimecnt2=1')
        dname1=st.experimental_get_query_params().get('dname')[0]
        st.experimental_set_query_params(
            logindone=True,
            cnt=2,
            firsttimecnt2=1,patient=None,dname=dname1,
            setup=True
            )
#        st.write(st.experimental_get_query_params())
#        st.write(st.session_state)

#def loginCountVar():
#loginCount = 0
#Note for tomorrow
##add counter vsrible for refresh in condition below
#((st.experimental_get_query_params().get('logindone')[0]) == 'True') and (st.session_state['login'] == False) :

if (st.experimental_get_query_params().get('logindone') == None) and (st.session_state['login'] == False) :
#    st.write("1")
#    st.write("[You need to login First to access this data](main)")
    st.info("[You need to login First to access this data](main)")
#    st.experimental_set_query_params(logindone=False)
elif ((st.experimental_get_query_params().get('logindone')[0]) == 'False') and (st.session_state['login'] == False) :
#    st.write("2")
    st.experimental_set_query_params(logindone=False,cnt=1,firsttimecnt2=0,patient=None,setup=None)
#    st.write("[You need to login First to access this data](main)")
    st.info("[You need to login First to access this data](main)")
elif ((st.experimental_get_query_params().get('logindone')[0]) == 'True' and (st.experimental_get_query_params().get('cnt')[0]) == '1'):
#    st.write("3")
    if (st.session_state['login'] == True) and st.experimental_get_query_params().get('firsttimecnt2')[0] == '0'  :
#        st.write("4")
        d=first_time()
#        doc_id=st.session_state['luname']
#        st.write(doc_id)
        loginCount = 1
        dname1=st.experimental_get_query_params().get('dname')[0]
        st.experimental_set_query_params(
            logindone=True,
            cnt=1,patient=None,
            firsttimecnt2=0,setup=None,dname=dname1
            )
#        st.write(st.experimental_get_query_params())
    else :
#        st.write("5")
        if (loginCount == 0 or loginCount == None):
#            st.write("[You need to login First to access this data](main)")
            st.info("[You need to login First to access this data](main)")
elif ((st.experimental_get_query_params().get('logindone')[0]) == 'True' and (st.experimental_get_query_params().get('cnt')[0]) == '2'):
#    st.write("6")
    if st.experimental_get_query_params().get('firsttimecnt2')[0] == '0':
#        st.write('1st time access before logging in directly by url')
#        st.write("[You need to login First to access this data](main)")
        st.info("[You need to login First to access this data](main)")
        st.info("1st time access before logging in directly by url")
    elif st.experimental_get_query_params().get('firsttimecnt2')[0] == '1' :# and st.experimental_get_query_params().get('setup')[0] == 'True' :
        loginCount = 1
#        st.write('setting logincount= 1 value in this part ==> elif st.experimental_get_query_params().get(\'firsttimecnt2\')[0] == \'1\'')
#        st.write(st.experimental_get_query_params())
    else:
#        st.write("[You need to login First to access this data](main)")
        st.info("[You need to login First to access this data](main)")
#        st.write("here")
        
        
#    if 'login' not in st.session_state :
#        st.write()
 #   if st.session_state['login'] == True or st.session_state['login'] == False :
    if st.session_state['login'] == True and ((st.experimental_get_query_params().get('firsttimecnt2')[0] == '1') or (st.experimental_get_query_params().get('firsttimecnt2')[0] == '1')) : #removed this st.session_state['login'] == True
        loginCount = 1
#    if st.session_state :
#         loginCount = 1
#        st.write("7")
#         st.write("Hi")
#         st.write("8")
#         st.write('inside else')
#         loginCount = 1      
#            st.write("[You need to login First to access this data](main)")
    else :
#        st.write('8')
        if st.session_state['login'] == False :#and st.experimental_get_query_params().get('setup')[0] == 'True' :#st.experimental_get_query_params().get('firsttimecnt2')[0] == '1' :
            loginCount = 1
#            st.write('9')
        else:
            st.info("[You need to login First to access this data](main)")
            
        
#        if st.session_state['login'] == False and st.experimental_get_query_params().get('firsttimecnt2')[0] == '0' :
#            st.write("10")
#            loginCount = 1
#            st.write("[You need to login First to access this data](main)")
else :
#    st.write("11")
    loginCount = 1

#if ((st.experimental_get_query_params().get('logindone')[0]) == 'True' and (st.experimental_get_query_params().get('cnt')[0]) == '2'):

#else:
#if st.session_state['login'] == False :
#    st.write("[You need to login First to access this data](main)")
#else :


def upload_patient_detail():
    # Connect to server
    cnx = mysql.connector.connect(
        host="sql6.freemysqlhosting.net",
        port=3306,
        user="sql6525472",
        password="5YE8LUlZdI",
        database="sql6525472")
#        host="localhost",
#        port=3306,
#        user="root",
#        password="Asdf@1234",
#        database="Medhini")
        # Get a cursor
    cur = cnx.cursor()
    doc_id=first_time()
#    st.write(doc_id)
    P_name=st.session_state['pname']
    P_contact=st.session_state['pphno']
    P_sex=st.session_state['psex']
    P_age=st.session_state['page']
    P_image=st.session_state['image']
    if len(P_age) == 1:
        P_id = P_name[:3]+P_age[:1]+P_sex+P_contact[5:]
    else:
        P_id = P_name[:3]+P_age[:1]+P_sex+P_age[1:]+P_contact[6:]
    s_sql="Insert into patient_data (doc_id,patient_name,patient_id,patient_contact,patient_sex,patient_age,patient_image) values (%s, %s, %s, %s, %s, %s, %s)"
    s_val=(doc_id,P_name,P_id,P_contact,P_sex,P_age,P_image)
    cur.execute(s_sql,s_val)
    cnx.commit()
#    st.write("1 record inserted : ", cur.lastrowid)
#   st.success("Signup Successful")
#   Close Connection
    cnx.close()

def patient_name_validation():
    if st.session_state['pname'] == '':
        st.error('Patient name can\'t be blank.',icon="🚨")
    elif str(st.session_state['pname']).isdigit():
        st.error('Please dont enter numbers in name field',icon="🚨")
    else:
#        st.success("Name seems fine",icon="✅")
        return True

def patient_sex_validation():
    if st.session_state['psex'] == '':
        st.error('Please enter sex of patient',icon="🚨")
    elif str(st.session_state['psex']).isdigit():
        st.error('Please dont enter numbers in sex field',icon="🚨")
    elif st.session_state['psex'] in ['M','F','O'] :
#        st.success("SEX seems fine",icon="✅")
        return True
    else :
        st.error('Only M F & O is allowed',icon="🚨")


def patient_age_validation():
    if st.session_state['page'] == '':
        st.error('Age field can\'t be left blank',icon="🚨")    
    elif str(st.session_state['page']).isdigit():
#        st.success("Age",icon="✅")
        return True
    else :
        st.error("Please enter numbers in Age field",icon="🚨")


def patient_contact_validation():
    if st.session_state['pphno'] == '':
                st.error('Contact Number can\'t be blank. Please enter Patient\'s contact number',icon="🚨")
    elif str(st.session_state['pphno']).isdigit():
#       st.write("Entered value is Number")
        length = len(str(st.session_state['pphno']))
        if length == 10:
            phno = str(st.session_state['pphno'])
            firstDigit = phno[0]
            if ( firstDigit in ['9','8','7','6']):
#                st.success("Contact No",icon="✅")
                return True
            else:
                st.error(f"Valid Contact number cannot starts with {firstDigit}")
        else :
            st.error("Contact no cannot be less than 10 digit",icon="🚨")
    else :
        st.error("Please enter numbers in Contact number",icon="🚨")


def patient_data_validation():
    p_name_valid = patient_name_validation()
    p_sex_valid = patient_sex_validation()
    p_age_valid = patient_age_validation()
    p_contact_valid=patient_contact_validation()

    if p_name_valid and p_sex_valid and p_age_valid and p_contact_valid :
        return True
    else :
        st.error("Patient data is incorrect",icon="🚨")


def get_patient_data():
    with st.form("PatientForm",clear_on_submit=False):
                P_name=st.text_input("Patient name",type="default",max_chars=30,value="",key="pname",placeholder="Enter Patient Name")
                P_sex=st.text_input("Sex",type="default",max_chars=1,value="",key="psex",placeholder="M/F/O")
                P_age=st.text_input("Age",type="default",max_chars=2,value="",key="page",placeholder="Enter Patient Age")
                P_contact=st.text_input("Patient Contact No",type="default",max_chars=10,value="",key="pphno",placeholder="Enter Patient Contact No")
#                email=st.text_input("Email",type="default",max_chars=30,value="",key="semail",placeholder="Enter your mail id")
                P_submit=st.form_submit_button("Submit")
                if P_submit:
#                    st.write("Data submitted successfully")
                    p_valid = patient_data_validation()
                    if p_valid :
#                        doc=first_time()
#                        st.write(f"Doctor id is:- {doc}")
                        if len(P_age) == 1:
                            P_id = P_name[:3]+P_age[:1]+P_sex+P_contact[5:]
                        else:
                            P_id = P_name[:3]+P_age[:1]+P_sex+P_age[1:]+P_contact[6:]
#                        st.success("Patient data validated successfully")
#                        st.write("Patient data validated successfully")
                        current_logindone_value = st.experimental_get_query_params().get('logindone')[0]
                        current_cnt_value = st.experimental_get_query_params().get('cnt')[0]
                        current_firsttimecnt2_value = st.experimental_get_query_params().get('firsttimecnt2')[0]
                        current_patient_value = st.experimental_get_query_params().get('patient')[0]
                        dname1=st.experimental_get_query_params().get('dname')[0]
    #                    current_setup_value = st.experimental_get_query_params().get('setup')[0]
#                        st.write('extracted url values')
                        st.experimental_set_query_params(
                            logindone=current_logindone_value,
                            cnt=current_cnt_value,
                            patient=True,
                            firsttimecnt2=current_firsttimecnt2_value,
                            dname=dname1
                            #,setup=None
                            )


#           start of pdf generation
def generate_pdf():
    class PDF(FPDF):
        def header(self):
            #logo
            self.image('Medhini_logo.jpeg', 0, 0, 80, 40,link = 'https://www.arficus.com')
            # font
            self.set_font('helvetica', 'BU', 20)
            # Line break
            self.ln(30)
            #padding
        #   self.cell(80)
        #   Title
            self.cell(0, 10, 'Monkey Pox Diagnosing', ln=1, align='C')
        # Line break
            self.ln(10)
                            

# page footer
        def footer(self):
            # Set position of the footer
            self.set_y(-35)
            #Set font
            self.set_font('helvetica', 'I', 10)
            #Footer Line
            self.cell(0,10,"This is a system generated report. If you want to visit our website click on our Logo in the Header or Medhini Below",ln=1)
            self.ln(2)
            #Set font
            self.set_font('helvetica', 'B',15)
            #Footer Line
            self.cell(0,10,"Medhini",border=False,ln=1,link = 'https://www.arficus.com')
            #Footer Line
            self.cell(40,8,"Raho Chirayu",border=False,link = 'https://www.arficus.com')
            #Footer Line
            self.cell(140)
            #Set font
            self.set_font('helvetica', 'I',10)
            #Page number
            self.cell(25,10,f'Page {self.page_no()}/{{nb}}')

    time = str(datetime.datetime.now())
    time_now = time[:19]
    pdf=PDF('P', 'mm', 'Letter')
    #For footer class to get totalpage numbers
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('helvetica', '', 16)
    doc_name=st.experimental_get_query_params().get('dname')[0]
    pdf.cell(0,10,f'Doctor\'s Name :- {doc_name}',ln=True)
    pdf.cell(0,10,'Hospital Name :- {hospital_name}',ln=True)
    P_name1 = st.session_state['pname']
    P_age1 = st.session_state['page']
    P_sex1 = st.session_state['psex']
    pdf.cell(0,10,f'Name of Patient :- {P_name1}', ln=True)
    pdf.cell(0,10,f'Age of Patient :- {P_age1}', ln=True)
    pdf.cell(0,10,f'Sex :- {P_sex1}', ln=True)
    pdf.cell(10,10,' ', ln=True)
    pdf.cell(0,10,f'Time of test :- {time_now}', ln=True)
    pdf.cell(0,10,f'Input data :- {image_file.name}', ln=True)
    pdf.cell(0,10,f'Result of Diagnosing :- {predictions[0]}',ln=True)
    pdf.ln(2)
    folder_name=first_time()
    ab_path=os.path.dirname(__file__)
    exact_path=os.path.join(ab_path)
    pdf.image(f"{exact_path}/{image_file.name}", 50, 157, 120, 80)
#    st.write(folder_name)
#    absolute_path = os.path.dirname(__file__)
#for relative path
#    image_path = Path(__file__)
#    st.write(image_path)
#    relative_path = "src/lib"
#    full_path = os.path.join(absolute_path, relative_path)
#    pdf.image(f'{folder_name}_upload/{image_file.name}', 50, 157, 120, 80)
     
#    pdf.output(os.path.join(os.path.dirname(__file__)+f"/{P_name1}.pdf")
#    pdf.output(os.path.join(os.path.dirname(__file__)+"/"+'f{P_name1}.pdf',dest='I')
#    pdf.output(f'{P_name1}.pdf')
#    st.write("successfully generated PDF")
    return True
                
#   end of PDF generation 


#           start of pdf generation for browser
def generate_pdfB():
    class PDF(FPDF):
        def header(self):
            #logo
            self.image('Medhini_logo.jpeg', 0, 0, 80, 40,link = 'https://www.arficus.com')
            # font
            self.set_font('helvetica', 'BU', 20)
            # Line break
            self.ln(30)
            #padding
        #   self.cell(80)
        #   Title
            self.cell(0, 10, 'Monkey Pox Diagnosing', ln=1, align='C')
        # Line break
            self.ln(10)
                            

# page footer
        def footer(self):
            # Set position of the footer
            self.set_y(-35)
            #Set font
            self.set_font('helvetica', 'I', 10)
            #Footer Line
            self.cell(0,10,"This is a system generated report. If you want to visit our website click on our Logo in the Header or Medhini Below",ln=1)
            self.ln(2)
            #Set font
            self.set_font('helvetica', 'B',15)
            #Footer Line
            self.cell(0,10,"Medhini",border=False,ln=1,link = 'https://www.arficus.com')
            #Footer Line
            self.cell(40,8,"Raho Chirayu",border=False,link = 'https://www.arficus.com')
            #Footer Line
            self.cell(140)
            #Set font
            self.set_font('helvetica', 'I',10)
            #Page number
            self.cell(25,10,f'Page {self.page_no()}/{{nb}}')

    time = str(datetime.datetime.now())
    time_now = time[:19]
    pdf=PDF('P', 'mm', 'Letter')
    #For footer class to get totalpage numbers
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('helvetica', '', 16)
    doc_name=st.experimental_get_query_params().get('dname')[0]
    pdf.cell(0,10,f'Doctor\'s Name :- {doc_name}',ln=True)
    pdf.cell(0,10,'Hospital Name :- {hospital_name}',ln=True)
    P_name1 = st.session_state['pname']
    P_age1 = st.session_state['page']
    P_sex1 = st.session_state['psex']
    pdf.cell(0,10,f'Name of Patient :- {P_name1}', ln=True)
    pdf.cell(0,10,f'Age of Patient :- {P_age1}', ln=True)
    pdf.cell(0,10,f'Sex :- {P_sex1}', ln=True)
    pdf.cell(10,10,' ', ln=True)
    pdf.cell(0,10,f'Time of test :- {time_now}', ln=True)
    pdf.cell(0,10,f'Input data :- {image_file.name}', ln=True)
    pdf.cell(0,10,f'Result of Diagnosing :- {predictions[0]}',ln=True)
    pdf.ln(2)
    folder_name=first_time()
    ab_path=os.path.dirname(__file__)
    exact_path=os.path.join(ab_path)
    pdf.image(f"{exact_path}/{image_file.name}", 50, 157, 120, 80)
    return bytes(pdf.output())
#    st.write(folder_name)
#    absolute_path = os.path.dirname(__file__)
#for relative path
#    image_path = Path(__file__)
#    st.write(image_path)
#    relative_path = "src/lib"
#    full_path = os.path.join(absolute_path, relative_path)
#    pdf.image(os.path.join(os.path.dirname(__file__)+f"/{image_file.name}", 50, 157, 120, 80)
#    pdf.image(f'{folder_name}_upload/{image_file.name}', 50, 157, 120, 80)

                
#   end of PDF generation for browser

                        

#st.write(f'outside if {loginCount}')
if loginCount == 1 :
    if st.experimental_get_query_params().get('cnt')[0] == '1' :
#        st.write(f'Inside If {loginCount}')
        dname1=st.experimental_get_query_params().get('dname')[0]
        # Set query params
        st.experimental_set_query_params(
            logindone = True,
            cnt = 2,
            firsttimecnt2=1,patient=None,
            setup=None,dname=dname1
            )
    ###end of setting query params
    # monkeypox down part#
    st.title("Skin Image based Pox Analysis")
    st.text("Pox Affected Or Not: To detect chances of MonkeyPox, Measles and ChickenPox")

    # col1 = st.columns(1)
    # col1, col2 = st.columns(2)
    # col1.image(display, width = 400)
    # col2.title("Data Storyteller Application")

    # Add all your application here
    #monkeypox down part end
    
    #poxAnalysis.py code
#    def app():     ankit
    header=st.container()
    result_all = st.container()
    model=commons.load_model()
    with header:
        st.subheader("Test whether an area is affected by pox")
        st.info("Please fill the below form to start diagnosing",icon="ℹ️")
#        st.write(f"Doctor id is:- {doc_id}")
        get_patient_data()
        if (st.experimental_get_query_params().get('patient')[0]) == 'True':
            image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg","jfif"])
            if image_file is not None:
                folder_name1=first_time()
#                st.write(folder_name1)
                #save uploaded image file in new folder name "uploaded_case"
                st.write(os.path.dirname(__file__))
                with open(os.path.join(os.path.dirname(__file__)+"/",image_file.name), "wb") as f:
                    f.write(image_file.getbuffer())
#                st.success("File saved")
#                st.write(image_file.name)
                #create binary data of uploaded image
                with open(os.path.join(os.path.dirname(__file__)+"/",image_file.name), 'rb') as file:
                    P_image = file.read()
#                st.session_state['image'] = image_file
                st.session_state['image'] = P_image
                # To See details
                file_details = {"filename":image_file.name, "filetype":image_file.type,
                              "filesize":image_file.size}
                # st.write(file_details)

                # To View Uploaded Image
                st.image(commons.load_image(image_file)
                    ,width=250
                    )
                print("Image file is it showing location?",image_file)            
                predictions=commons.predict(model,image_file)
                print("Loaded image for model")
                pdf_generated=generate_pdf()
                P_name2 = st.session_state['pname']
                # Embed PDF to display it:
#                base64_pdf = b64encode(generate_pdfB()).decode("utf-8")
#                pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
#                st.markdown(pdf_display, unsafe_allow_html=True)
                #download Button to download output
                st.download_button(label="Download PDF",
                                   data=generate_pdfB(),
                                   file_name=f"{P_name2}.pdf",
                                   mime="application/pdf",
                                   )
                #####

                #connect to db to save patient details
#                st.write(pdf_generated)

            else:
                proxy_img_file="data/chicken00.jpg"
                st.image(commons.load_image(proxy_img_file),width=250)        
                predictions=commons.predict(model,proxy_img_file)
                print("Loaded proxy image for model")
    
#        else :
#            st.warning("You need to fill Patient detail first to get the diagnosing",icon="🚨")


    with result_all:
        if (st.experimental_get_query_params().get('patient')[0]) == 'True' :
            i=1
            st.subheader("Pox types arranged in order of probability (highest first):")
            for pred in predictions:
                st.text(str(i)+". "+pred)
                i+=1
            st.info(f"Result of Diagnosing :- {predictions[0]}")
#            st.write(pdf_generated)
            if pdf_generated == True :
                #Upload patient detail in database
                upload_patient_detail()
                #now connet it to database                
                current_logindone_value = st.experimental_get_query_params().get('logindone')[0]
                current_cnt_value = st.experimental_get_query_params().get('cnt')[0]
                current_firsttimecnt2_value = st.experimental_get_query_params().get('firsttimecnt2')[0]
                current_patient_value = st.experimental_get_query_params().get('patient')[0]
    #               current_setup_value = st.experimental_get_query_params().get('setup')[0]
#                st.write('now setting patient value to false')
                dname1=st.experimental_get_query_params().get('dname')[0]
                st.experimental_set_query_params(
                    logindone=current_logindone_value,
                    cnt=current_cnt_value,
                    patient=None,
                    firsttimecnt2=current_firsttimecnt2_value,dname=dname1
                    #,setup=None
                    )


    

    ##poxanalysis.py code end

    # Create an instance of the app 
#    app = MultiPage()   ankit

    # removed part and copied after else    ankit
    
#    app.add_page("Pox Analysis", poxAnalysis.app)   ankit
    # app.add_page("Detect Disaster Type", detectDisaster.app)

#monkeyPox?logindone=True&cnt=2

    # The main app
#    app.run()    ankit
    #button to logout from current user
    def false_session():
#        st.write("on clicking")
        st.session_state['login'] = False
        st.experimental_set_query_params(
            logindone=False,
            cnt=1,
            firsttimecnt2=0,
            patient=None#,setup=None
            )
        global loginCount
        loginCount=0
#        st.write(st.experimental_get_query_params())

    st.button("Logout",on_click=false_session)
