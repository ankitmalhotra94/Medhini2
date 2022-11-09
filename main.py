import streamlit as st
from PIL import  Image
import numpy as np
import mysql.connector
import os

st.set_page_config(page_title="Login", page_icon=":health:", layout="centered", initial_sidebar_state="collapsed", menu_items=None)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


if 'login' not in st.session_state:
        st.session_state['login'] = False
        st.session_state['sphno'] = ''
        st.session_state['spswd'] = ''
        st.session_state['scpswd'] = ''
        st.session_state['pswd_entered'] = 0
        st.session_state['cpswd_entered'] = 0
        

display = Image.open('cover.jpg')
display = np.array(display)
st.image(display)


def get_data():
            login_user=st.session_state['luname']
            login_pswd=st.session_state['lpswd']
            # Connect to server
            cnx = mysql.connector.connect(
                    host="sql280.main-hosting.eu",
                    port=3306,
                    user="u553007133_xpbfq",
                    password="yR1/#1hV0AP",
                    database="u553007133_xlvy9")            
            # Get a cursor
            cur = cnx.cursor()
            # Execute a query
            l_sql="SELECT userid, pass, username FROM signup where userid=%s"
            l_val = (login_user,)
            cur.execute(l_sql,l_val)
            # Fetch one result
            rs = cur.fetchone()
            if cur.rowcount > 0:
        #        st.write(f"No of rows for {login_user} is :- ", cur.rowcount)
        #        st.write(rs[1])
                if rs[1] == login_pswd :
                    st.success(f"{login_user} Successfully Logged in ",icon="✅")
                    st.session_state['login'] = True
#                    st.write(os.path.dirname(__file__))
                    st.experimental_set_query_params(
                            logindone = True,
                            cnt=1,
                            firsttimecnt2=0,
                            patient=None,
                            setup=None,
                            dname=rs[2]
                            )
                
                else :
                    st.error("In-correct Password ",icon="🚨")

        #        for row in rs:
        #            st.write("user name :- ", rs[0])
        #            st.write("pswd name :- ", rs[1])
                # Close connection
                cnx.close()
            else :
                st.error(f"User name {login_user} doesnot exist",icon="🚨")
                st.info("Please Signup first by clicking on Sign-Up tab")

        

###### Signing up a user ####

def do_signup():
        suid = st.session_state['suname']
        sname = st.session_state['sfname']+' '+st.session_state['smname']+' '+st.session_state['slname']
        scontact=st.session_state['sphno']
        semail=st.session_state['semail']
        spass=st.session_state['spswd']
        # Connect to server
        cnx = mysql.connector.connect(
                host="sql280.main-hosting.eu",
                port=3306,
                user="u553007133_xpbfq",
                password="yR1/#1hV0AP",
                database="u553007133_xlvy9") 
#        host="localhost",
#        port=3306,
#       user="root",
#        password="Asdf@1234",
#       database="Medhini")
        # Get a cursor
        cur = cnx.cursor()
        s_sql="Insert into signup value(%s, %s, %s, %s, %s)"
        s_val=(suid,sname,scontact,semail,spass)
        cur.execute(s_sql,s_val)
        cnx.commit()
        # Close Connection
        cnx.close()
        return True


### End of Signing up ####


#Signup name validation
def validate_names():
        st.write(fname)
        st.write(mname)
        st.write(lname)

#Signup Contact validation
def validate_contact():
        if st.session_state['sphno'] == '':
                st.error('Contact Number can\'t be blank. Please enter your contact number',icon="🚨")
        elif str(st.session_state['sphno']).isdigit():
                length = len(str(st.session_state['sphno']))
                if length == 10:
                        phno = str(st.session_state['sphno'])
                        firstDigit = phno[0]
                        if ( firstDigit in ['9','8','7','6']):
                            st.success("Contact No",icon="✅")
                            return True
                        else:
                                st.error(f"Valid Contact number cannot starts with {firstDigit}")
                else :
                        st.error("Contact no cannot be less than 10 digit",icon="⚠️")
        else :
                st.error("Please enter numbers in Contact number",icon="⚠️")

def validate_cpassword():
        if (st.session_state['scpswd'] == '') and (st.session_state['cpswd_entered'] == 0) :
                st.warning("Cant leave confirm password field as empty",icon="ℹ️")
        else:
                if (st.session_state['spswd'] == '' and st.session_state['scpswd'] != '') :
                        st.info('Please enter password in Password field',icon="ℹ️")
                        st.session_state['cpswd_entered'] = 1
                else :
                        if (st.session_state['spswd'] == '' and st.session_state['scpswd'] == '') :
                                if(st.session_state['pswd_entered'] and st.session_state['cpswd_entered']) :
                                        st.warning("Cant leave password field as empty",icon="ℹ️")
                                        st.warning("Cant leave confirm password field as empty",icon="ℹ️")
                                else :
                                        st.warning("Cant leave confirm password field as empty",icon="ℹ️")
                        elif st.session_state['spswd'] == st.session_state['scpswd'] :
                                st.session_state['cpswd_entered'] = 1
                                st.success("Both password are same",icon="✅")
                                return True
                        elif (st.session_state['spswd'] != '' and st.session_state['scpswd'] == '') :
                                st.info('Please enter password in Confirm Password field',icon="ℹ️")
                                st.session_state['cpswd_entered'] = 1
                        else:
                                st.error("Password and Confirm Password is not same",icon="⚠️")
                
