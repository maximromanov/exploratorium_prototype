# Initial data format should be as follows:

`id > item > type`, which includes the following types:

~~__onom__ :: onomastic data (names)~~
~~__onto__ :: toponimic onomastic data (toponymic names)~~
__desc__ :: the top two are replaced with *desc*, which refers to a dictionary, where the further classification is provided.
__topo__ :: toponymic data (toponyms)

`date` should be replace with the following:
__yebi__ :: year of birth
__yede__ :: year of death (this one will help to count individuals, as there are often many dates in a biography)
__yemi__ :: years of other kind (not categorized)

# DataFile

Only **one** datafile per source, `*.dataUni` (`0748Dhahabi.TarikhIslam.JK007088-ara1.dataUni `). Other data structures (`*.dataGeNW` and `*.dataNETW`) should be generated on the fly from the `*.dataUni` file.
 
# Enriching Layers
In `R`, the initial data is to be split into subvariables () and expanded with  `enriching layers` that will provide additional analytical data, such as transliteration, translation, categorization (metacategories, synonyms, etc), coordinates, etc.

FileName pattern: `sourceURI` + `.descScheme.json` (?) 
 