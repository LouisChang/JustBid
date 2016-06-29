eventsim
========

Eventsim is a program that generates event data for testing and demos. It's written in Scala, because we are
big data hipsters (at least sometimes). It's designed to replicate page requests for a fake music
web site (picture something like Spotify); the results look like real use data, but are totally fake. You can
configure the program to create as much data as you want: data for just a few users for a few hours, or data for a
huge number of users of users over many years. You can write the data to files, or pipe it out to Apache Kafka.




Usage
=====

To build the executable, run

    $ sbt assembly
    $ # make sure the script is executable
    $ chmod +x bin/eventsim

(By the way, eventsim requires Java 8.)

The program can accept a number of command line options:

    $ bin/eventsim --help
        -a, --attrition-rate  <arg>    annual user attrition rate (as a fraction of
                                       current, so 1% => 0.01) (default = 0.0)
        -c, --config  <arg>            config file
            --continuous               continuous output
            --nocontinuous             run all at once
        -e, --end-time  <arg>          end time for data
                                       (default = 2015-08-12T14:56:25.006)
        -f, --from  <arg>              from x days ago (default = 15)
            --generate-counts          generate listen counts file then stop
            --nogenerate-counts        run normally
            --generate-similars        generate similar song file then stop
            --nogenerate-similars      run normally
        -g, --growth-rate  <arg>       annual user growth rate (as a fraction of
                                       current, so 1% => 0.01) (default = 0.0)
            --kafkaBrokerList  <arg>   kafka broker list
        -k, --kafkaTopic  <arg>        kafka topic
        -n, --nusers  <arg>            initial number of users (default = 1)
        -r, --randomseed  <arg>        random seed
        -s, --start-time  <arg>        start time for data
                                       (default = 2015-08-05T14:56:25.040)
            --tag  <arg>               tag applied to each line (for example, A/B test
                                       group)
        -t, --to  <arg>                to y days ago (default = 1)
        -u, --userid  <arg>            first user id (default = 1)
            --help                     Show help message

       trailing arguments:
        output-file (not required)   File name

Only the config file is required.

Parameters can be specified in three ways: you can accept the default value, you can specify them in the config file,
or you can specify them on the command line. Config file values override defaults; command line options override
everything.

Example for about 2.5 M events (1000 users for a year, growing at 1% annually):

    $ bin/eventsim -c "config/Jug.json" --from 365 --nusers 1000 --growth-rate 0.01 data/fake.json
    Initial number of users: 1000, Final number of users: 1010
    Starting to generate events.
    Damping=0.0625, Weekend-Damping=0.5
    Start: 2013-10-06T06:27:10, End: 2014-10-05T06:27:10, Now: 2014-10-05T06:27:07, Events:2468822

Example for more events (30,000 users for a year, growing at 30% annually):

    $ bin/eventsim -c "config/Jug.json" --from 365 --nusers 30000 --growth-rate 0.30 data/fake.json

Building huge data sets in parallel
===================================
You can run multiple instances of this application simultaneously if you need to generate a lot of data very quickly.
To do this, we recommend the following strategy:

* Use a different random seed for each instance. This assures that each instance will produce different data.
* Use a different starting user id for each instance (and make sure the ranges don't overlap). This assures that each
instance will produce data with different user ids.
* Create a set of configuration files, one for each instance of eventsim. This will help you re-create your data,
and help you remember the details of the data
* Do not generate data for different time periods. The generator doesn't generate full sessions if they cross the start
and end dates; you will find some incomplete data between files.


About the source data
=====================

The results of this simulation are fake... but they are based on real data. 


For the real novice
===================

If you aren't familiar with the Java toolkit (and Scala), here's a few commands to get your started.

On a Mac, you'll need to install Java 8 and Scala. I use Homebrew for package management, so I can just
install it with this command:

    $ brew install scala

On Linux (specifically Ubuntu), it's a little more complicated. Here's what works for me:

    $ echo "deb http://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
    $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 642AC823
    $ sudo apt-get update
    $ sudo apt-get install openjdk-8-jdk scala sbt

To build the executable, run

    $ sbt assembly
    $ # make sure the script is executable
    $ chmod +x bin/eventsim
