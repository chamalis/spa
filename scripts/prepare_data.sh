#!/bin/bash

URLS=(
  "https://datasets.imdbws.com/title.basics.tsv.gz"
  "https://datasets.imdbws.com/title.ratings.tsv.gz"
)

if [ -n "$1" ]; then
  # if raw data folder provided as argument (positional)
  DATA_FOLDER="$1"
else
  # figure it out via the current script's path
  SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
  DATA_FOLDER=$(realpath "${SCRIPT_DIR}/../raw_data")
fi

echo Downloading and extracting dataset

# create DATA_FOLDER if it does not already exist
mkdir -p "$DATA_FOLDER" && cd "$DATA_FOLDER"
if [ $? -ne 0 ]; then
  echo "Error: Failed to create directory $DATA_FOLDER"
  exit 1
fi

echo && echo Downloading files at "$DATA_FOLDER"
for url in ${URLS[*]}; do
  filename=$(basename "$url")

  filepath="${DATA_FOLDER}/${filename}"
  filepath_gunzipped=$(basename -s .gz "$filepath")
  # check if either the compressed file or uncompressed file/folder already exists
  if [ ! -f "$filepath" ] && [ ! -e "$filepath_gunzipped" ]; then
    echo "Downloading $url ..."
    wget "$url" -O "$filepath" &> /dev/null
  fi
done

#echo && echo Extracting files
#for f in *.gz; do  # file or folder
#  outf=$(basename -s .gz "$f")
#  outpath="${DATA_FOLDER}/$outf"
#  if [ ! -e "$outpath" ]; then
#    gunzip "$f"   # will extract to $outfile by default
#  fi
#done
#echo

# No longer needed because of read_csv(quoting=3...) trick
#for f in *.tsv; do
#  # remove quotes at the beginning of columns e.g "a title
#  sed -i -e 's/\t"/\t/g' "$f"
#done

#
## find the ones inside folders and mv them in the current dir
#for f in *.tsv; do
#  if [ -d "$f" ]; then
#    # replace folder with its file (data.tsv)
#    echo  # todo
#  fi
#done

echo Done!