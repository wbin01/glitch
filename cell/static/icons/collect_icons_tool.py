#!/usr/bin/env python3
import sys


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
        self.__platform = sys.argv[1] if len(sys.argv) > 1 else None

    def collect(self) -> None:
        if not self.__platform:
            print(
                'Send a platform name, like:\n    '
                'plasma, cinnamon, gnome, windows-7, windows-10, windows-11\n'
                'Ex:\n    python collect_icons_tool.py plasma')
            return

        # Gtk:     /usr/share/icons/icon-theme/22x22/actions/icon-name.svg
        # Qt:      /usr/share/icons/icon-theme/actions/22/icon-name.svg
        # Default: /usr/share/icons/hicolor/22x22/actions/icon-name.png
        if self.__platform == 'plasma':
            path = '/usr/share/icons/icon-theme/actions/22'
        elif self.__platform in ['cinnamon', 'gnome']:  # TODO: Gnome is scaled
            path = '/usr/share/icons/icon-theme/22x22/actions'
        elif self.__platform in ['windows-7', 'windows-10', 'windows-11']:
            pass
        elif self.__platform == 'linux':
            path = '/usr/share/icons/hicolor/22x22/actions'
        else:
            path = None

        if path:
            for name in self.__icon_names:
                print(name)


if __name__ == '__main__':
    collect_icons = CollectIconsTool()
    collect_icons.collect()
