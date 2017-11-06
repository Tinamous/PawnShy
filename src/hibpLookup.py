
import requests
import json
import time

# Have I Been Pwned Lookup
# responsible for getting pwn details from the HIBP API.
class HibpLookup():

	# Lookup the email and return
	# the number of times it appears in a compromise.
	def lookup_email(self, email_address):
		print ("email lookup: " + email_address)

		response = requests.get("https://haveibeenpwned.com/api/v2/breachedaccount/" + email_address + "?includeUnverified=true")

		# Insert artificial delay to make it look busy
		# even if the api returned quickly.
		time.sleep(5)

		if str(response.status_code) == "404":
			print("No results for email :-)")
			return 0

		if str(response.status_code) == "200":
			print("email comprised")
			results = response.json()
			print(results)
			return len(results)

		print("***** Failed to load HIBP results. *****")

		# HACK! return 5 to show an issue rather than showing all clear.
		return 5;

	# Lookup the domain and return
	# pwn details (for now, just pwn count)
	def lookup_domain(self, domain):
		print ("domain lookup: " + domain)

		# Insert artificial delay to make it look busy
		# even if the api returned quickly.
		time.sleep(5)

		return 60000
