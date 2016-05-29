import sys,os,re,subprocess

#TODO randomly generate optional parameters (properly sanitize using neo), add/retrieve password param in Jenkins

class neoSimpleTest(object): 
	""" 
	Functions that correspond to Neo commands santize parameters and store relevant information in member variables"""
	def __init__(self,config=None):
		#Check Jenkins for necessary parameters, otherwise terminate execution
		jenkinsParameters = ['AR_HOST','AR_ACCOUNT','AR_USERNAME','AR_PASSWORD','AR_NEW_ACCOUNT_DISPLAY_NAME','AR_APPLICATION','AR_SSL_HOST', 'AR_CERTIFICATE_NAME','AR_CUSTOM_DOMAIN','AR_APPLICATION_URL']
		try:
			if not frozenset(jenkinsParameters).issubset(frozenset(os.environ.keys())):
				raise ValueError("Missing necessary parameters in Jenkins Build environment - please ensure the following parameters exist:\n %s" % (''.join([i+"\n" for i in jenkinsParameters])))
		except ValueError as e: 
			print e
			sys.exit(1)

		self.host = os.environ.get('AR_HOST')
		self.account = os.environ.get('AR_ACCOUNT') #provider account
		self.username = os.environ.get('AR_USERNAME') #provider username
		self.password = os.environ.get('AR_PASSWORD') #TODO
		self.displayName = os.environ.get('AR_NEW_ACCOUNT_DISPLAY_NAME')
		self.subscriberAccount = ""
		self.application = os.environ.get('AR_APPLICATION')
		self.sslName = os.environ.get('AR_SSL_HOST')
		self.certName = os.environ.get('AR_CERTIFICATE_NAME')
		self.custDomain = os.environ.get('AR_CUSTOM_DOMAIN')
		self.appURL = os.environ.get('AR_APPLICATION_URL')
		print "this executes@!!!!@!@!@!@"

	def executeNeoCommand(self,cmd):
		"""	Creates subprocess to run neo command - returns output in line-delimited array"""
		print cmd.split()
		try:
			return subprocess.check_output(cmd.split())
		except subprocess.CalledProcessError as e: 
			print e.output 
			sys.exit(1)

	def createOrcaAccount(self): 
		cmd = "./neo.sh create-account -h %s -a %s -u %s -p %s -n %s" % (self.host, self.account, self.username, self.password, self.displayName)
		result = self.executeNeoCommand(cmd) 		
		for line in result.splitlines():
			match = re.search("Account\s+?'(\w+?)'\s+?.*?", line)
			if match:
				self.subscriberAccount = match.groups()[0]
		return result

	def deleteOrcaAcocunt(self):
		cmd = "./neo.sh delete-account -h %s -a %s -u %s -p %s" % (self.host, self.account, self.username, self.password)
		return executeNeoCommand(cmd)

	def subscribeToApp(self): 
		cmd = "neo.bat subscribe -h %s -a %s -b %s:%s -u %s -p %s" % (self.host, self.subscriberAccount, self.account, self.application, self.username, self.password)
		return executeNeoCommand(cmd)

	def unsubscribeFromApp(self): 
		cmd = "neo.bat unsubscribe -h %s -a %s -b %s:%s -u %s -p %s" % (self.host, self.subscriberAccount, self.account, self.application, self.username, self.password)
		return executeNeoCommand(cmd)		

	def generateCSR(self):
		#step 6c ignore 
		pass
	def uploadDomainCertificate(self):
		#step 6c ignore 
		pass

	def  createSSLHost(self):
		cmd = "neo.bat create-ssl-host -h %s -a %s -u %s -p %s -n %s" % (self.host,self.account,self.username,self.password, self.sslName)
		return executeNeoCommand(cmd)

	def deleteSSLHost(self): 
		cmd = "neo.bat delete-ssl-host -h %s -a %s -u %s -p %s -n %s" % (self.host,self.account,self.username,self.password, self.sslName)
		return executeNeoCommand(cmd)

	def bindDomainCert(self):
		cmd = "neo.bat bind-domain-certificate -h %s -a %s -u %s -p %s -l %s --certificate %s" % (self.host,self.account,self.username,self.password, self.sslName, self.certName)
		return executeNeoCommand(cmd)

	def unbindDomainCert(self):
		cmd = "neo.bat unbind-domain-certificate -h %s -a %s -u %s -p %s -l %s --certificate %s" % (self.host,self.account,self.username,self.password, self.sslName, self.certName)
		return executeNeoCommand(cmd)
		
	def addCustomDomain(self):
		cmd = "neo.bat add-custom-domain -h %s -a %s -u %s -p %s -e %s -i %s -l %s" % (self.host,self.account,self.username,self.password,self.custDomain,self.appURL,self.sslName)
		return executeNeoCommand(cmd)

	def removeCustomDomain(self): 
		cmd = "neo.bat remove-custom-domain -h %s -a %s -u %s -p %s -e %s -l %s" % (self.host,self.account,self.username,self.password,self.custDomain,self.sslName)
		return executeNeoCommand(cmd)

print neoSimpleTest().createOrcaAccount()
print subprocess.check_output("neo list-schemas -h hanatrial.ondemand.com -a i820059trial -u i820059 -p Building.321".split())
