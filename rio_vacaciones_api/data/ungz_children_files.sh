#!/bin/bash

cd 3RioMarch2024
mv listings.csv listings_summary.csv
mv reviews.csv reviews_summary.csv
gzip -d listings.csv.gz
gzip -d reviews.csv.gz
gzip -d calendar.csv.gz
cd ..
cd 2RioDecember2023
mv listings.csv listings_summary.csv
mv reviews.csv reviews_summary.csv
gzip -d listings.csv.gz
gzip -d reviews.csv.gz
gzip -d calendar.csv.gz
cd ..
cd 1RioSeptember2023
mv listings.csv listings_summary.csv
mv reviews.csv reviews_summary.csv
gzip -d listings.csv.gz
gzip -d reviews.csv.gz
gzip -d calendar.csv.gz
cd ..