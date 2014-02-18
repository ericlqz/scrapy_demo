#!/bin/sh

rm hei.*

grep 'parse_post' hei > hei.parse_post
grep 'parse_next' hei > hei.parse_next
grep 'use' hei > hei.proxy
grep 'Mfw' hei > hei.item
grep 'update' hei > hei.item.store
grep 'insert' hei >> hei.item.store
grep 'retrieve' hei > hei.retrieve


sort hei.retrieve > hei.retrieve.sort
sort hei.item | uniq > hei.item.sort
