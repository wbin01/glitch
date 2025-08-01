#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).parent)

from ini_parse import IniParse
from platform_selection import PlatformSelection


class PlatformIcons(object):
    def __init__(self, desktop_environment: str):
        self.__desktop_environment = desktop_environment
        self.__plasma_icon_theme = None
        self.__gtk_icon_theme = None

    def icon_theme(self) -> str | None:
        """..."""
        if self.__desktop_environment == 'plasma':
            if self.__plasma_icon_theme:
                return self.__plasma_icon_theme

            kdeglobals = Path(os.environ['HOME']) / '.config' / 'kdeglobals'
            if kdeglobals.exists():
                ini = IniParse(kdeglobals)

                if not '[Icons]' in ini.content:
                    return None

                if not 'Theme' in ini.content['[Icons]']:
                    return None
                
                self.__plasma_icon_theme = ini.content['[Icons]']['Theme']
                return self.__plasma_icon_theme

        if self.__desktop_environment == 'mate':
            if self.__gtk_icon_theme:
                return self.__gtk_icon_theme

                gtk_icons = subprocess.getoutput(
                    'dconf read /org/mate/desktop/interface/icon-theme').strip(
                    "'")
                self.__gtk_icon_theme = gtk_icons if gtk_icons else None
                return self.__gtk_icon_theme

        if self.__desktop_environment == 'gnome':
            if self.__gtk_icon_theme:
                return self.__gtk_icon_theme

            gtk_icons = subprocess.getoutput(
                'gsettings get org.gnome.desktop.interface icon-theme').strip(
                "'")
            self.__gtk_icon_theme = gtk_icons if gtk_icons else None
            return self.__gtk_icon_theme


# https://specifications.freedesktop.org/icon-naming-spec/latest/#names
icon_naming_spec = """
address-book-new
application-exit
appointment-new
call-start
call-stop
contact-new
document-new
document-open
document-open-recent
document-page-setup
document-print
document-print-preview
document-properties
document-revert
document-save
document-save-as
document-send
edit-clear
edit-copy
edit-cut
edit-delete
edit-find
edit-find-replace
edit-paste
edit-redo
edit-select-all
edit-undo
folder-new
format-indent-less
format-indent-more
format-justify-center
format-justify-fill
format-justify-left
format-justify-right
format-text-direction-ltr
format-text-direction-rtl
format-text-bold
format-text-italic
format-text-underline
format-text-strikethrough
go-bottom
go-down
go-first
go-home
go-jump
go-last
go-next
go-previous
go-top
go-up
help-about
help-contents
help-faq
insert-image
insert-link
insert-object
insert-text
list-add
list-remove
mail-forward
mail-mark-important
mail-mark-junk
mail-mark-notjunk
mail-mark-read
mail-mark-unread
mail-message-new
mail-reply-all
mail-reply-sender
mail-send
mail-send-receive
media-eject
media-playback-pause
media-playback-start
media-playback-stop
media-record
media-seek-backward
media-seek-forward
media-skip-backward
media-skip-forward
object-flip-horizontal
object-flip-vertical
object-rotate-left
object-rotate-right
process-stop
system-lock-screen
system-log-out
system-run
system-search
system-reboot
system-shutdown
tools-check-spelling
view-fullscreen
view-refresh
view-restore
view-sort-ascending
view-sort-descending
window-close
window-new
zoom-fit-best
zoom-in
zoom-original
zoom-out
"""


class CollectIconsTool(object):
    def __init__(self):
        self.__icon_names = icon_naming_spec.split('\n')
        self.__platform_selection = PlatformSelection()

    def collect(self) -> None:
        if self.__platform_selection.desktop_environment == 'plasma':
            for name in self.__icon_names:
                print(name)

            #Gtk
            # /usr/share/icons/icon-theme/22x22/actions/icon-name.svg
            # Qt
            # /usr/share/icons/icon-theme/actions/22/icon-name.svg
            
            # Default sys
            # /usr/share/icons/hicolor/22x22/actions/icon-name.png


if __name__ == '__main__':
    collect_icons = CollectIconsTool()
    collect_icons.collect()

    icons = PlatformIcons('plasma')
    print(icons.icon_theme())
