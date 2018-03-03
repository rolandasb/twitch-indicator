# Twitch Indicator

**This project is not maintained anymore. If you want to maintain it, feel free to make a fork.**

![](http://i.imgur.com/1yXOF6S.png)

Twitch.tv indicator for Linux. Tracks your followed channels and notifies when they go live.

### Setup

We don't have official PPA yet, but meanwhile you can use [PPA provided by Web Upd8](http://www.webupd8.org/2015/03/twitchtv-indicator-lets-you-know-when.html) (thanks Andrew!):
```
sudo add-apt-repository ppa:nilarimogard/webupd8
sudo apt-get update
sudo apt-get install twitch-indicator
```

Or install manually:
```
cd twitch-indicator
sudo ./setup.sh
twitch-indicator &
```

### License

This code is free software; you can redistribute it and/or modify it under the terms of the zlib License. A copy of this license can be found in the included LICENSE file.
