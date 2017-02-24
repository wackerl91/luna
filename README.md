![alt tag](https://raw.github.com/wackerl91/luna/master/icon.png)

Luna aims to be a one-size-fits-all Moonlight launcher for Kodi. Even though it's tailored for OSMC right now, it can be easily extended to support pretty much any platform where both Kodi and Moonlight Embedded are available. 
If you feel like a specific feature is missing don't hesitate to tell me and I'll see what I can do ;) 

Screenshots can be found on the [Wiki](https://github.com/wackerl91/luna/wiki)

## Prerequisites
[Moonlight-Embedded](https://github.com/irtimmer/moonlight-embedded) needs to be installed. For setup instructions please follow irtimmer's wiki.

## Installation
- Download from [release page](https://github.com/wackerl91/luna/releases)
- Copy to your OSMC installation or use a network share
- In Kodi: Settings > Addons > Install from zip file
- Optional:
    - install m2crypto (via apt-get) and pycrypto (via pip) for Luna's built in host pairing; fallback is the moonlight binary
    - install zeroconf (via pip) for mDNS discovery; fallback is an IP input field

## Features
- GameStream Host Pairing from within Luna
- Multi Host Support
- WoL Support
- Audio Device Selection
- Controller Mapping from within Luna
- Dynamic Game Library; allows for starting of specific games
- Multiple Scrapers for Game Information (configurable + chained together to provide a maximum of covers / fanarts)
- Game View similar to Kodi's movie view (cover art / fanart support)
- extensive configuration which supports nearly all of moonlight-embedded's launch options

## Bugs / Feature Requests
- Please report any bugs or feature requests on the issue tracker - I can only make Luna better if you're willing to report every issue you run into!
- Have a look at existing issues (this includes closed ones!) before opening a new one

## Eos
Luna uses a web support called [Eos](https://github.com/wackerl91/eos) for telemetry data and exception / error reporting.

This is in place for mainly two reasons:
- to get a better understanding of the user base in general (total number of users, 'active' users, currently installed versions, ...)
- to be able to compile a list of common exceptions / errors in the log, as most users either don't report them or don't include logs right away.
While I still rely on issues being reported, this takes some responsibility away from the users as I can just have a look at the database
every now and then and fix stuff that I wouldn't even know about otherwise.

The following information is gathered:
- current Luna version (no history, just plain current version in use), e.g. `0.7.0~rc6`
- system identifier, e.g. `Linux osmc 4.4.27-7-osmc`
- system version (again, no history), e.g. `2017.02-2`
- Kodi version, e.g. `17.1.1 - releasecandidate`
- number of hosts, number of games per host and GFE server version per host, e.g. `7.1.351.0` for a gen 7 server and `5` for five games on that host
(the relevance here is that there are sometimes issues that are tied to a specific GFE version, the number of hosts / games will be averaged
over all users to see if and when the main menu / game list needs UI improvements)
- each opening of Luna is logged per day (no timestamp), e.g. `2017-02-12` and tied to the user information to get usage percentage, filter out 'one-time' starters, ...
- logs are saved including the timestamp of occurrence (normalized to my timezone), log level, channel and message and tied to the user information, e.g.
```
logLevel: "warning",
logChannel: "script.luna.repository",
logMessage: "Attempted to remove non-existent device: 'None'"
```
- exceptions contain their exception type, exception message and a full stacktrace leading up to the failure; again tied to the user information. Example:
```
exceptionType: "<type 'exceptions.ValueError'>",
exceptionValue: "Moonlight binary could not be found.",
traceback: [snip]

```
- linking user information to logs / exceptions is important e.g. for calculating averages over either all or more active users, thus providing a
measure of overall functionality

From the above information I am not able to identify single users (i.e. don't know who they are and where they come from, meaning each single user is just a number in the system),
but I am able to track them through the system (usage count, logs, exceptions).

Since Eos already helped out a lot in identifying bugs I feel it's the right thing to do and thus it is enabled by default. If you don't think so,
however, you can disable it completely in the settings. If you don't want the very first start to be registered, you should do so before starting
Luna after installing / re-installing the add-on. That being said, users with no additional information attached are hard-deleted every few weeks, since it's clear they
opted out but did so after starting Luna for the first time.

In the future, Eos will also provide different other services (proxied API access, ...), but they will always be optional (if possible) and not dependent on each other,
i.e. never require you to opt-in for telemetry just so you can use something else.

## Credits
- Logo [Ben Biedrawa](http://BengerengTV.com)
- Icons from [Freepik](http://www.flaticon.com/authors/freepik), provided by [flaticon](www.flaticon.com)
- Game information and posters provided by [TheGamesDB](http://thegamesdb.net)
- Steam Background from DiglidiDudeNG over at [deviantart](http://diglididudeng.deviantart.com/art/Steam-Wallpaper-Globe-458081397)
- most of the common assets (like arrows, ...) are taken from OSMCs skin (GPLv2)
- mesh background from pixabay.com (CC0)
