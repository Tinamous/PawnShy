
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

		url = "https://haveibeenpwned.com/api/v2/breachedaccount/" + email_address + "?includeUnverified=true"
		headers = {
			'User-Agent': 'Pawn Shy (https://github.com/Tinamous/PawnShy)',
		}

		response = requests.get(url, headers=headers)

		# Insert artificial delay to make it look busy
		# even if the api returned quickly.
		time.sleep(5)

		if str(response.status_code) == "404":
			print("No results for email :-)")
			return 0, None

		if str(response.status_code) == "200":
			print("email comprised")
			results = response.json()
			count = len(results)
			print("Count: " + str(count))
			print(results)
			return count, results

		print("***** Failed to load HIBP results. *****")

		# HACK! return 5 to show an issue rather than showing all clear.
		return 5, None;

	# Lookup the domain and return
	# pwn details (for now, just pwn count)
	def lookup_domain(self, domain):
		print ("domain lookup: " + domain)

		url = "https://haveibeenpwned.com/api/v2/breaches?domain=" + domain + "&includeUnverified=true"
		headers = {
			'User-Agent': 'Pawn Shy (https://github.com/Tinamous/PawnShy)',
		}

		response = requests.get(url, headers=headers)

		# Insert artificial delay to make it look busy
		# even if the api returned quickly.
		time.sleep(5)

		if str(response.status_code) == "404":
			print("No results for domain :-)")
			return 0, None

		if str(response.status_code) == "200":
			results = response.json()
			count = len(results)
			print("Count: " + str(count))
			print(results)

			# return the total PwnCount for all breaches listed.
			pwnCount = 0
			if count > 0:
				for result in results:
					print("PwnCount: " + str(result.PwnCount))
					pwnCount = pwnCount + result.PwnCount

			return pwnCount, results

		print("***** Failed to load HIBP results. *****")

		# HACK! return large number to show an issue rather than showing all clear.
		return 100000000, None;
