[![Build Status](https://travis-ci.com/awoodwa/PlanIt.svg?branch=master)](https://travis-ci.com/awoodwa/PlanIt)


# Welcome to PlanIt

## What would Al Gore do?

The world is on fire, and we want to ask you: WWAGD? Whether you're a resident or a representative, use PlanIt to start your journey of green technology discovery. There's a lot of information out there and we want to help you interpret it.

### Getting Started:

To fully utilize this program, an access code must first be obtained granting access to the data. Follow the link below and enter the appropriate information to get an API key:
    https://developer.nrel.gov/signup/

Once an API key has been assigned to you, [follow this link to open PlanIt!](https://planit-project.herokuapp.com/)

In the app, you will be prompted to input your custom API key.

### Using PlanIt

After navigating to the website, feel free to explore the home screen. Hovering over each state capital will give you our best estimate of how much energy a single wind turbine or a single solar panel will provide in that geographic region.

When you're ready, click the **PlanIt** button and from the drop-down menu, select your use-case: government or resident.

#### Using the Government Option

First, we ask that you select your state from the drop down menu. Unfortunately, Hawaii and Alaska are not covered in the database yet.

You should then enter your city or town name. We ask that you enter it with the first letters of any parts of the name capitalized, and please do not enter an abbreviation (for example, write Los Angeles instead of LA).

Optionally, you can input your energy percentage goal. Not every city or town is ready for complete conversion to renewables, so feel free to enter anywhere from 1-100%.

As a government or township entity, we want to know how much land you can dedicate to installing wind turbines and solar panels. You'll be able to explore options of many combinations of turbines and panels, but first we ask that you enter how much land could be developed into wind and/or solar farms. Please use $km^2$.

Finally, you are required to enter your API key from the NREL website in order to access the data.

When you are done entering the required (and optional) information, please wait while the application takes into account your geographic resources, energy goals, and more.

The final screen will be a chart that allows for an exploration of our recommendations. You'll notice that you can hover your cursor over the chart to see the cost of certain turbine and panel combinations and how well that specific combination achieves your goal in a percentage. Note the black line: this indicates land availability restrictions. Anything above and to the right is realistically impossible given your inputted land availability. However, feel free to explore the options in that part of the chart to establish context for the recommended combinations.

![heroku government gif](https://github.com/awoodwa/PlanIt/blob/master/PlanIt/static/governmentgif.gif)

#### Using the Resident Option

Similar to the government option, we ask that you select your state from the dropdown menu (only those states within the continuous 48 will work) and your city or town.

Next, we want to know how big your household is. Single residents to community living scenarios are welcome!

You can optionally input your monthly energy usage in kWh. This can be found on your latest electricity bill. We ask that you ensure this value is for a single month's use (not two months or longer). This will make our prediction more accurate for your situation. However, if you cannot provide that at this time or if you're just exploring, we will estimate your residential energy use ourselves!

Another optional input is your energy goal percentage. We will assume you want to convert 100% of your energy use to be sourced from renewables, but we know that that's not always realistic! Feel free to input anywhere from 1-100%.

Finally, you're required to input your API key you received from the NREL website.

The results page will detail our expected energy output covered by renewables, how many solar panels we recommend you install, and the cost of that installation. However, we know that number of solar panels and cost can be prohibitive! From our research, an average rooftop can accommodate 25 solar panels. With this in mind, we also provide how much energy 25 panels would provide in your area, what percentage of your energy conversion goal that achieves, and the cost of that installation.

![heroku resident gif](https://github.com/awoodwa/PlanIt/blob/master/PlanIt/static/Residentgif.gif)

### Thank you for using PlanIt!

![Not Okay Meme](https://github.com/awoodwa/PlanIt/blob/master/PlanIt/static/not_okay_meme.PNG)
