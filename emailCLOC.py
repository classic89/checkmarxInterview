import unittest, re, getpass, smtplib, ssl, os, subprocess, sys, pip, base64, git 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from secrets import myDefaultPassword

class emailCLOC:
    def __init__(self, myEmail, myPassword, yourEmail, repoURL, repoName, branch, outputFile, clocfile):
        self.myEmail= myEmail
        self.myPassword = myPassword
        self.yourEmail = yourEmail
        self.repoUrl = repoURL
        self.repoName = repoName
        self.branch = branch
        self.outputFile = outputFile
        self.clocfile = clocfile

    def gitinit(self):
        name = self.repoName
        currentDirectory = "./"
        if not os.path.exists(currentDirectory+name):
            print ('Cloning ' + name + '...')
            git.Git(currentDirectory).clone(self.repoUrl)
        gitrepo = git.Repo(name)
        gcmd = git.cmd.Git(name)
        gcmd.pull()
        print ('Checking out'+ name + '...')
        gitrepo.git.checkout("-f", self.branch)

        print ('Running CLOC report for ' + name + '...')
        proc = subprocess.Popen([currentDirectory+self.clocfile,currentDirectory+name, "--csv","--out", self.outputFile , "--quiet"], stdout=subprocess.PIPE)
        proc.stdout.read()

    def sendEmail(self):
        msg = MIMEMultipart()
        msg['Subject'] = 'The CLOC Report of the %s epository' % self.repoName
        msg['From'] = self.myEmail
        msg['To'] = self.yourEmail
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(self.outputFile, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="'+ self.outputFile +'"')
        msg.preamble = 'Here is the report you wanted'
        msg.attach(part)
        context = ssl.create_default_context()
        print("Emailing...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(self.myEmail, self.myPassword)
            server.sendmail(self.myEmail, self.yourEmail, msg.as_string())

    def validateInput(self):
        validateEmail(self.myEmail)
        print("From : "+self.myEmail)
        validateEmail(self.yourEmail)
        print("To : "+self.yourEmail)
        validateURL(self.repoUrl)
        print("Repository : "+self.repoUrl)
        print("Branch : "+self.branch)
        print("Attachment : "+self.outputFile)

#helper methods
# class helperMethods: 
#     def __init__():
#         self.getRepository()
#         self.validateEmail()
#         self.

def getRepository(repoUrl):
        return(repoUrl[repoUrl.rfind('/')+1:repoUrl.rfind('.')])

def validateEmail(email):
    errorMessage = email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errorMessage = errorMessage+"Email format is invalid\n"

def validateURL(url):
    errorMessage = url
    if not re.match(r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(\/)?", url) and (not len(url)==0):
        errorMessage = errorMessage +"Git repository is invalid.\n"

def setup():
    speed = [
        "retrorock8821@gmail.com", 
        myDefaultPassword.decode(), 
        "mw103110@gmail.com",
        "https://github.com/classic89/Forbidden-Island.git", 
        "master"
    ]
    print("Press enter at prompt for speed or enter in your own")
    # me, pw, yo, ru, br = ().split()
    me = input("Type your email: ")
    pw = getpass.getpass(prompt='Type your password: ', stream=sys.stderr)
    # print("Type your password: ", pw)
    yo = input("Type the email for report: ")
    ru = input("Git URL: ")
    br = input("Git branch: ")
    count = 0
    t = [me, pw, yo, ru, br]
    for x in t:
        if len(x)==0:
            t[count] = speed[count]
        count += 1
    repoName = getRepository(t[3])
    logtime = datetime.now().strftime("%Y%m%d%H%M%S")
    clocfile = "cloc-1.64.exe"
    outputFile = "CLOC_"+repoName+"_"+t[4]+"_"+logtime+".csv"

    return emailCLOC(t[0], t[1], t[2], t[3], repoName, t[4], outputFile, clocfile)


#main
def main():
    e = setup()
    e.validateInput()
    startTime = datetime.now()
    e.gitinit()
    e.sendEmail()
    endTime = datetime.now()
    totalTime = endTime - startTime
    print ('Email of the CLOC report on ' + e.branch + ' of ' + e.repoName + ' completed successfully (' + str(totalTime.total_seconds()) + ' seconds)')

if __name__ == "__main__":
    main()
