# TODO
This file contains our to do list for **docflow**, grouped into different time periods
and annotated with our comments and thoughts. Entries are removed from this list
as they are completed and make their way into the development and / or master branch.


## Short-term
Tasks that can / should be completed in the next couple of days.

##### Adding basic documentation
Docflow is currently rather cryptic for people that are not on the Discord Server.
Adding some basic information like this file could help getting more people interested
in the project and lend useful feedback.

##### Adding tests
While the scraping spiders were originally very self-contained and more or less impossible
to test - [attempts were made](https://github.com/strinking/docflow/issues/13) to do this with
scrapy's built-in contracts. Over the time, the spiders were split up into smaller functions
that can be easily testable. Now that Travis is set up, we should **add a `test` directory
and validate the proper function of the various functions used for the spiders**.

##### Fix long Embeds in `eval` output
The Discord bot will currently raise an exception when the output of a command is too long.
A possible solution would be uploading the results to hastebin or Gist, and sending a link
to the results along with a truncated excerpt from them.



## Mid-term
Tasks that can / should be completed in the next 1-2 weeks.



## Long-term
Tasks that can / should be completed in the next 1-2 months.

##### Moving the scraper to its own module
Creating a module for the scraper itself would modularize this further and ease maintenance.
Using it would be as simple as using something like `docscrape.cpp_symbol("accumulate")`
(although further configuration would obviously be required).
