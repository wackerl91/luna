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

## Issues
- Controller Mapping sometimes not working
- Audio Device Selection might or might not be working; haven't gotten any input on this so far
- Please keep in mind that Luna - while I guess it's working pretty good right now - is still alpha, so don't expect it to work perfectly

## Bugs / Feature Requests
- Please report any bugs or feature requests on the issue tracker - I can only make Luna better if you're willing to report every issue you run into!
- Have a look at existing issues (this includes closed ones!) before opening a new one

## Credits
- Logo [Ben Biedrawa](http://sooulart.com)
- Icons from [Freepik](http://www.flaticon.com/authors/freepik), provided by [flaticon](www.flaticon.com)
- Game information and posters are provided by [OMDB](http://www.omdbapi.com) under CC-BY4.0
- Additional game information and posters provided by [TheGamesDB](http://thegamesdb.net)
- Some more information is being pulled from [IGDB](https://www.igdb.com) (very developer friendly terms, thank you so much!)
- Steam Background from DiglidiDudeNG over at [deviantart](http://diglididudeng.deviantart.com/art/Steam-Wallpaper-Globe-458081397)
- most of the common assets (like arrows, ...) are taken from OSMCs skin (GPLv2)
- mesh background from pixabay.com (CC0)
