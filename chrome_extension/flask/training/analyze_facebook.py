import requests
import re
import sys

page_name = 'myiannopoulos'


access_token = 'EAACEdEose0cBACqNv0XAv3EWUsZANl4hyYBR7Kmqu3ZBfOYpYEEnSzbdzYSq3nKhEIVSbI9o2i2MjZCQzZC3HAZCMbtCMsX5EWW5jjcUi4wg2JbML6f4fYlF3xScXkVJ1aYpHK3iVSoQKmarJFD3AicfU2f4iHe3Maaot3upO1wZDZD'
next_url = 'https://graph.facebook.com/' + page_name + '/feed?access_token=' + access_token

print(next_url)

posts = []
num_pages = 0

filename = 'texts/facebook/' + page_name + '_r.txt'
output = open(filename, 'w')

while next_url and next_url is not None:
	res = requests.get(next_url).json()	

	if 'data' not in res or res['data'] is None:
		break

	for obj in res['data']:
		if 'message' not in obj:
			continue
		message = re.sub(r'[^\x00-\x7f]',r'', obj['message'])
		posts.append(message)
		output.write(message)
		output.write('\n')

	next_url = res['paging']['next']
	num_pages += 1
	print('Saw ' + str(num_pages) + ' pages')

output.close()

print('**Saw ' + str(num_pages) + ' pages')