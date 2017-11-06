
# Have I Been Pwned Lookup
# responsible for getting pwn details from the HIBP API.
class HibpLookup():

	# Lookup the email and return
	# the number of times it appears in a compromise.
	def lookup_email(self, email_address):
		print ("email lookup")
		return 2;

	# Lookup the domain and return
	# pwn details (for now, just pwn count)
	def lookup_domain(self, domain):
		print ("domain lookup")
		return 60000
