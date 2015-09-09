DocIt
=====

Zero-conf documentation client

Intro
-----

DocIt is a almost zero-configuration documentation helper aimed to improve the way we write documentation.

(this description is assuming you are a system administrator but I'm pretty sure this applies to lots of other IT figures)

One of the biggest drawback in documentation writing is the lack of will; You spend the last two hours to get that piece of software working and is the hundredth time you reconfigure the daemon, sincerely you have no time also to write documentation. Not the fancy, tidy, schematic documentation you would like to produce, but not even two lines in the shitty wiki.

So you postpone and soon you forget what you did, because you have tons of other things to fix, create, hack.

I don't think I can find a real solution for this problem, is all about self-discipline, but I can relieve the burden. With DocIt you write snippets of documentation, thoughts and all sort of stuff you want directly from the command line (or a web interface, if you want). This then goes to a bucket where it is stored and tagged, ready to be pigeonholed later, when you have time.

Features
--------

* Client should be easily installed
* Client automatically discovers and connects to server, no need of basic configuration
* You can set tag on command line (with ``-t`` switch for example)
* Autocomplete on tags (Ajax / bash autocomplete)
* Client can accept also standard input
* Server stores snippets indexing with tags and renders in HTML
* Snippets can be modified on server with web interface, then exported with different markups
* Client sends info about the server name, the user who run, the current path and so on
