#!/usr/bin/env python3
import pathlib
import sys

from platform_icons import PlatformIcons
from platform_selection import PlatformSelection

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


class IconCollectionTool(object):
    def __init__(self):
        self.__size = sys.argv[1] if len(sys.argv) > 1 else '16'
        self.__icon_names = icon_naming_spec.split('\n')
        self.__os_de = PlatformSelection()
        self.__os_icon = PlatformIcons(self.__os_de.desktop_environment)

    def collect(self) -> None:
        size = f'{self.__size}x{self.__size}'
        if self.__os_de.operational_system == 'linux':
            # Gtk:     /usr/share/icons/icon-theme/22x22/actions/icon-name.svg
            # Qt:      /usr/share/icons/icon-theme/actions/22/icon-name.svg
            # Default: /usr/share/icons/hicolor/22x22/actions/icon-name.png
            if self.__os_de.desktop_environment == 'plasma':
                path = f'/usr/share/icons/icon-theme/actions/{self.__size}'
            elif self.__os_de.desktop_environment == ['gnome', 'cinnamon']:
                # TODO: Gnome is scaled
                
                path = f'/usr/share/icons/icon-theme/{size}/actions'
            else:
                path = f'/usr/share/icons/hicolor/{size}/actions'

        # elif 'windows' in self.__os_de.operational_system:
        #     pass
        # elif self.__os_de.operational_system == 'mac':
        #     pass
        # elif self.__os_de.operational_system == 'bsd':
        #     pass
        else:
            path = None

        if not path:
            return
        
        icons_path = pathlib.Path(
            path.replace('icon-theme', self.__os_icon.icon_theme()))

        if icons_path.exists():
            for name in self.__icon_names:
                print(name)

        print('Collected from:', icons_path)


if __name__ == '__main__':
    collect_icons = IconCollectionTool()
    collect_icons.collect()
