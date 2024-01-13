import json, requests, time

MAX_ITEMS = 40758
MAX_ITEMS_REQUESTED = 100
NONE = 999999999

######API######
index = open("index_2.html", "w+")
index.write("<html>\n\t<link href=\"txtstyle2.css\" rel=\"stylesheet\" type=\"text/css\" />\n\t\t<head>\n\t\t\t<meta charset=\"UTF-8\">\n\t\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t\t\t<meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">\n\t\t</head>\n\t\t<body class=\"screen-height\">\n\t\t\t<div id=\"ui-container\" class=\"ui-container-height\">\n\t\t\t\t<div class=\"ui-background\">\n\t\t\t\t<h1 class=\"ui-title\">Bubble Butt Boba Scalper Network</h1>\n\t\t\t\t<a href=\"velocity.html\">\n\t\t\t\t\t<button>sorted by sale velocity</button>\n\t\t\t\t</a>\n\t\t\t\t<div class=\"ui-grid\">\n\t\t\t\t\t<div class=\"ui-aspect\">\n\t\t\t\t\t<img src=\"https://raw.githubusercontent.com/0xhyashi/0xhyashi.github.io/main/1000.png\" height = 500 width = 500 alt=\"asuhuh\" class=\"ui-image\">\n\t\t\t\t</div>\n\t\t\t\t\t<div>\n\t\t\t\t\t\t<p class=\"ui-text\">")
index.close()
index = open("velocity.html", "w+")
index.write("<html><link href=\"txtstyle2.css\" rel=\"stylesheet\" type=\"text/css\" /><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\"></head><body class=\"screen-height\"><div id=\"ui-container\" class=\"ui-container-height\"><div class=\"ui-background\"><h1 class=\"ui-title\">Sorted by Sale Velocity</h1><div class=\"ui-grid\"><div class=\"ui-aspect\"><img src=\"https://raw.githubusercontent.com/0xhyashi/0xhyashi.github.io/main/1000.png\" height = 500 width = 500 alt=\"Abstract Image\" class=\"ui-image\"></div><div><p class=\"ui-text\">")
index.close()
market_items = open("marketable_items.json", "r") 
market_items_json = json.load(market_items)
url = "https://universalis.app/api/v2/"
worlds = ["Ultros", "Famfrit", "Exodus", "Behemoth", "Excalibur", "Lamia"]
world_count = len(worlds)
item_numbers = []
for x in market_items_json:
	item_numbers.append(x)
array_of_tuples = []
###############

def output_fast(item_name, prices_array, saleVelocity, page):
	index = open(page, "a+")
	local_p_a = prices_array.copy()
	fast_tuple = tuple((item_name, local_p_a, saleVelocity))
	array_of_tuples.append(fast_tuple)
	if prices_array.count(NONE) == 5 or saleVelocity == 0:
		return
	if prices_array[0] == -1:
		index.write("Ultros has no listings for this item!<br>")
		prices_array[0] = NONE;
	min_price = min(prices_array)

	output_buffer = "\n\t\t\t\t\t\t<div class=\"table\">\n\t\t\t\t\t\t\t\t<table>\n\t\t\t\t\t\t\t\t\t<tr>"
	output_buffer += f"{item_name} - {saleVelocity}<br>"
	output_buffer += f"\n\t\t\t\t\t\t\t\t\t\t<td>Ultros</td><td>Famfrit</td><td>Exodus</td><td>Behemoth</td><td>Excalibur</td><td>Lamia</td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>"
	for item_price in prices_array:
		if item_price == NONE:
			item_price = "∅"
		if min_price == item_price:
			output_buffer += f"\n\t\t\t\t\t\t\t\t\t\t<td>§{item_price}✓</td>"
		else:
			output_buffer += f"\n\t\t\t\t\t\t\t\t\t\t<td>§{item_price}✓</td>"
	output_buffer += "\n\t\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t</table>\n\t\t\t\t\t\t\t</div>"
	index.write(output_buffer)
	output_buffer = "_______________________________<br>"
	index.write(output_buffer)
	index.close()
	return

def build_url(world_name):
	local_url = url
	local_url += world_name + "/"
	max_count = 0
	for x in item_numbers:
		if max_count != 100:
			max_count += 1
			local_url += str(x)
			local_url += ","
	return(local_url[:-1])		

def request_items():
	global item_numbers 						# all items
	world_response = []							# array of json responses
	item_count = 0 								# total items in url
	item_price_array = [0]*world_count  		# array of item prices
	
	for x in range(0, world_count): 			# for each world name,
		api_url = build_url(worlds[x])			# make url for request
		print("Getting request...")				# then make request
		try:
			response = requests.get(api_url) 		# putting each response
			response = response.json()				# into worlds_response[]
		except:
			time.sleep(5)
			print("Retrying request...")
			response = requests.get(api_url) 	
			response = response.json()	

		world_response.append(response)

	item_count += MAX_ITEMS_REQUESTED           # add 100, the max requests,
	requested_list = item_numbers[:item_count]	# to item count and get list
	item_numbers = item_numbers[item_count::]	# of requested items & truncate
												# global array for next set

	for x in requested_list:
		for i in range(0, world_count):
			sanity_check = world_response[i]['items'].get(str(x)) # make sure response returned item
			if sanity_check:
				saleVelocity = world_response[i]['items'][str(x)]['regularSaleVelocity'] # get its sale velocity
				if world_response[i]['items'][str(x)]['listings'] != []: # if there is a response, add it to array
					item_price_array[i] = world_response[i]['items'][str(x)]['listings'][0]['pricePerUnit']
				elif i == 0: 
					item_price_array[i] = -1 # if no items, and homeworld, set it to -1, signify no listings
				else:
					item_price_array[i] = NONE # if not homeworld, set to NONE, which allows for proper min to be found


		if item_price_array[0] == -1: # if homeworld has no listings, display all listings
				output_fast(market_items_json[str(x)]['en'], item_price_array, saleVelocity, "index_2.html")

		else: 
			ultros_price = item_price_array[0]												 # find homeworld price
			minimum_price = min(item_price_array)											 # find minimum
			percentage = ultros_price - minimum_price										 # calculate percentage difference
			percentage = percentage / minimum_price * 100	
			min_world = item_price_array.index(minimum_price)								 # find which world has minimum
			if abs(percentage) > 20 and saleVelocity > 2:									 # if greater than 20% different, and high sale velocity,
				output_fast(market_items_json[str(x)]['en'], item_price_array, saleVelocity, "index_2.html") # print it

def main():
	global array_of_tuples
	for x in range(0, 100%len(item_numbers)):
		request_items()
	index = open("index_2.html", "a+")
	index.write("</div></div></div></div></body></html>")
	index.close()
	array_of_tuples.sort(key=lambda tup: tup[2], reverse=True)
	for x in range(0, len(array_of_tuples)):
		output_fast(array_of_tuples[x][0],array_of_tuples[x][1],array_of_tuples[x][2], "velocity.html")
	print("DONE")



if __name__ == '__main__':
	main()
