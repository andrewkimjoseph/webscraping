import scrapy

import csv

data = open('input.csv', encoding='utf-8')  # opens the input file you shared
csv_data = csv.reader(data)
doctor_urls = list(csv_data)  # then, it transforms the data into a list of lists

doctor_urls.pop(0)  # then, it pops the first item out, which is the column label
all_urls = []

# here, it unpacks the list of lists
# and sorts it into one list, namely all_urls

for urls in doctor_urls:
    for url in urls:
        all_urls.append(url)

# the spider runs from here

class DoctorsInfoSpider(scrapy.Spider):

    name = 'doctors_info'
    allowed_domains = ['iconcancercentre.com.au']
    start_urls = [all_urls[1]]  # has all the links

    def parse(self, response):

        # getting each item using xpath
        link = response.request.url
        name = response.xpath("//h1/text()").get()
        degree = response.xpath("//div[@class='dr-information']/h4/text()").get()
        specialty = response.xpath("//div[@class='pill']/text()").get()

        location = response.xpath("(((//div[@class='page-intro--details-row'])[1])/text())[2]").get()
        # cleaning location because it doesn't look presentable at the moment
        # it looks like this: \n\t\t\t\t\t\t\t\t\tEpworth Freemasons\t\t\t\t\t\t\t\t
        location = location.replace('\t', '')
        location = location.replace('\n', '')

        tel = response.xpath("//div[@class='page-intro--details-col']/a/text()").get()

        fax = response.xpath("(//div[@class='page-intro--details-col'])[2]/text()[2]").get()
        # cleaning fax too, just like location
        fax = fax.replace('\t', '')
        fax = fax.replace('\n', '')

        email = response.xpath("(//div[@class='page-intro--details-row'])[2]/a/text()").get()
        special_interests = response.xpath("(//div[@class='entry-content'])[1]/ul/li/text()").getall()
        languages_spoken = response.xpath("(//div[@class='entry-content'])[2]/ul/li/text()").getall()

        icon_locations = response.xpath("//*[@id='icon-locations']/div/a/text()").getall()
        # cleaning icon_locations too, just like fax and location
        # but we do it differently because it is a list
        clean_icon_locations = []  # will store the cleaned-up locations
        for icon_location in icon_locations:
            icon_location = icon_location.replace('\t', '')
            icon_location = icon_location.replace('\n', '')
            clean_icon_locations.append(icon_location)

        # since some doctors don't have visiting locations
        # we need to check if the h3 element is there first
        visiting_h3 = response.xpath("//*[@id='visiting-locations']/h3").get()
        # if not, it means there are visiting locations
        # in such a case, we set the value to '-', a hyphen(short dash)
        if visiting_h3 is None:
            visiting_locations = '-'
        else:
            visiting_locations = response.xpath("(//div[@class='entry-content'])[3]/ul/li/text()").getall()

        # like with the visiting locations
        # some doctors don't have affiliations and memberships
        # so, we'll set another condition to check if the header is present:
        membership_h3 = response.xpath("//*[@id='memberships']/h3/text()").get()
        # we'll give a '-' for a doctor with no affiliations or memberships
        if membership_h3 is None:
            memberships = '-'
        else:
            memberships = response.xpath("//*[@id='memberships']/div/div/ul/li/text()").getall()

        biography = response.xpath("//*[@id='bio']/div/p/text()").getall()

        # we now compile the data into a dictionary, which we'll use to make the CSV file
        yield{
            'url': link,
            'name': name,
            'degree': degree,
            'specialty': specialty,
            'location': location,
            'tel': tel,
            'fax': fax,
            'email': email,
            'special_interests': special_interests,
            'languages_spoken': languages_spoken,
            'icon_locations': clean_icon_locations,
            'visiting_locations': visiting_locations,
            'affiliations_and_memberships': memberships,
            'biography': biography
            }