def validate_password():
        if (st.session_state['spswd'] != '' and st.session_state['pswd_entered'] == 0) :
                st.session_state['pswd_entered'] = 1
        elif (st.session_state['spswd'] == '' and st.session_state['pswd_entered'] == 0) :
                st.warning("Cant leave password field as empty",icon="ℹ️")
        else :
                st.write()

def validate_email():
        if st.session_state['semail'] == '':
                st.warning('Email field can\'t be left blank. Please enter a valid email id')
        else:
                varcount=st.session_state['semail'].count('@')
                if varcount == 1 :
                        indexOfAtTheRate = st.session_state['semail'].index('@')
                        indexAfterAtTheRate = indexOfAtTheRate + 1
                        restEmail=st.session_state['semail'][indexAfterAtTheRate:]
                        if restEmail.count('.com') == 0:
                                st.error('Email should contains .com in it',icon="🚨")
                        elif restEmail.count('.com') == 1:
                                valOfDotCom = st.session_state['semail'].index('.com')
                                valBtwAtTheRateDotCom = restEmail.index('.com')
                                mailProvider = st.session_state['semail'][indexAfterAtTheRate:valOfDotCom]
                                if (mailProvider == ''):
                                        st.error('There can be space in between @ and .com',icon="🚨")
                                elif (mailProvider in ['gmail','yahoo','outlook']):
                                        st.success('success email id validation',icon="✅")
                                        return True
                                else :
                                        st.error(f'{mailProvider}.com is not a valid mail service',icon="🚨")
                                
                        else:
                                st.error('Email should not contain .com more than once',icon="🚨")
                else :
                        st.error(f'email can\'t contain\'s {varcount} @',icon="🚨")
        


def validate_signup():
#        v_names=validate_names()
        v_contact=validate_contact()
        v_email=validate_email()
        v_pass=validate_password()
        v_cpass=validate_cpassword()
        if (v_contact and v_email and v_cpass):
                signedUp = do_signup()
                if signedUp == True :
                        st.success('Sign Up successful. Please login',icon="✅")
#                        directory=st.session_state['suname']
#                        parent_dir = "https://github.com/ankitmalhotra94/Medhinihttps://github.com/ankitmalhotra94/Medhini"
#                        path = os.path.join(parent_dir, directory)
#                        os.mkdir(path)
#                        directory=st.session_state['suname']+"_upload"
#                        path = os.path.join(parent_dir, directory)
#                        os.mkdir(path)
#                        st.success('Sign Up successful. Please login',icon="✅")
#                        directory=st.session_state['suname']
#                        parent_dir = "/Users/ankitmalhotra/opt/anaconda3/envs/snowflakes/StreamlitProject/PoxDetectionMyVersionDemo"
#                        path = os.path.join(parent_dir, directory)
#                        os.mkdir(path)
#                        directory=st.session_state['suname']+"_upload"
#                        path = os.path.join(parent_dir, directory)
#                        os.mkdir(path)
        else :
                st.write()

tab1 = st.tabs(["Login"])
#tab1, tab2 = st.tabs(["Login","Sign Up"])

with tab1:
        with st.form("LoginForm",clear_on_submit=True):
                user=st.text_input("User Name",type="default",max_chars=10,value="",key="luname",placeholder="Enter your user name")
                password=st.text_input("Password",type="password",placeholder="Password",key="lpswd",value="")
                login_submit=st.form_submit_button("Submit")
        if login_submit:
                get_data()

#with tab2:
#        with st.form("SignInForm",clear_on_submit=False):
#                fname=st.text_input("First Name",type="default",max_chars=15,value="",key="sfname",placeholder="Enter First name")
#                mname=st.text_input("Middle Name",type="default",max_chars=15,value="",key="smname",placeholder="Enter Middle name")
##                lname=st.text_input("Last Name",type="default",max_chars=15,value="",key="slname",placeholder="Enter Last name")
 #               username=st.text_input("UserId",type="default",max_chars=10,value="",key="suname",placeholder="Create user id of your choice")
 #               contact=st.text_input("Contact No",type="default",max_chars=10,value="",key="sphno",placeholder="Enter Contact Number")
 #               email=st.text_input("Email",type="default",max_chars=30,value="",key="semail",placeholder="Enter your mail id")
 #               spswd=st.text_input("Password",type="password",max_chars=20,placeholder="Password",key="spswd",value="")
 #               scpswd=st.text_input("Confirm Password",type="password",max_chars=20,placeholder="Confirm Password",key="scpswd",value="")
 #               Signup_submit=st.form_submit_button("Submit")
 #       if Signup_submit:
 #               validate_signup()
