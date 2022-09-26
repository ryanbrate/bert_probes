A pipeline to explore wikidata extracts and property co-occurrence, build a subset of wikidata, build plm mask prediction statements, probe hugging face models and calculate resulting R@n scores.

# 1. Explore property co-occurrence counts for wikidata extracts

    i.e., get counts of coincident (existing) wikidata properties in extracted set - which properties are we interested in?

* paste wikidata extracts csv into "data/wikidata_extracts"
    * amend id column header to "ID"
    * amend label column header to "labels"
    * note: this csv is assumed comma separated

Run:
```
cd scripts/explore_wikidata_extracts/
python3 frequency.py  # outputs frequency of each column into CL
```

* update "scripts/explore_wikidata_extracts/stats_configs.json", each config run separately
python3 stats.py  # examines coincident columns of complete data, for cols specified

Run: 
```
python3 combinations.py
```


# 2. Build a subset of wikidata extracts

    Create a subset of the wikidata extracts, retaining only those datapoints which have full data for all of the selected wikidata properties of interest.

* Update "scripts/build_extracts_subset/build_subset_configs.json", each config run separately

Run:
```
cd scripts/build_extracts_subset/
python3 build_subset.py
```

The result overwrites any existing
The resultant csv is comma separated


# 3. Format wikidata extracts

    format the wikidata property names, and values of the collated subset

I.e.:
* The probes are formed by appending "$(wikidata property name) $(datapoint property value)", hence we may wish to format the column name to something more natural language appropriate

* Some of the property values, e.g., date are not in a very palatable format

Run
```
cd format_wikidata_extracts
python3 format_extracts.py
```

The result overwrites any existing
The resultant csv is comma separated


# 4. Build probe combinations

Run:
```
cd scripts/build_probes
python3 build_probes.py
```

The result overwrites any existing
The resultant csv is tab separated


# 5. Probe PLMs

Run:
```
cd scripts/predict
python3 predict.py
```

The resultant overwrites any existing
resultant csv is Tab separated


# 6. Calculate r@1 and r@5 values

Run:
```
cd scripts/r_values
python3 r_values
```

The resultant overwrites any existing
resultant csv is Tab separated

# 7. sign test 

Run:
```
cd scripts/sign_test
python3 sign_test
```

Reports result in the terminal
