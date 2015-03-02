#!/usr/bin/python

import appindicator
import pynotify
import urllib
import json
import sys
import webbrowser

import gobject
import gtk
gtk.gdk.threads_init()

import threading

class Twitch:
  def __init__(self):
    self.twitchUsername = "xrbrs" # Your twitch username

  def push_notifications(self, streams):
    for stream in streams:
      urllib.urlretrieve(stream["image"], "/tmp/twitcher.png")

      pynotify.init("image")
      self.n = pynotify.Notification("%s just went LIVE!" % stream["name"],
        stream["status"],
        "/tmp/twitcher.png",
      )
      
      self.n.show()

  def fetch_followed_channels(self, username):
    """Fetches user followed channels from Twitch.
    
    Args:
      username: twitch account username.

    Returns:
      A list of followed channels. For example:

      ["cohhcarnage", "itmejp", "ezekiel_iii"]
    """
    try:
      self.f = urllib.urlopen("https://api.twitch.tv/kraken/users/%s/follows/channels?limit=100" % username)
      self.data = json.loads(self.f.read())
      self.followedChannels = []
      for channel in self.data['follows']:
        self.followedChannels.append(channel['channel']['display_name'])
      return self.followedChannels
    except RuntimeError:
      return None

  def fetch_live_streams(self, channels):
    """Fetches live streams from Twitch.

    Args:
      channels: twitch channels, passed as a list.

    Returns:
      A list of dictionaries, with live streams data. For example:

      [
        {
          'name': 'cohhcarnage',
          'status': '[DAY 500! Wooo!] H1Z1 Battle Royales',
          'image': 'http://www.twitch.tv/channels/cohhcarnage.jpeg',
          'url': 'http://www.twitch.tv/cohhcarnage'
        },
        {
          'name': 'itmejp',
          'status': 'Battle Royale w/ @itmeJP',
          'image': 'http://www.twitch.tv/channels/itmejp.jpeg',
          'url': 'http://www.twitch.tv/itmejp'
        }
      ]
    """
    try:
      self.f = urllib.urlopen("https://api.twitch.tv/kraken/streams?channel=%s" % ','.join(channels))
      self.data = json.loads(self.f.read())
      self.liveStreams = []
      for stream in self.data['streams']:
        # For some reason sometimes status is not defined on twitch
        try:
          self.status = stream['channel']['status']
        except RuntimeError:
          self.status = "Playing now %s" % stream['channel']['game']
        
        st = {
          'name': stream['channel']['display_name'],
          'status': self.status,
          'image': stream['channel']['logo'],
          'url': "http://www.twitch.tv/%s" % stream['channel']['name']
        }

        self.liveStreams.append(st)
      return self.liveStreams
    except RuntimeError:
      return None

class Indicator():
  def __init__(self):
    self.a = appindicator.Indicator(
      'wallch_indicator',
      '/home/rbrs/Documents/twitch-icon.png',
      appindicator.CATEGORY_APPLICATION_STATUS
    )
    self.a.set_status(appindicator.STATUS_ACTIVE)

    self.menu = gtk.Menu()
    self.streamsMenu = gtk.Menu()

    self.streamsMenuDisabled = gtk.MenuItem('Loading streams...')
    self.streamsMenuDisabled.set_sensitive(False)

    self.streamsMenuItem = gtk.MenuItem("...")
    self.streamsMenuItem.set_submenu(self.streamsMenu)

    self.menuItems = [
      gtk.MenuItem('Check now'),
      gtk.SeparatorMenuItem(),
      self.streamsMenuItem,
      gtk.SeparatorMenuItem(),
      gtk.MenuItem('Settings'),
      gtk.MenuItem('Quit')
    ]

    self.menuStreamsItems = []

    for i in self.menuItems:
      self.menu.append(i)

    self.a.set_menu(self.menu)

    for i in self.menu.get_children():
      i.show()

    self.menuItems[0].connect('activate', self.refresh_streams_init)
    self.menuItems[-1].connect('activate', self.quit)

  def rebuild_menu(self):
    for i in self.menu.get_children():
      self.menu.remove(i)

    for i in self.menuItems:
      self.menu.append(i)

    for i in self.menu.get_children():
      i.show()

  def open_link(self, widget, url):
    webbrowser.open_new_tab(url)

  def refresh_streams_init(self, widget):
    threading.Thread(target=self.refresh_streams, args=(widget)).start()

  def refresh_streams(self, items):
    """Refreshes live streams.
    
    This function fetches followed channels, checks which ones are live, updates
    menu accordingly and pushes notifications of new streams.

    Args:
      silent: should application hide notifications, passed as a boolean

    """
    self.menuItems[0].set_sensitive(False)
    self.menuItems[0].set_label("Checking...")
    self.menuItems[2] = self.streamsMenuDisabled
    self.rebuild_menu()

    self.tw = Twitch()
    self.followedChannels = self.tw.fetch_followed_channels("xrbrs")
    self.liveStreams = self.tw.fetch_live_streams(self.followedChannels)

    # Push notifications of new streams
    self.tw.push_notifications(self.liveStreams)

    # Update menu
    self.streamsMenuItem.set_label("Live channels (%d)" % len(self.liveStreams))
    for i in self.streamsMenu.get_children():
      self.streamsMenu.remove(i)

    self.menuStreamsItems = []
    for index, stream in enumerate(self.liveStreams):
      self.menuStreamsItems.append(gtk.MenuItem(stream["name"]))
      self.menuStreamsItems[index].connect('activate', self.open_link, stream["url"])
      self.streamsMenu.append(self.menuStreamsItems[index])

    for i in self.streamsMenu.get_children():
      i.show()

    self.menuItems[2] = self.streamsMenuItem
    self.rebuild_menu()
    self.menuItems[0].set_label("Check now")
    self.menuItems[0].set_sensitive(True)

  def main(self):
    gtk.main()

  def quit(self, item):
    gtk.main_quit()

if __name__=="__main__":
  gui = Indicator()
  gtk.gdk.threads_enter()
  gui.main()
  gtk.gdk.threads_leave()

