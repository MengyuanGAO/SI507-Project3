# Scraping the National Park Website


### Part 0 

* There are 10 images on the page `http://newmantaylor.com/gallery.html`. Some of them have "alt text", which is the text that is displayed or spoken because of browser limitations, or because someone is using a screen reader, for example. Scrape this page and print out the alt text for each image. If there is no alt text, print "No alternative text provided!" 


### Part 1 

* Access and cache data, starting from `https://www.nps.gov/index.htm`. You will ultimately need the HTML data from all the parks from Arkansas, California, and Michigan. So, you should save on your computer data from the following pages, in files with the following names:

	* [Main page data](https://www.nps.gov/index.htm), `https://www.nps.gov/index.htm`, in a file `nps_gov_data.html`

	* [Arkansas](https://www.nps.gov/state/ar/index.htm), `https://www.nps.gov/state/ar/index.htm`, in a file `arkansas_data.html`

	* [California](https://www.nps.gov/state/ca/index.htm), `https://www.nps.gov/state/ca/index.htm`, in a file `california_data.html`

	* [Michigan](https://www.nps.gov/state/mi/index.htm), `https://www.nps.gov/state/mi/index.htm`, in a file `michigan_data.html`



### Part 2 


* Define a class `NationalSite` that accepts a BeautifulSoup object as input to its constructor, representing 1 National Park / National Lakeshore / etc (e.g. [what you see here](https://www.dropbox.com/s/zngd317gqwan9p7/Screenshot%202017-09-30%2016.32.49.png?dl=0) or [what you see here](https://www.dropbox.com/s/nngi1q95otic2f1/Screenshot%202017-09-30%2016.34.57.png?dl=0))

* A `NationalSite` instance should have the following instance variables:

	* `location` (state, or a city, or states ...  whatever location description is provided)
	* `name` (e.g. `"Alcatraz Island"`, `"Channel Islands"`...)
	* `type` (e.g. `"National Lakeshore"`, `"National Monument"`... if there is no specified type, this value should be the special value `None`)
	* `description` (e.g. `"Established in 1911 by presidential proclamation, Devils Postpile National Monument protects and preserves the Devils Postpile formation, the 101-foot high Rainbow Falls, and pristine mountain scenery. The formation is a rare sight in the geologic world and ranks as one of the world's finest examples of columnar basalt. Its columns tower 60 feet high and display an unusual symmetry."` -- if there is no description, this instance variable should have the value of the empty string, `""`)

* A `NationalSite` instance should also have the following methods:

	* A string method `__str__` that returns a string of the format **National Park/Site/Monument Name | Location**

	* A `get_mailing_address` method that returns a string representing the mailing address of the park/site/etc. Because a multi-line string will make a CSV more difficult, you should separate the lines in the address with a forward slash, like this: `/`. However you decide to get this information and relatively-sensibly put it together is fine. In fact, some addresses may have information included in them twice, e.g. "Yosemite National Park, CA 95389 / Yosemite National Park / CA / 95389", while some will not -- that is also OK! There is enough information to send mail if possible there, which is all that matters for our purposes: **is there some address info that will be returned in a single-line string from this function? If so, that is success.**

	
		* **NOTE:** If a park has no mailing address, the return value of this function should be the empty string ("").

	* A `__contains__` method that checks whether the additional input to the method is included in the string of the park's name. If the input *is* inside the name of the park, this method should return `True`; otherwise, it should return `False`.

	* *Note* that you may make additional design decisions when you define your class `NationalSite` to help you write these methods successfully -- e.g. you could add other instance variables or other methods if you wanted to/found them useful.

	* After you complete this, you should try creating an instance of your `NationalSite` class with the following code, to test and see if your class definition worked properly:

	```f = open("sample_html_of_park.html",'r')
	soup_inst = BeautifulSoup(f.read(),'html.parser')```

### Part 3 

* Create a list of `NationalSite` objects from each one of these 3 states: Arkansas, California, and Michigan. They should be saved in the following variables, respectively:

	* `arkansas_natl_sites`
	* `california_natl_sites`
	* `michigan_natl_sites`


* Write 3 CSV files, `arkansas.csv`, `california.csv`, `michigan.csv` -- one for each state's national parks/sites/etc, each of which has 5 columns:

	* Name
	* Location
	* Type
	* Address
	* Description

Remember to handle e.g commas and multi-line strings so that data for 1 field all ends up inside 1 spreadsheet cell when you open the CSV!

For any park/site/monument/etc where a value is `None`, you should put the string `"None"` in the CSV file.
