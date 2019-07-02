import unittest, re, getpass, smtplib, ssl, os, subprocess, sys, pip, base64, git 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pip._internal import main
from datetime import datetime
from secrets import myDefaultPassword

class emailCLOC:

    # Get repository name from URL
    def getRepository(self):
        return(self.repoUrl[self.repoUrl.rfind('/')+1:self.repoUrl.rfind('.')])

    def validateEmail(self, email):
        errorMessage = email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errorMessage = errorMessage+"Email format is invalid\n"

    def validateURL(self, url):
        errorMessage = url
        if not re.match(r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(\/)?", url) and (not len(url)==0):
            errorMessage = errorMessage +"Git repository is invalid.\n"

    def gitinit(self):
        repo = self.getRepository()
        currentDirectory = "./"
        if not os.path.exists(currentDirectory+repo):
            print ('Cloning ' + repo + '...')
            git.Git(currentDirectory).clone(self.repoUrl)
        gitrepo = git.Repo(repo)
        gcmd = git.cmd.Git(repo)
        gcmd.pull()
        print ('Checking out'+ repo + '...')
        gitrepo.git.checkout("-f", self.branch)

        print ('Running CLOC report for ' + repo + '...')
        proc = subprocess.Popen([currentDirectory+self.clocfile,currentDirectory+repo, "--csv","--out", self.outputFile , "--quiet"], stdout=subprocess.PIPE)
        proc.stdout.read()

    def sendEmail(self):
        msg = MIMEMultipart()
        msg['Subject'] = 'The CLOC Report of the %s epository' % self.getRepository()
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

    # def speedInput(input):
    #     #test input
    #     me = "retrorock8821@gmail.com"
    #     you = "mw103110@gmail.com"
    #     defaultRepoURL = "https://github.com/classic89/Forbidden-Island.git"
    #     defaultBranch = "master"

    #     if (input is emailCLOC.myEmail):
    #         emailCLOC.myEmail = me
    #     if (input is emailCLOC.myPassword):
    #         emailCLOC.myPassword = myDefaultPassword.decode()
    #     if (input is emailCLOC.yourEmail):
    #         emailCLOC.yourEmail = you
    #     if (input is emailCLOC.repoUrl):
    #         emailCLOC.repoUrl = defaultRepoURL
    #     if (input is emailCLOC.branch):
    #         emailCLOC.branch = defaultBranch
    #     emailCLOC.validateInput(myEmail, yourEmail, myPassword, repoURL, branch, outputFile)

    def validateInput(self, myEmail, yourEmail, myPassword, repoURL, branch, outputFile):
        self.validateEmail(myEmail)
        print("From :"+myEmail)
        self.validateEmail(yourEmail)
        print("To: "+yourEmail)
        self.validateURL(repoURL)
        print("Repository : "+repoURL)
        print("Branch : "+branch)
        print("Attachment: "+outputFile)
        

    def __init__(self, myEmail, yourEmail, myPassword, repoURL, repoName, branch, outputFile, clocfile):
        self.myEmail= myEmail
        self.myPassword = myPassword
        self.yourEmail = yourEmail
        self.repoUrl = repoURL
        self.repoName = repoName
        self.branch = branch
        self.outputFile = outputFile
        self.clocfile = clocfile

# def main(self):
myEmail= input("Type your email: ")
myPassword = getpass.getpass(prompt='Type your password: ', stream=sys.stderr)
yourEmail = input("Type the email for report: ")
repoURL = input("Git URL: ")
repoName = self.getRepository()
branch = input("Git branch: ")
logtime = datetime.now().strftime("%Y%m%d%H%M%S")
outputFile = "CLOC_"+self.getRepository()+"_"+branch+"_"+logtime+".csv"
clocfile = "cloc-1.64.exe"
e = emailCLOC(myEmail, yourEmail, myPassword, repoURL, repoName, branch, outputFile, clocfile)
e.validateInput(myEmail, yourEmail, myPassword, repoURL, branch, outputFile)
startTime = datetime.now()
e.gitinit()
e.sendEmail()
endTime = datetime.now()	
totalTime = endTime - startTime
print ('Process for branch ' + e.branch + ' of repository ' + e.getRepository() + ' completed successfully (' + str(totalTime.total_seconds()) + ' seconds)')


#main
# if __name__ == "__main__":
#     main()
