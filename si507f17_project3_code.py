from bs4 import BeautifulSoup
import csv
import unittest
import requests

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
gallery = requests.get('http://newmantaylor.com/gallery.html')

soup = BeautifulSoup(gallery.content, 'html.parser')
# print(soup.prettify())

all_imgs = soup.find_all('img')
for img in all_imgs:
    print(img.get('alt', 'No alternative text provided!'))

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable 
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

try:
    nps_gov_data = open('nps_gov_data.html', 'r').text
except:
    nps_gov_data = requests.get('https://www.nps.gov/index.htm').text
    f = open('nps_gov_data.html', 'w')
    f.write(nps_gov_data)
    f.close()

# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure 
# that the rest of the program can access.

# TRY: 
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data 
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.

STATE_TO_CACHE = ['ar', 'ca', 'mi']

try:
    arkansas_data = open('arkansas_data.html', 'r').text
    california_data = open('california_data.html', 'r').text
    michigan_data = open('michigan_data.html', 'r').text
except:
    soup = BeautifulSoup(nps_gov_data, 'html.parser')
    div = soup.find('div', {'class': 'SearchBar StrataSearchBar'})
    drop_down_list = div.find('ul').find_all('li')
    all_states_urls = list(map(lambda x: x.find('a')['href'], drop_down_list))
    target_urls = list(filter(lambda x: any(state in x for state in STATE_TO_CACHE), all_states_urls))
    full_target_urls = list(map(lambda x: 'https://www.nps.gov' + x, target_urls))

    arkansas_data = requests.get(full_target_urls[0]).text
    california_data = requests.get(full_target_urls[1]).text
    michigan_data = requests.get(full_target_urls[2]).text

    with open('arkansas_data.html', 'w') as ar_f, open('california_data.html', 'w') as ca_f, open('michigan_data.html',
                                                                                                  'w') as mi_f:
        ar_f.write(arkansas_data)
        ca_f.write(california_data)
        mi_f.write(michigan_data)


######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...

## Define your class NationalSite here:

class NationalSite(object):
    def __init__(self, soup_park_inst):
        name = soup_park_inst.find('h3')
        location = soup_park_inst.find('h4')
        type = soup_park_inst.find('h2')
        description = soup_park_inst.find('p')

        self.name = '' if name is None else name.text.strip()
        self.location = '' if location is None else location.text.strip()
        self.type = '' if type is None else type.text.strip()
        self.description = '' if description is None else description.text.strip()

        sub_links = soup_park_inst.find('ul').find_all('li')
        basic_info_url = ""
        for link in sub_links:
            if 'Basic Information' in link.a.text:
                basic_info_url = link.a.get("href")
                break
        if basic_info_url == '':
            self.mailing_address = ''
        else:
            basic_info_page = requests.get(basic_info_url).text
            soup_basic_info = BeautifulSoup(basic_info_page, 'html.parser')
            address_div = soup_basic_info.find('div', itemprop='address')
            if address_div.find_all('span') is None:
                self.mailing_address = ""
            else:
                street_span = address_div.find('span', itemprop='streetAddress')
                city_span = address_div.find('span', itemprop='addressLocality')
                region_span = address_div.find('span', itemprop='addressRegion')
                post_code_span = address_div.find('span', itemprop='postalCode')
                street = '' if street_span is None else street_span.text.strip()
                city = '' if city_span is None else city_span.text.strip()
                region = '' if region_span is None else region_span.text.strip()
                post_code = '' if post_code_span is None else post_code_span.text.strip()
                self.mailing_address = "/".join([street, city, region, post_code])

    def __str__(self):
        return "{} | {}".format(self.name, self.location)

    def get_mailing_address(self):
        return self.mailing_address

    def __contains__(self, term):
        return term in self.name


## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html", 'r')
# soup_park_inst = BeautifulSoup(f.read(),
#                                'html.parser')  # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.


def sites_list(data):
    soup = BeautifulSoup(data, 'html.parser')
    park_list = soup.find('ul', id='list_parks')
    if park_list is not None:
        return park_list.find_all('li', {'class': 'clearfix'})


arkansas_natl_sites = [NationalSite(site) for site in sites_list(arkansas_data)]
california_natl_sites = [NationalSite(site) for site in sites_list(california_data)]
michigan_natl_sites = [NationalSite(site) for site in sites_list(michigan_data)]

##Code to help you test these out:
# for p in california_natl_sites:
#     print(p)
# for a in arkansas_natl_sites:
#     print(a)
# for m in michigan_natl_sites:
#     print(m)

######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!


FIELD_NAMES = ['NAME', 'LOCATION', 'TYPE', 'ADDRESS', 'DESCRIPTION']


def write_to_csv(sites_list, file_name):
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, FIELD_NAMES)
        writer.writeheader()
        for site in sites_list:
            writer.writerow({
                'NAME': site.name,
                'LOCATION': site.location,
                'TYPE': site.type,
                'ADDRESS': site.get_mailing_address(),
                'DESCRIPTION': site.description
            })


write_to_csv(arkansas_natl_sites, 'arkansas.csv')
write_to_csv(california_natl_sites, 'california.csv')
write_to_csv(michigan_natl_sites, 'michigan.csv')
