#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arfedora-custom-gnome.py
#
#  Copyright 2016 youcef sourani <youcef.m.sourani@gmail.com>
#
#  www.arfedora.blogspot.com
#
#  www.arfedora.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import subprocess
import platform
import sys
import time





############################################################################################
def init_check():

    if os.getuid()==0:
        sys.exit("Run Script Without Root Permissions.")

    if platform.linux_distribution()[0]!="Fedora" and platform.linux_distribution()[1]!="25":
        sys.exit("Fedora 25 Not Found.")


    if not sys.version.startswith("3"):
        sys.exit("Use Python 3 Try run python3 arfedora-custom-gnome.py")


    if os.getenv("XDG_CURRENT_DESKTOP")!="GNOME" :
        sys.exit("Your Desktop Is Not gnome shell")

init_check()
#############################################################################################





#############################################################################################
home=os.getenv("HOME")


def get_all_extensions():
	result=[]
	if os.path.isdir("%s/.local/share/gnome-shell/extensions"%home):
		for filee in os.listdir("%s/.local/share/gnome-shell/extensions"%home):
			if filee not in result:
				result.append(filee)

	if os.path.isdir("/usr/local/share/gnome-shell/extensions"):
		for filee in os.listdir("/usr/local/share/gnome-shell/extensions"):
			if filee not in result:
				result.append(filee)

	for filee in os.listdir("/usr/share/gnome-shell/extensions"):
		if filee not in result:
			result.append(filee)

	return result

old_extension=get_all_extensions()
############################################################################################





############################################################################################


extensions_to_enable=["alternate-tab@gnome-shell-extensions.gcampax.github.com",\
                      "apps-menu@gnome-shell-extensions.gcampax.github.com",\
                      "launch-new-instance@gnome-shell-extensions.gcampax.github.com",\
                      "places-menu@gnome-shell-extensions.gcampax.github.com",\
                      "background-logo@fedorahosted.org",\
                      "drive-menu@gnome-shell-extensions.gcampax.github.com",\
                      "user-theme@gnome-shell-extensions.gcampax.github.com"]


gsettings=["gsettings set org.gnome.desktop.background show-desktop-icons false",\
           "gsettings set org.gnome.desktop.background  picture-uri \
           'file:///usr/share/backgrounds/gnome/Godafoss_Iceland.jpg' ",\
           "gsettings set org.gnome.desktop.screensaver picture-uri \
           'file:///usr/share/backgrounds/gnome/Waterfalls.jpg' ",\
           "gsettings set org.gnome.desktop.interface icon-theme 'Paper' ",\
           "gsettings set org.gnome.shell.extensions.user-theme name 'Arc-Dark' ",\
           "gsettings set org.gnome.nautilus.preferences sort-directories-first true",\
           "gsettings set org.gnome.nautilus.preferences executable-text-activation ask",\
           "gsettings set org.gnome.desktop.interface gtk-theme  Arc",\
           "gsettings set org.gnome.desktop.interface enable-animations true",\
           "gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close' ",\
           "gsettings set org.gnome.nautilus.preferences always-use-location-entry false",\
           "gsettings set org.gnome.desktop.interface cursor-theme 'breeze_cursors' ",\
           "gsettings set org.gnome.Terminal.Legacy.Settings theme-variant light",\
           "gsettings set org.gnome.Terminal.Legacy.Settings default-show-menubar false"]

#########################################################################################################





def install_packs():
	check=subprocess.call("sudo dnf  copr enable youssefmsourani/arfedora-custom-gnome  -y --best",shell=True)
	if check!=0:
		sys.exit("\n\nFail Check Your Internet || Check sudo .\n\n")
	check=subprocess.call("sudo dnf -y --best install gnome-shell-extension-drive-menu\
    gnome-shell-extension-places-menu gnome-shell-extension-drive-menu\
	 gnome-shell-extension-user-theme gnome-shell-extension-apps-menu\
	  gnome-shell-extension-launch-new-instance gnome-tweak-tool\
	   powerline  gnome-terminal-nautilus  breeze-cursor-theme\
	    arc-theme paper-icon-theme ",shell=True)
	if check!=0:
		sys.exit("\n\nFail Check Your Internet || Check sudo .\n\n")
install_packs()



def check_bashrc():
	with open("%s/.bashrc"%home,"r") as myfile:
		for line in myfile.readlines():
			if "powerline-daemon" in line:
				return True
	return False

def powerline():
	if not check_bashrc():
		to_bashrc="""
if [ -f `which powerline-daemon` ]; then
	powerline-daemon -q
	POWERLINE_BASH_CONTINUATION=1
	POWERLINE_BASH_SELECT=1
	. /usr/share/powerline/bash/powerline.sh
fi
"""
		with open("%s/.bashrc"%home,"a") as myfile:
			myfile.write(to_bashrc)
		subprocess.call("source %s/.bashrc"%home,shell=True)







if old_extension!=None:
	for i in old_extension:
		subprocess.call("gnome-shell-extension-tool -d %s"%i,shell=True)
		time.sleep(1)



for i in extensions_to_enable:
	if os.path.isdir("%s/.local/share/gnome-shell/extensions/%s"%(home,i)) or \
    os.path.isdir("/usr/share/gnome-shell/extensions/%s"%i)or \
    os.path.isdir("/usr/local/share/gnome-shell/extensions/%s"%i):
		subprocess.call("gnome-shell-extension-tool -e  %s"%i,shell=True)
		time.sleep(1)



print ("\nPlease Wait.\n")
for conf in gsettings:
	subprocess.call("%s"%conf,shell=True)
	time.sleep(1)
	



powerline()
print("\nPlease Reboot System.\n")
