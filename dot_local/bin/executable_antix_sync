#!/bin/sh
    # backup existing database in local directory
    cp /home/ssserpent/.local/share/buku/bookmarks.db /home/ssserpent/.local/share/buku/bookmarks.db_bak
    # pull operation
    rsync -avzu ssserpent@antix:/home/ssserpent/.config/local/share/buku/bookmarks.db /home/ssserpent/.local/share/buku/bookmarks.db
    # push operation
    rsync -avzu /home/ssserpent/.local/share/buku/bookmarks.db ssserpent@antix:/home/ssserpent/.config/local/share/buku/bookmarks.db
    # update timestamp on local database
    touch /home/ssserpent/.local/share/buku/bookmarks.db
    # backup existing database in local directory
    cp /home/ssserpent/Documents/mydirtynotes.txt /home/ssserpent/Documents/mydirtynotes.txt_bak
    # pull operation
    rsync -avzu ssserpent@antix:/home/ssserpent/Documents/mydirtynotes.txt /home/ssserpent/Documents/mydirtynotes.txt
    # push operation
    rsync -avzu /home/ssserpent/Documents/mydirtynotes.txt ssserpent@antix:/home/ssserpent/Documents/mydirtynotes.txt
    # update timestamp on local database
    touch /home/ssserpent/Documents/mydirtynotes.txt
