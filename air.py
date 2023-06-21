from requests_html import HTMLSession
from urllib.parse import urljoin
import re
import pandas as pd

# Getting Product Links for each page
def get_links(url):
    links = []
    page_num = 1
    while True:
        session = HTMLSession()
        response = session.get(url)

        # Render the JavaScript on the page
        response.html.render(sleep=5)

        # Extract the URLs to each listing page
        listings = response.html.xpath('//*[@id="site-content"]/div/div[2]/div/div/div/div/div[1]', first=True)  # the whole listing block
        for item in listings.absolute_links:
            links.append(item)

        # Constructing the next page URL
        tags = response.html.find('a')
        pattern = r'<a aria-label="Next"'
        matches = [tag for tag in tags if re.search(pattern, str(tag.html))]
        next_page_url = None
        for match in matches:
            href = match.attrs.get('href')
            next_page_url = urljoin(url, href)

        # Update the URL for the next iteration
        if next_page_url is not None:
            url = next_page_url
        else:
            break

        print(f"{len(links)} URLs have been extracted from page {page_num}")
        print(f">>>>>>>>>> HEADING TO PAGE {page_num + 1} <<<<<<<<<<")
        print('---------------------------------------')
        page_num += 1

    return links


 # Extracting Listing information

def extract_details(urls):
	print('---------------------------------')
	print('---------------------------------')
	print('STARTING DATA EXTRACTION')
	session = HTMLSession()
	r = session.get(urls)
	r.html.render(sleep=2)  # rendering the page of each listing
	name = r.html.find('div._b8stb0', first=True).text
	try:
		rating = r.html.find('span._12si43g', first=True).text
	except:
		rating = 'New,No_Rating'
	try:
		price = r.html.find('span._tyxjp1', first=True).text
	except AttributeError:
		try:
			price = r.html.find('span._1y74zjx', first=True).text
		except AttributeError:
			price = None
	listings = {
	'name':name,
	'price':price,
	'rating':rating
	}
	print('Details extracted.....')

	return listings


def save_to_csv():
	data = pd.DataFrame(products)
	print(data)
	data.to_csv('sample.csv',index=False)

initial_url = 'https://www.airbnb.com/s/Nashville--TN--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-07-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Nashville%2C%20TN&place_id=ChIJPZDrEzLsZIgRoNrpodC5P30&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click'
urls = get_links(initial_url)
sub = urls[:20]
products = [extract_details(url) for url in sub]
save_to_csv()


