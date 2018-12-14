#!/usr/bin/env bash

mkdir -p tablebases/syzygy/regular
for endgame in "KQvK"; do
  wget -c http://tablebase.sesse.net/syzygy/3-4-5/${endgame}.{rtbw,rtbz} -P tablebases/syzygy/regular
done
9